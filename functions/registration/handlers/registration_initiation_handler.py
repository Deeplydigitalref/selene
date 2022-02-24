import uuid
from typing import Dict
from pymonad.tools import curry

from pyfuncify import fn, monad, logger, app

from common.typing.custom_types import Either
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

def handle(request: app.RequestEvent) -> Either:
    _CTX['tracer'] = request.tracer

    result = generate_registration_options(request) >> to_result
    return result

def generate_registration_options(request) -> Either[app.RequestEvent]:
    result = command.authn_registration.invoke(request.event)
    if result.is_right():
        request.event.web_session = result.value.registration_session
        request.response = monad.Right(serialisers.WebAuthnSerialiser(result.value))
    else:
        breakpoint()
    return monad.Right(request)


def to_result(request) -> Either[app.RequestEvent]:
    return monad.Right(request)

#
# Helpers
#
