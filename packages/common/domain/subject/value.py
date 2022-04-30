from typing import List
from attrs import define, field
from webauthn.helpers import structs
from webauthn.registration import verify_registration_response as webauthn_verify  # A bit coupled to be here
from enum import Enum

from common.repository.subject import webauthn_registration, subject
from common.domain.subject import subject as sub


# Subject States, transitions
class SubjectStates(Enum):
    CREATED = 'CREATED'

class SubjectEvents(Enum):
    REGISTERED = 1

class SubjectClass(Enum):
    PERSON = 'PERSON'
    SYSTEM = 'SYSTEM'

class CredentialRegistrationClass(Enum):
    WebAuthnRegistration = 'WEBAUTHN'
    ServiceRegistration = 'OAUTH-CLIENT_CREDENTIAL'

@define
class Subject:
    """
    The Value object passed between the domain and the commands
    """
    uuid: str
    subject_name: str
    is_class_of: str
    state: SubjectStates
    registrations: List = []
    model: subject.SubjectModel = field(default=None)


# Reg States, transitions, and state machine
class RegistrationStates(Enum):
    NEW = "NEW"
    CREATED = "CREATED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

class RegistrationEvents(Enum):
    NEW = 1
    INITIATION = 2
    COMPLETION = 3
    FAILURE = 4


@define
class WebAuthnRegistration:
    """
    Defines a person's WebAuthn registered credential
    The Value object passed between the domain and the commands
    """
    uuid: str
    subject_name: str
    realm: str
    is_class_of: CredentialRegistrationClass
    subject: Subject = field(default=None)
    sub: str = field(default=None)
    state: RegistrationStates = field(default=None)
    registration_options: structs.PublicKeyCredentialCreationOptions = field(default=None)
    registration_session: str = field(default=None)
    verified_registration: webauthn_verify.VerifiedRegistration = field(default=None)
    model: webauthn_registration.RegistrationModel = field(default=None)


@define
class ServiceRegistration:
    """
    Defines a service's registered credential using for the Oauth Client Credentials grant
    The Value object passed between the domain and the commands
    """
    uuid: str
    subject_name: str
    client_secret: str
    realm: str
    is_class_of: CredentialRegistrationClass
    subject: Subject = field(default=None)
    sub: str = field(default=None)
    state: RegistrationStates = field(default=None)
    model: webauthn_registration.RegistrationModel = field(default=None)

