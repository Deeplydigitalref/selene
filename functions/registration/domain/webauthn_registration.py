from common.domain import constants
from pyfuncify import monad
from webauthn.helpers import structs
from common.domain import webauthn_helpers
from common.repository import registration
from . import value

def registration_obligations(registration: value.Registration) -> value.Registration:
    opts = webauthn_helpers.generate_options(rp_id=constants.RELYING_PARTY_ID,
                                             rp_name=constants.RELYING_PARTY_NAME,
                                             subject_name=registration.subject_name)
    registration.registration_options = opts
    return monad.Right(registration)

def regenerate_opts(model: registration.RegistrationModel) -> structs.PublicKeyCredentialCreationOptions:
    return webauthn_helpers.generate(rp_id=constants.RELYING_PARTY_ID,
                                     rp_name=constants.RELYING_PARTY_NAME,
                                     user_id=model.subject_name,
                                     user_name=model.subject_name,
                                     user_display_name=model.subject_name,
                                     challenge=model.registration_challenge)
