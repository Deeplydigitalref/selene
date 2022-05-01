from typing import Dict
from pyfuncify import fn, monad

from . import token_flow_validations as V

"""
Implements the Oauth Token Grant Flow.

The Token flow is provided for both the client credentials grant and the authorisation clode grant flow (the second step)
"""

def token_grant(grant_request: Dict) -> monad.EitherMonad:
    result = (_validate((grant_request, {})) >> grant_access >> generate_id_token)
    breakpoint()


#
# commands
#
def _validate(grant_tuple: Dict) -> monad.EitherMonad[Dict]:
    results = fn.either_compose(_validators(), monad.Right(grant_tuple))
    return results

def grant_access(grant_tuple):
    """
    + For a client credentials grant is grants a token to the AZP for itself.

    """
    breakpoint()
    pass


def generate_id_token():
    pass
#
#Helpers
#
def _validators():
    return [V.has_relying_party_validation,
            V.is_valid_client_credential,
            V.has_token_grant_type_validation,
            V.has_token_required_params_validation,
            V.no_native_app_security_leak]
