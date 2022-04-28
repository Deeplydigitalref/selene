from typing import Union
import uuid
from pyfuncify import state_machine, monad, record

from common.repository.subject import subject as repo
from common.util import layer

from . import value

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
                        registrations=[registration])
    model = to_model(sub)
    return model, sub


def get(uuid: str) -> value.Subject:
    return find(uuid)


def from_registration(registration):
    return get(registration.sub)


#
# State Management
#
def state_transition(from_state: str, with_transition: str) -> monad.EitherMonad[value.SubjectStates]:
    return state_machine.transition(state_map=state_map, from_state=from_state, with_transition=with_transition)


#
# Helpers
#

def class_from_registration(registration):
    return reg_type_to_subject_class[type(registration)]


def to_model(subject: value.Subject) -> repo.SubjectModel:
    return repo.SubjectModel(uuid=subject.uuid,
                             subject_name=subject.subject_name,
                             state=subject.state.value,
                             is_class_of=subject.is_class_of.value,
                             registrations=list(map(record.at('uuid'), subject.registrations)))


def find(uuid: str) -> value.Subject:
    return to_domain(repo.find_by_uuid(uuid))


def to_domain(model: monad.EitherMonad[repo.SubjectModel]):
    if model.is_left():
        breakpoint()

    return monad.Right(value.Subject(uuid=model.value.uuid,
                                     subject_name=model.value.subject_name,
                                     state=value.SubjectStates[model.value.state],
                                     registrations=model.value.registrations,
                                     is_class_of=value.SubjectClass[model.value.is_class_of],
                                     model=model))


#
# State Management
#

#
# Observer fn
#

def call_observers(observers, args):
    [f(args) for f in observers]
    pass
