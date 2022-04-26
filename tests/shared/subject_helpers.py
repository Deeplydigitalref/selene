import uuid

from common.util import encoding_helpers
from common.repository.subject import webauthn_registration


def create_webauthn_reg_in_created_state(reg_completion):
    challenge, request = reg_completion
    model = initiated_registration(challenge)
    return challenge, request, model


def initiated_registration(challenge):
    model = webauthn_registration.RegistrationModel(uuid=str(uuid.uuid4()),
                                                    subject_name="subject1",
                                                    state="CREATED",
                                                    registration_challenge=encoding_helpers.base64url_to_bytes(
                                                        challenge))
    webauthn_registration.create(model)
    return model


def create_service_registration_and_subject(service_name):
    pass
