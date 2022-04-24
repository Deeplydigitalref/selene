from typing import Optional, List, Dict, Tuple, Callable, Any, Union
from attrs import define, field
import uuid
from pyfuncify import state_machine, monad, record
from enum import Enum

from common.repository.subject import subject as repo
from common.util import observer, layer


# Reg States, transitions, and state machine
class States(Enum):
    CREATED = 'CREATED'


class Events(Enum):
    REGISTERED = 1


state_map = state_machine.state_transition_map([
    (None, Events.REGISTERED, States.CREATED)])


@define
class Subject():
    """
    The Value object passed between the domain and the commands
    """
    uuid: str
    subject_name: str
    state: States
    registrations: List = []
    model: repo.SubjectModel = field(default=None)


#
# Finialisers
#
def commit(model: repo.SubjectModel, subject: Subject):
    result = repo.create(model)
    if result.repo.is_right():
        return monad.Right(subject)
    breakpoint()
    return result


#
# API
#

@layer.finaliser(finaliser_fn=commit)
def new_from_registration(registration) -> Subject:
    sub = Subject(uuid=str(uuid.uuid4()),
                  subject_name=registration.subject_name,
                  state=state_transition(None, Events.REGISTERED).value,
                  registrations=[registration])
    model = to_model(sub)
    return model, sub


def get(uuid: str) -> Subject:
    return find(uuid)


def from_registration(registration):
    return get(registration.sub)


#
# State Management
#
def state_transition(from_state: str, with_transition: str) -> monad.EitherMonad[States]:
    return state_machine.transition(state_map=state_map, from_state=from_state, with_transition=with_transition)


#
# Helpers
#

def to_model(subject: Subject) -> repo.SubjectModel:
    return repo.SubjectModel(uuid=subject.uuid,
                             subject_name=subject.subject_name,
                             state=subject.state.value,
                             registrations=list(map(record.at('uuid'), subject.registrations)))


def find(uuid: str) -> Subject:
    return to_domain(repo.find_by_uuid(uuid))


def to_domain(model: monad.EitherMonad[repo.SubjectModel]):
    if model.is_left():
        breakpoint()

    return monad.Right(Subject(uuid=model.value.uuid,
                               subject_name=model.value.subject_name,
                               state=States[model.value.state],
                               registrations=model.value.registrations,
                               model=model))

    #
    # State Management
    #
    def registration_transition(from_state: str, with_transition: str) -> monad.EitherMonad:
        return state_machine.transition(state_map=reg_state_map, from_state=from_state, with_transition=with_transition)

    def is_complete(reg):
        return reg.circuit_state == value.RegistrationStates.COMPLETED.name

    #
    # Observer fn
    #

    def call_observers(observers, args):
        [f(args) for f in observers]
        pass

    # state_observers = observer.Observers([
    #     observer.Observer(event=value.RegistrationEvents.INITIATION, observer_fn=commit)
    # ])
