from attrs import define, field
from webauthn.helpers import structs
from webauthn.registration import verify_registration_response as webauthn_verify  # A bit coupled to be here
from enum import Enum

from common.repository import registration

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
    registration_session: str = field(default=None)
    verified_registration: webauthn_verify.VerifiedRegistration = field(default=None)
    model: registration.RegistrationModel = field(default=None)

