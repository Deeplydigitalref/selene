import pytest
import json

from tests.shared.key_management_helpers import *
from tests.shared.subject_helpers import *
from tests.shared.request_fixtures import *

from webauthn.helpers import structs

from common.domain.subject import registration, value, subject
from common.domain.policy import security_policy


def setup_module():
    set_up_key_management_env()
    pass


#
# WebAuthn Reg
def it_creates_new_registration():
    reg = registration.new(subject_name='test1')

    assert isinstance(reg, value.WebAuthnRegistration)
    assert reg.subject_name == 'test1'


def it_creates_the_new_reg_in_new_state(set_up_env_without_ssm,
                                        new_reg):
    assert new_reg.state == value.RegistrationStates.NEW


def it_successfully_adds_webauthn_reg_options(set_up_env_without_ssm,
                                              new_reg):
    reg = registration.registration_obligations(new_reg)

    assert reg.is_right()
    assert isinstance(reg.value.registration_options, structs.PublicKeyCredentialCreationOptions)


def it_sets_the_reg_into_initiated_state(set_up_env_without_ssm,
                                         new_reg,
                                         dynamo_mock,
                                         set_up_env):
    initiated_reg = registration.initiate(registration.registration_obligations(new_reg).value)

    assert initiated_reg.is_right()
    assert initiated_reg.value.state == value.RegistrationStates.CREATED


def it_persists_the_created_reg(set_up_env_without_ssm,
                                reg_with_options,
                                dynamo_mock):
    initiate_reg(reg_with_options)
    reg = registration.find(reg_with_options.uuid, reify=None)

    assert reg.is_right()
    assert reg.value.uuid == reg_with_options.uuid
    assert reg_with_options.registration_options.rp.name == reg_with_options.registration_options.rp.name


def it_completes_the_registration_when_completion_valid(set_up_env_without_ssm,
                                                        dynamo_mock):
    challenge, request, model = create_webauthn_reg_in_created_state(registration_completion_usb())

    reg = registration.get(model.uuid).value
    result = registration.complete_registration(json.loads(request), reg)

    assert result.is_right()
    assert result.value.state == value.RegistrationStates.COMPLETED

def it_defaults_to_the_customer_realm(set_up_env_without_ssm,
                                                        dynamo_mock):
    challenge, request, model = create_webauthn_reg_in_created_state(registration_completion_usb())

    reg = registration.get(model.uuid).value
    completed_reg = registration.complete_registration(json.loads(request), reg).value

    assert completed_reg.realm == security_policy.Realm.CUSTOMER


def it_creates_a_subject_on_completion(set_up_env_without_ssm,
                                       dynamo_mock):
    challenge, request, model = create_webauthn_reg_in_created_state(registration_completion_usb())

    reg = registration.get(model.uuid).value

    completed_reg = registration.complete_registration(json.loads(request), reg).value

    assert completed_reg.subject.subject_name == "subject1"
    assert completed_reg.subject.is_class_of == value.SubjectClass.PERSON
    assert completed_reg.subject.state == value.SubjectStates.CREATED


#
# System Reg
def it_registers_a_new_internal_service(dynamo_mock,
                                        set_up_env):
    reg = registration.new_service(new_service_reg())

    assert isinstance(reg, value.ServiceRegistration)
    assert reg.subject_name == 'urn:service:service1'
    assert reg.state == registration.value.RegistrationStates.COMPLETED


def it_registers_service_with_realm(dynamo_mock,
                                    set_up_env):
    reg = registration.new_service(new_service_reg())

    assert reg.realm == security_policy.Realm.INTERNAL


def it_onboards_the_subject(dynamo_mock,
                            set_up_env):
    result = registration.new_service(new_service_reg())

    reg = registration.get(result.uuid, reify=(value.Subject, subject.from_registration)).value

    assert isinstance(reg, value.ServiceRegistration)
    assert reg.subject.state == value.SubjectStates.CREATED
    assert reg.subject.is_class_of == value.SubjectClass.SYSTEM


#
# Helpers
#
@pytest.fixture
def new_reg() -> value.WebAuthnRegistration:
    return registration.new(subject_name='test1')


@pytest.fixture
def reg_with_options() -> value.WebAuthnRegistration:
    return registration.registration_obligations(registration.new(subject_name='test1')).value


def initiate_reg(reg) -> value.WebAuthnRegistration:
    return registration.initiate(reg)


def new_service_reg():
    return {
        'serviceName': 'urn:service:service1',
        'realm': 'https://example.com/ontologies/sec/realm/internal'
    }
