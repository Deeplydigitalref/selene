from typing import Optional, List, Dict, Tuple, Callable, Any, Union
from attrs import define, field

from enum import Enum
import uuid

from pyfuncify import state_machine, monad

from webauthn.helpers import structs

from common.domain import value
from common.repository import registration as repo
from common.typing.custom_types import Either
from common.util import encoding_helpers, observer, layer

# Reg States, transitions, and state machine
class RegistrationStates(Enum):
    NEW = 1
    CREATED = 2
    FAILED = 3
    COMPLETED = 4

class RegistrationEvents(Enum):
    NEW = 1
    INITIATION = 2
    COMPLETION = 3
    FAILURE = 4


reg_state_map = state_machine.state_transition_map([
    (None,                              RegistrationEvents.NEW,             RegistrationStates.NEW),
    (RegistrationStates.NEW,            RegistrationEvents.INITIATION,      RegistrationStates.CREATED),
    (RegistrationStates.CREATED,        RegistrationEvents.COMPLETION,      RegistrationStates.COMPLETED)])


class AuthType(Enum):
    WEBAUTHN = 1

@define
class Registration():
    """
    The Value object passed between the domain and the commands
    """
    uuid: str
    subject_name: str
    authn_candidate: AuthType
    registration_state: RegistrationStates = field(default=None)
    registration_options: structs.PublicKeyCredentialCreationOptions = field(default=None)


#
# State Transition Finialisers
#
def commit(model: repo.RegistrationModel, registration: Registration):
    result = repo.create(model)
    if result.repo.is_right():
        return monad.Right(registration)
    breakpoint()
    return result


#
# API
#

def new(subject_name: str) -> Registration:
    reg = Registration(uuid=str(uuid.uuid4()),
                       subject_name=subject_name,
                       registration_state=registration_transition(None, RegistrationEvents.NEW).value,
                       authn_candidate=AuthType.WEBAUTHN)
    # call_observers(observer.observers_for_event(RegistrationEvents.NEW, state_observers), reg)
    return reg

@layer.finaliser(finaliser_fn=commit)
def initiate(registration_value: Registration):
    registration_value.registration_state = registration_transition(RegistrationStates.NEW, RegistrationEvents.INITIATION).value
    model = build_model_from_registration(registration_value)
    # call_observers(observer.observers_for_event(RegistrationEvents.INITIATION, state_observers), model)
    return model, registration_value


def build_model_from_registration(registration_value: Registration) -> repo.RegistrationModel:
    return repo.RegistrationModel(uuid=registration_value.uuid,
                                  subject_name=registration_value.subject_name,
                                  registration_state=registration_value.registration_state,
                                  registration_challenge=registration_value.registration_options.challenge)

#
# State Management
#
def registration_transition(from_state: str, with_transition: str) -> Either[RegistrationStates]:
    return state_machine.transition(state_map=reg_state_map, from_state=from_state, with_transition=with_transition)

def is_complete(reg):
    return reg.circuit_state == RegistrationStates.COMPLETED.name

#
# Observer fn
#

def call_observers(observers, args):
    [f(args) for f in observers]
    pass

state_observers = observer.Observers([
    observer.Observer(event=RegistrationEvents.INITIATION, observer_fn=commit)
])
