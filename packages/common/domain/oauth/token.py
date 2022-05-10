from typing import Dict, Tuple
from pyfuncify import fn, monad

from . import token_flow_validations as V
from . import authorisers, value

granters = {
        "client_credentials": authorisers.client_credentials_authoriser
    }

"""
Implements the Oauth Token Grant Flow.

The Token flow is provided for both the client credentials grant and the authorisation clode grant flow (the second step)
"""

def token_grant(grant_request: Dict) -> monad.EitherMonad[value.Authorisation]:
    result = (_validate((grant_request, {})) >> _grant_access)

    return result


#
# commands
#
def _validate(grant_tuple: Tuple[Dict, Dict]) -> monad.EitherMonad[Tuple[Dict, Dict]]:
    results = fn.either_compose(_validators(), monad.Right(grant_tuple))
    return results

def _grant_access(grant_tuple) -> monad.EitherMonad[value.Authorisation]:
    """
    + For a client credentials grant is grants a token to the AZP for itself.

    """
    return _access_granters(grant_tuple[0].get('grant_type', None))(grant_tuple)


#
#Helpers
#
def _validators():
    return [V.has_relying_party_validation,
            V.is_valid_client_credential,
            V.has_token_grant_type_validation,
            V.has_token_required_params_validation,
            V.no_native_app_security_leak]

def _access_granters(grant_type):
    return granters.get(grant_type, None)