from typing import List
from attrs import define, field
from webauthn.helpers import structs
from webauthn.registration import verify_registration_response as webauthn_verify  # A bit coupled to be here
from enum import Enum

from common.repository.subject import subject, credential_registration


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
    registration_ids: List = []  # the uuids of the CredentialRegistrations
    registrations: List = []  # the reified CredentialRegistrations
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
class CredentialRegistration:
    uuid: str
    subject_name: str
    realm: str
    is_class_of: CredentialRegistrationClass
    subject: Subject = field(default=None)
    sub: str = field(default=None)
    state: RegistrationStates = field(default=None)
    model: credential_registration.RegistrationModel = field(default=None)


@define
class WebAuthnRegistration(CredentialRegistration):
    """
    Defines a person's WebAuthn registered credential
    The Value object passed between the domain and the commands
    """
    registration_options: structs.PublicKeyCredentialCreationOptions = field(default=None)
    registration_session: str = field(default=None)
    verified_registration: webauthn_verify.VerifiedRegistration = field(default=None)


@define
class ServiceRegistration(CredentialRegistration):
    """
    Defines a service's registered credential using for the Oauth Client Credentials grant
    The Value object passed between the domain and the commands
    """
    client_secret: str = field(default=None)

