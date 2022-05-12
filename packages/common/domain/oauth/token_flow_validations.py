from pyfuncify import monad

from common.domain.subject import subject, registration, value
from . import value as Val

def has_relying_party_validation(grant_tuple):
    grant, ctx = grant_tuple
    client_id = grant.get('client_id', None)
    azp, ctx = _rp_from_ctx(client_id, ctx)

    if azp.is_right():
        return monad.Right((grant, ctx))
    return monad.Left((Val.OauthErrors.INVALID_CLIENT,
            "Unknown Client ID: {}".format(client_id),
            Val.OauthTokenRecommendations.DO_NOT_GRANT))

def is_valid_client_credential(grant_tuple):
    grant, ctx = grant_tuple
    client_id = grant.get('client_id', None)
    azp, ctx = _rp_from_ctx(client_id, ctx)

    if subject.is_valid_secret(azp.value, grant['client_secret']):
        return monad.Right((grant, ctx))
    return (Val.OauthErrors.INVALID_CREDENTIALS,
            "Invalid Client Credentials: {}".format(client_id),
            Val.OauthTokenRecommendations.DO_NOT_GRANT)

def has_token_grant_type_validation(grant_tuple):
    grant, ctx = grant_tuple
    type = grant.get('grant_type', None)
    if type in ['client_credentials']:
        return monad.Right((grant, ctx))
    return (Val.OauthErrors.INVALID_GRANT_TYPE,
            "Invalid Grant Type: {}".format(type),
            Val.OauthTokenRecommendations.DO_NOT_GRANT)

def has_token_required_params_validation(grant_tuple):
    return monad.Right(grant_tuple)

def no_native_app_security_leak(grant_tuple):
    return monad.Right(grant_tuple)

def _rp_from_ctx(client_id, ctx):
    if ctx.get('azp', None):
        return ctx['azp'], ctx
    azp = subject.get(client_id, reify=(value.CredentialRegistration, registration.registrations_for_subject))
    ctx['azp'] = azp
    return azp, ctx