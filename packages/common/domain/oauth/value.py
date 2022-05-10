from enum import Enum
from attrs import define, field

from common.repository.oauth import authorisation

class OauthTokenRecommendations(Enum):
    DO_NOT_GRANT = 'urn:idp:recommendation:doNotGrant'

class OauthErrors(Enum):
    INVALID_CLIENT = 'urn:idp:error:invalidClient'
    INVALID_CREDENTIALS = 'urn:idp:error:invalidClientCredentials'
    INVALID_GRANT_TYPE = 'urn:idp:error:invalidGrantType'
    INVALID_SUBJECT = 'urn:idp:error:invalidSubject'

class AuthorisationClass(Enum):
    CLIENT_CREDENTIALS = 'CLIENT_CREDENTIALS'

@define
class Authorisation:
    """
    """
    uuid: str
    is_class_of: AuthorisationClass
    state: str
    jwt: str
    sub: str
    azp: str
    exp: int
    model: authorisation.AuthorisationModel = field(default=None)
