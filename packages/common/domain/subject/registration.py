from typing import Dict, Tuple, Callable, Any, Union
import uuid
from pyfuncify import state_machine, monad
import sys

from common.repository.subject import credential_registration as repo
from common.domain import subject
from common.domain.policy import security_policy
from common.util import observer, layer

from . import subject, value, webauthn_registration, service_registration

reg_state_map = state_machine.state_transition_map([
    (None, value.RegistrationEvents.NEW, value.RegistrationStates.NEW),
    (value.RegistrationStates.NEW, value.RegistrationEvents.INITIATION, value.RegistrationStates.CREATED),
    (value.RegistrationStates.NEW, value.RegistrationEvents.COMPLETION, value.RegistrationStates.COMPLETED),
    (value.RegistrationStates.CREATED, value.RegistrationEvents.COMPLETION, value.RegistrationStates.COMPLETED)])


#
# Finialisers
#
def commit(model: repo.RegistrationModel, registration: value.WebAuthnRegistration):
    result = repo.create(model)
    if result.repo.is_right():
        return monad.Right(registration)
    breakpoint()
    return result


def save_completed(model: repo.RegistrationModel, registration: value.WebAuthnRegistration):
    result = repo.completed_state_change(model)
    if result.repo.is_right():
        return monad.Right(registration)
    breakpoint()
    return result


def commit_service(model: repo.RegistrationModel, registration: value.ServiceRegistration):
    breakpoint()


#
# API
#

def new(subject_name: str) -> value.WebAuthnRegistration:
    reg = value.WebAuthnRegistration(uuid=str(uuid.uuid4()),
                                     subject_name=subject_name,
                                     state=registration_transition(None, value.RegistrationEvents.NEW).value)
    # call_observers(observer.observers_for_event(value.RegistrationEvents.NEW, state_observers), reg)
    return reg


def new_service(service_value) -> value.ServiceRegistration:
    reg = (service_registration.build_service_reg(service_value, registration_transition) >>
           service_registration.create_service_reg >>
           service_registration.onboard_subject >>
           service_registration.complete_registration(registration_transition))
    return reg.value


def registration_obligations(registration_value: value.WebAuthnRegistration) -> value.WebAuthnRegistration:
    return webauthn_registration.registration_obligations(registration_value)


@layer.finaliser(finaliser_fn=commit)
def initiate(registration_value: value.WebAuthnRegistration):
    registration_value.state = registration_transition(value.RegistrationStates.NEW,
                                                       value.RegistrationEvents.INITIATION).value
    model = build_model_from_registration(registration_value)
    # call_observers(observer.observers_for_event(value.RegistrationEvents.INITIATION, state_observers), model)
    return model, registration_value


def get(uuid: str, reify: Callable = None) -> monad.EitherMonad[Union[value.WebAuthnRegistration, value.ServiceRegistration]]:
    return find(uuid, reify)


@layer.finaliser(finaliser_fn=save_completed)
def complete_registration(challenge_response: Dict,
                          registration_value: value.WebAuthnRegistration) -> value.WebAuthnRegistration:
    reg_validation = webauthn_registration.validate_registration(challenge_response, registration_value)
    if reg_validation.user_verified:
        return completer(registration_value, reg_validation, onboard_subject(registration_value))
    breakpoint()


def completer(registration_value: value.WebAuthnRegistration,
              validation,
              subject: value.Subject) -> Tuple[repo.RegistrationModel, value.WebAuthnRegistration]:
    registration_value.subject = subject.value
    registration_value.verified_registration = validation
    registration_value.state = registration_transition(registration_value.state,
                                                       value.RegistrationEvents.COMPLETION).value
    registration_value.model = complete_valid_registration_model(registration_value)
    return registration_value.model, registration_value


def onboard_subject(registration_value: value.WebAuthnRegistration):
    return subject.new_from_registration(registration_value)


#
# Helpers
#

