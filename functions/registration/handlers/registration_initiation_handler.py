import uuid
from typing import Dict
from pyfuncify import monad, app

from common.util import serialisers

from .. import command


_CTX = {}

instrumentables = []

"""
Registration Request initiates the WebAuthn flow, providing a subject name as the only parameter

The example from webauthn.io allows config of the biometric auth type 

https://webauthn.io/makeCredential/fauve2?attType=direct&authType=platform&userVerification=discouraged&residentKeyRequirement=false&txAuthExtension=
Request Method: GET

Respond with a cookie and the generated webauthn registration parameters:

{
  "publicKey": {
    "challenge": "3UkLCUlNg3YFYk2I93YrDnlIIZ6M7ZfR6EEHLCmvJvU=",
    "rp": {
      "name": "webauthn.io",
      "id": "webauthn.io"
    },
    "user": {
      "name": "fauve2",
      "displayName": "fauve2",
      "id": "gu8RAAAAAAAAAA=="
    },
    "pubKeyCredParams": [
      {
        "type": "public-key",
        "alg": -7
      },
      {
        "type": "public-key",
        "alg": -35
      },
      {
        "type": "public-key",
        "alg": -36
      },
      {
        "type": "public-key",
        "alg": -257
      },
      {
        "type": "public-key",
        "alg": -258
      },
      {
        "type": "public-key",
        "alg": -259
      },
      {
        "type": "public-key",
        "alg": -37
      },
      {
        "type": "public-key",
        "alg": -38
      },
      {
        "type": "public-key",
        "alg": -39
      },
      {
        "type": "public-key",
        "alg": -8
      }
    ],
    "authenticatorSelection": {
      "authenticatorAttachment": "platform",
      "requireResidentKey": false,
      "userVerification": "discouraged"
    },
    "timeout": 60000,
    "extensions": {
      "txAuthSimple": ""
    },
    "attestation": "direct"
  }
} 

"""

def handle(request: app.RequestEvent) -> monad.EitherMonad:
    _CTX['tracer'] = request.tracer

    result = generate_registration_options(request) >> session_and_response
    return result

def generate_registration_options(request: app.RequestEvent) -> monad.EitherMonad[app.RequestEvent]:
    """
    Creates a new authn registration request.  Returning the registration domain value into the results value.

    :param request:
    :return: monad.EitherMonad[request]
    """
    result = command.authn_registration_initiate.invoke(request.event)
    if result.is_right():
        request.results = result.value
    else:
        breakpoint()
    return monad.Right(request)


def session_and_response(request: app.RequestEvent) -> monad.EitherMonad[app.RequestEvent]:
    """
    The registration session is set in the domain value.  This is copied to the request value as the new
    web session to be set, and the WebAuthnRegistrationSerialiser is injected to enable the response body creation
    from the registration.

    :param request:
    :return: monad.EitherMonad[request]
    """
    request.event.web_session = request.results.registration_session
    request.response = monad.Right(serialisers.WebAuthnRegistrationSerialiser(request.results))
    return monad.Right(request)

#
# Helpers
#
