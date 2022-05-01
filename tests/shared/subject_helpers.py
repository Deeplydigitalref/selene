import uuid

from common.util import encoding_helpers
from common.domain.subject import value
from common.domain.policy import security_policy
from common.repository.subject import credential_registration


def create_webauthn_reg_in_created_state(reg_completion):
    challenge, request = reg_completion
    model = initiated_registration(challenge)
    return challenge, request, model


def initiated_registration(challenge):
    model = credential_registration.RegistrationModel(uuid=str(uuid.uuid4()),
                                                      subject_name="subject1",
                                                      state="CREATED",
                                                      is_class_of=value.CredentialRegistrationClass.WebAuthnRegistration.value,
                                                      realm=security_policy.Realm.CUSTOMER.value,
                                                      registration_challenge=encoding_helpers.base64url_to_bytes(
                                                          challenge))
    credential_registration.create(model)
    return model


def create_service_registration_and_subject(service_name):
    pass
