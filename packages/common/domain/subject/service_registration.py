from typing import Dict, Callable
from pyfuncify import monad
from pymonad.tools import curry
import uuid

from common.repository.subject import service_registration as repo
from key_management.domain import crypto, sym_enc
from . import subject, value


#
# Commands
#
def build_service_reg(service_value: Dict, state_transition: Callable) -> monad.EitherMonad[value.ServiceRegistration]:
    return monad.Right(value.ServiceRegistration(uuid=str(uuid.uuid4()),
                                                 subject_name=service_value['serviceName'],
                                                 enc_secret=generate_secret(),
                                                 state=state_transition(value.RegistrationStates.NEW,
                                                                        value.RegistrationEvents.INITIATION).value))


def create_service_reg(reg: value.ServiceRegistration) -> monad.EitherMonad[value.ServiceRegistration]:
    model = build_model_from_registration(reg)
    result = repo.create(model)
    if result.is_right():
        reg.model = result.value
        return monad.Right(reg)
    breakpoint()


def onboard_subject(reg: value.ServiceRegistration) -> monad.EitherMonad[value.ServiceRegistration]:
    result = subject.new_from_registration(reg)
    if result.is_right():
        reg.subject = result.value
        reg.sub = result.value.uuid
        return monad.Right(reg)
    breakpoint()


@curry(2)
def complete_registration(state_transition: Callable,
                          reg: value.ServiceRegistration) -> monad.EitherMonad[value.ServiceRegistration]:
    reg.state = state_transition(reg.state, value.RegistrationEvents.COMPLETION).value
    model = reg.model
    model.state = reg.state.value
    model.sub = reg.subject.uuid
    result = repo.completed_state_change(model)
    breakpoint()
    if result.repo.is_right():
        return monad.Right(reg)
    breakpoint()
    return result


#
# Helpers
#

def generate_secret():
    return sym_enc.encrypt(crypto.generate_random_secret_url_safe())

def build_model_from_registration(registration_value: value.ServiceRegistration) -> repo.RegistrationModel:
    return repo.RegistrationModel(uuid=registration_value.uuid,
                                  subject_name=registration_value.subject_name,
                                  state=registration_value.state.name)
