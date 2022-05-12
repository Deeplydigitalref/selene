from typing import Union, Tuple, Callable, List
import sys
import uuid
from pymonad.maybe import Just, Nothing
from pyfuncify import state_machine, monad, record, fn

from common.repository.subject import subject as repo
from common.util import layer
from key_management.domain import sym_enc
from common.domain import oauth, activity

from . import value

SubjectReifyUnion = Union[value.CredentialRegistration,
                          oauth.value.Authorisation,
                          activity.value.Activity]

state_map = state_machine.state_transition_map([
    (None, value.SubjectEvents.REGISTERED, value.SubjectStates.CREATED)])

reg_type_to_subject_class = {
    value.WebAuthnRegistration: value.SubjectClass.PERSON,
    value.ServiceRegistration: value.SubjectClass.SYSTEM
}


#
# Finialisers
#
def commit(model: repo.SubjectModel, subject: value.Subject):
    result = repo.create(model)
    if result.repo.is_right():
        return monad.Right(subject)
    breakpoint()
    return result


#
# API
#

@layer.finaliser(finaliser_fn=commit)
def new_from_registration(registration: Union[value.ServiceRegistration, value.WebAuthnRegistration]) -> value.Subject:
    sub = value.Subject(uuid=str(uuid.uuid4()),
                        subject_name=registration.subject_name,
                        state=state_transition(None, value.SubjectEvents.REGISTERED).value,
                        is_class_of=class_from_registration(registration),
                        registration_ids=[registration])
    model = to_model(sub)
    return model, sub


def get(uuid: str, reify: Tuple[SubjectReifyUnion, Callable] = None) -> value.Subject:
    return find(uuid, reify)


def from_registration(registration):
    return get(registration.sub)

def is_valid_secret(subject: value.Subject, secret: str) -> Just:
    reg = fn.find(reg_is_class_of_service_registration, subject.registrations)
    if is_system(subject):
        return sym_enc.jwe_decrypt(reg.client_secret) == secret
    return Nothing

#
# State Management
#
def state_transition(from_state: str, with_transition: str) -> monad.EitherMonad[value.SubjectStates]:
    return state_machine.transition(state_map=state_map, from_state=from_state, with_transition=with_transition)


#
# Helpers
#

def find(uuid: str,
         reify: Tuple[SubjectReifyUnion, Callable]) -> monad.EitherMonad[Union[value.WebAuthnRegistration, value.ServiceRegistration]]:

    reg = to_domain(repo.find_by_uuid(uuid))
    if reify:
        cls, reify_fn = reify
        return reify_token_caller(cls)(reg, reify_fn)
    return reg


def credentialregistration_reifier(subject: monad.EitherMonad, reify_fn: callable) -> monad.EitherMonad[value.WebAuthnRegistration]:
    """
    Takes a monadic subject and adds the credentials domain.
    If credentials domain returns a Left, the entire subject query returns a left
    :param reg:
    :param reify_fn:
    :return monad.EitherMonad[value.Registration]:
    """
    if subject.is_left():
        return subject
    regs = reify_fn(subject.value)
    if all(map(lambda reg: reg.is_right(), regs)):
        subject.value.registrations = [reg.value for reg in regs]
        return subject
    return monad.Left(subject.value)

def authorisation_reifier(subject: monad.EitherMonad, reify_fn: callable) -> monad.EitherMonad[List[oauth.value.Authorisation]]:
    """
    Takes a monadic subject and adds any valid authorisations (authorisations which have not expired).
    When there are no un-expired auths, the collection is empty

    :param subject:
    :param reify_fn:
    :return:
    """
    if subject.is_left():
        return subject
    unexpired_authzs = reify_fn(subject.value)
    if unexpired_authzs.is_right():
        subject.value.authorisations = unexpired_authzs.value
        return subject
    return monad.Left(subject.value)

def activity_reifier(subject: monad.EitherMonad, reify_fn: callable) -> monad.EitherMonad[List[activity.value.Activity]]:
    """
    Takes a monadic subject and adds any activities registered for the subject.
    System subjects are the only type of subject which should have activities, although this is not enforced here

    :param subject:
    :param reify_fn:
    :return: monad.EitherMonad[List[activity.value.Activity]]
    """
    if subject.is_left():
        return subject
    activities = reify_fn(subject.value)

    if activities.is_right():
        subject.value.activities = activities.value
        return subject
    return monad.Left(subject.value)



def reify_token_caller(cls):
    return getattr(sys.modules[__name__], "{}_reifier".format(cls.__name__.lower()))


def class_from_registration(registration):
    return reg_type_to_subject_class[type(registration)]


def to_model(subject: value.Subject) -> repo.SubjectModel:
    return repo.SubjectModel(uuid=subject.uuid,
                             subject_name=subject.subject_name,
                             state=subject.state.value,
                             is_class_of=subject.is_class_of.value,
                             registrations=list(map(record.at('uuid'), subject.registration_ids)))


def to_domain(model: monad.EitherMonad[repo.SubjectModel]):
    if model.is_left():
        breakpoint()

    return monad.Right(value.Subject(uuid=model.value.uuid,
                                     subject_name=model.value.subject_name,
                                     state=value.SubjectStates[model.value.state],
                                     registration_ids=model.value.registrations,
                                     is_class_of=value.SubjectClass[model.value.is_class_of],
                                     model=model))

def is_system(subject: value.Subject) -> bool:
    return subject.is_class_of == value.SubjectClass.SYSTEM

def reg_is_class_of_service_registration(reg: value.CredentialRegistration) -> bool:
    return reg.is_class_of == value.CredentialRegistrationClass.ServiceRegistration
#
# State Management
#

#
# Observer fn
#

def call_observers(observers, args):
    [f(args) for f in observers]
    pass
