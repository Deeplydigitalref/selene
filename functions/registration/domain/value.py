from attrs import define, field
from webauthn.helpers import structs
from enum import Enum

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

