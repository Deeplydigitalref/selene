from enum import Enum

class OauthTokenRecommendations(Enum):
    DO_NOT_GRANT = 'urn:idp:recommendation:doNotGrant'

class OauthErrors(Enum):
    INVALID_CLIENT = 'urn:idp:error:invalid_client'
    INVALID_CREDENTIALS = 'urn:idp:error:invalid_client_credentials'