def build_model_from_registration(registration_value: value.WebAuthnRegistration) -> repo.RegistrationModel:
    return repo.RegistrationModel(uuid=registration_value.uuid,
                                  subject_name=registration_value.subject_name,
                                  state=registration_value.state.name,
                                  registration_challenge=registration_value.registration_options.challenge)


def complete_valid_registration_model(registration_value: value.WebAuthnRegistration) -> repo.RegistrationModel:
    model = registration_value.model.value
    model.state = registration_value.state.name
    model.credential = registration_value.verified_registration.json()
    model.sub = registration_value.subject.uuid
    return model


def find(uuid: str, reify: Tuple[Any, Callable]) -> monad.EitherMonad[Union[value.WebAuthnRegistration, value.ServiceRegistration]]:
    reg = to_domain(repo.find_by_uuid(uuid))
    if reify:
        cls, reify_fn = reify
        return reify_token_caller(cls)(reg, reify_fn)
    return reg


def subject_reifier(reg: monad.EitherMonad, reify_fn: callable) -> monad.EitherMonad[value.WebAuthnRegistration]:
    """
    Takes a monadic registration and adds the subject domain.
    If subject returns a Left, the entire registration query returns a left
    :param reg:
    :param reify_fn:
    :return monad.EitherMonad[value.Registration]:
    """
    if reg.is_left():
        return reg
    sub = reify_fn(reg.value)
    if sub.is_right():
        reg.value.subject = sub.value
        return reg
    return monad.Left(reg.value)


def reify_token_caller(cls):
    return getattr(sys.modules[__name__], "{}_reifier".format(cls.__name__.lower()))


def find_with_sub(uuid: str) -> value.WebAuthnRegistration:
    reg = repo.find_by_uuid(uuid)
    breakpoint()
    return to_domain(repo.find_by_uuid(uuid))


def to_domain(model: monad.EitherMonad[repo.RegistrationModel]) -> monad.EitherMonad[Union[value.WebAuthnRegistration, value.ServiceRegistration]]:
    """
    Determines the class of the registration; a WebAuth or Service registration and creates a domain object of that class.
    :param model:
    :return:
    """
    if model.is_left():
        breakpoint()

    is_class_of = value.CredentialRegistrationClass(model.value.is_class_of)

    if is_class_of == value.CredentialRegistrationClass.ServiceRegistration:
        return monad.Right(to_service_reg(model.value))
    return monad.Right(to_webauthn_reg(model.value))


def to_service_reg(model):
    return value.ServiceRegistration(uuid=model.uuid,
                                     subject_name=model.subject_name,
                                     sub=model.sub,
                                     state=value.RegistrationStates(model.state),
                                     realm=security_policy.Realm(model.realm),
                                     is_class_of=value.CredentialRegistrationClass.ServiceRegistration,
                                     client_secret=model.client_secret,
                                     model=model)


def to_webauthn_reg(model):
    return value.WebAuthnRegistration(uuid=model.uuid,
                                      subject_name=model.subject_name,
                                      sub=model.sub,
                                      state=value.RegistrationStates(model.state),
                                      realm=security_policy.Realm(model.realm),
                                      is_class_of=value.CredentialRegistrationClass.WebAuthnRegistration,
                                      registration_options=webauthn_registration.regenerate_opts(model),
                                      model=model)


#
# State Management
#
def registration_transition(from_state: value.RegistrationStates,
                            with_transition: value.RegistrationEvents) -> monad.EitherMonad[value.RegistrationStates]:
    return state_machine.transition(state_map=reg_state_map, from_state=from_state, with_transition=with_transition)


def is_complete(reg):
    return reg.circuit_state == value.RegistrationStates.COMPLETED.name


#
# Observer fn
#

def call_observers(observers, args):
    [f(args) for f in observers]
    pass


state_observers = observer.Observers([
    observer.Observer(event=value.RegistrationEvents.INITIATION, observer_fn=commit)
])
