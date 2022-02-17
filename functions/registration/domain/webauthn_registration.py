from common.domain import constants
from pyfuncify import monad
from . import webauthn_helpers
from . import registration

def registration_obligations(registration: registration.Registration) -> registration.Registration:
    opts = webauthn_helpers.generate_options(rp_id=constants.RELYING_PARTY_ID,
                                             rp_name=constants.RELYING_PARTY_NAME,
                                             subject_name=registration.subject_name)
    registration.registration_options = opts
    return monad.Right(registration)