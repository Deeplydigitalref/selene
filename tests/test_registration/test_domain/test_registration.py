import pytest

from webauthn.helpers import structs

from functions.registration.domain import registration, value


def it_creates_new_registration():
    reg = registration.new(subject_name='test1')

    assert isinstance(reg, value.Registration)
    assert reg.subject_name == 'test1'

def it_creates_the_new_reg_in_new_state(new_reg):
    assert new_reg.registration_state == value.RegistrationStates.NEW

def it_successfully_adds_webauthn_reg_options(new_reg):
    reg = registration.registration_obligations(new_reg)

    assert reg.is_right()
    assert isinstance(reg.value.registration_options, structs.PublicKeyCredentialCreationOptions)


def it_sets_the_reg_into_initiated_state(new_reg,
                                         dynamo_mock,
                                         set_up_env):
    initiated_reg = registration.initiate(registration.registration_obligations(new_reg).value)

    assert initiated_reg.is_right()
    assert initiated_reg.value.registration_state == value.RegistrationStates.CREATED

def it_persists_the_created_reg(reg_with_options,
                                dynamo_mock,
                                set_up_env):
    initiate_reg(reg_with_options)
    reg = registration.find(reg_with_options.uuid)

    assert reg.is_right()
    assert reg.value == reg_with_options




#
# Helpers
#
@pytest.fixture
def new_reg() -> value.Registration:
    return registration.new(subject_name='test1')


@pytest.fixture
def reg_with_options() -> value.Registration:
    return registration.registration_obligations(registration.new(subject_name='test1')).value


def initiate_reg(reg) -> value.Registration:
    return registration.initiate(reg)