from typing import Optional, List, Dict, Tuple, Callable, Any, Union

from enum import Enum
import uuid

from pyfuncify import state_machine, monad

from common.repository import registration as repo
from common.typing.custom_types import Either
from common.util import observer, layer

from . import webauthn_registration
from . import value

reg_state_map = state_machine.state_transition_map([
    (None,                              value.RegistrationEvents.NEW,             value.RegistrationStates.NEW),
    (value.RegistrationStates.NEW,      value.RegistrationEvents.INITIATION,      value.RegistrationStates.CREATED),
    (value.RegistrationStates.CREATED,  value.RegistrationEvents.COMPLETION,      value.RegistrationStates.COMPLETED)])



#
# State Transition Finialisers
#
def commit(model: repo.RegistrationModel, registration: value.Registration):
    result = repo.create(model)
    if result.repo.is_right():
        return monad.Right(registration)
    breakpoint()
    return result


#
# API
#

def new(subject_name: str) -> value.Registration:
    reg = value.Registration(uuid=str(uuid.uuid4()),
                             subject_name=subject_name,
                             registration_state=registration_transition(None, value.RegistrationEvents.NEW).value,
                             authn_candidate=value.AuthType.WEBAUTHN)
    # call_observers(observer.observers_for_event(value.RegistrationEvents.NEW, state_observers), reg)
    return reg

def registration_obligations(registration_value: value.Registration) -> value.Registration:
    return webauthn_registration.registration_obligations(registration_value)

@layer.finaliser(finaliser_fn=commit)
def initiate(registration_value: value.Registration):
    registration_value.registration_state = registration_transition(value.RegistrationStates.NEW, value.RegistrationEvents.INITIATION).value
    model = build_model_from_registration(registration_value)
    # call_observers(observer.observers_for_event(value.RegistrationEvents.INITIATION, state_observers), model)
    return model, registration_value


def build_model_from_registration(registration_value: value.Registration) -> repo.RegistrationModel:
    return repo.RegistrationModel(uuid=registration_value.uuid,
                                  subject_name=registration_value.subject_name,
                                  registration_state=registration_value.registration_state.name,
                                  registration_challenge=registration_value.registration_options.challenge)

def find(uuid: str) -> value.Registration:
    return to_domain(repo.find_by_uuid(uuid))

def to_domain(model: Either[repo.RegistrationModel]):
    if model.is_left():
        breakpoint()

    return monad.Right(value.Registration(uuid=model.value.uuid,
                                          subject_name=model.value.subject_name,
                                          authn_candidate=value.AuthType.WEBAUTHN,
                                          registration_state=value.RegistrationStates[model.value.registration_state],
                                          registration_options=webauthn_registration.regenerate_opts(model.value)))


#
# State Management
#
def registration_transition(from_state: str, with_transition: str) -> Either[value.RegistrationStates]:
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
