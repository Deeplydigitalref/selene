import pytest
import json

"""
Server Response to Initiation Request...

From test...
{"rp": {"name": "Example Co", "id": "example.com"}, "user": {"id": "c3ViamVjdDE", "name": "subject1", "displayName": "subject1"}, "challenge": "JdLI_1i6vTVTcGlOyJAVz0jwONfMZjaRPIOTQZXd2fptxJ4IAIQ84aREpTu_HyxBxr1RDqA_SKXaFKpSFkZytQ", "pubKeyCredParams": [{"type": "public-key", "alg": -36}], "timeout": 12000, "excludeCredentials": [{"id": "JdLI_1i6vTVTcGlOyJAVz0jwONfMZjaRPIOTQZXd2fptxJ4IAIQ84aREpTu_HyxBxr1RDqA_SKXaFKpSFkZytQ", "type": "public-key"}], "authenticatorSelection": {"authenticatorAttachment": "platform", "residentKey": "required", "requireResidentKey": true, "userVerification": "preferred"}, "attestation": "direct"}

From WebAuthn.io
{
  "publicKey": {
    "challenge": "n1medBqeuBlrIlbhsZ8mKXyTEsj6GLxllQcd4Kwgm0Y=",
    "rp": {
      "name": "webauthn.io",
      "id": "webauthn.io"
    },
    "user": {
      "name": "fauve",
      "displayName": "fauve",
      "id": "kYoSAAAAAAAAAA=="
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

Decoding the Registration from the Client (see completion below):

import webauthn.helpers as h
from common.util import encoding_helpers

# The clientDataJSON is base64 encoded
collection = h.parse_client_data_json(encoding_helpers.base64url_to_bytes(completion['response']['clientDataJSON))
# CollectedClientData(type=<ClientDataType.WEBAUTHN_CREATE: 'webauthn.create'>, challenge=b'\x9fY\x9et\x1a\x9e\xb8\x19k"V\xe1\xb1\x9f&)|\x93\x12\xc8\xfa\x18\xbce\x95\x07\x1d\xe0\xac \x9bF', origin='https://webauthn.io', cross_origin=False, token_binding=None)

# Then to get back to the base64 encoded challenge set on the initiation, we bytes_to_base64url it
encoding_helpers.bytes_to_base64url(collection.challenge)

Same with the Attestation Object...
h.parse_attestation_object(encoding_helpers.base64url_to_bytes(completion['response']['attestationObject))

Public Key:
pk = h.decode_credential_public_key(ato.auth_data.attested_credential_data.credential_public_key)
 
"""

def registration_completion_internal():
    req = {"id": "AfZnlyjVTfl8NEktDlA3IpdgEHxfVxNjV4EYIb9xYEqo7g_Mr5pIqVA7wNf-PmfZWWSE6XGi",
           "rawId": "AfZnlyjVTfl8NEktDlA3IpdgEHxfVxNjV4EYIb9xYEqo7g_Mr5pIqVA7wNf-PmfZWWSE6XGi",
           "type": "public-key",
           "response": {
               "attestationObject": "o2NmbXRmcGFja2VkZ2F0dFN0bXSiY2FsZyZjc2lnWEcwRQIgTLNB9Do4Bzm48PQW8T-jMa9r39eDQyqQclxRihBkld8CIQCw1e58KUTILSLx6e4kDTncdfVhNP9qsticyf1bLzsjRGhhdXRoRGF0YVi6dKbqkhPJnC90siSSsyDPQCYqlMGpUKA5fyklC2CEHvBFYhNAga3OAAI1vMYKZIsLJfHwVQMANgH2Z5co1U35fDRJLQ5QNyKXYBB8X1cTY1eBGCG_cWBKqO4PzK-aSKlQO8DX_j5n2VlkhOlxoqUBAgMmIAEhWCBgZ9PW_N8THx4xpxR--Hea4Jz3tvUT0IfBeeYibdUpSyJYIIs__AX-9NIvqsDh3UE_8Ks4heVTdeeJgLTgudwyRfVA",
               "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoibjFtZWRCcWV1QmxySWxiaHNaOG1LWHlURXNqNkdMeGxsUWNkNEt3Z20wWSIsIm9yaWdpbiI6Imh0dHBzOi8vd2ViYXV0aG4uaW8iLCJjcm9zc09yaWdpbiI6ZmFsc2UsIm90aGVyX2tleXNfY2FuX2JlX2FkZGVkX2hlcmUiOiJkbyBub3QgY29tcGFyZSBjbGllbnREYXRhSlNPTiBhZ2FpbnN0IGEgdGVtcGxhdGUuIFNlZSBodHRwczovL2dvby5nbC95YWJQZXgifQ"}
           }
    return json.dumps(req)

def registration_completion_usb():
        reg = {
            "id": "9y1xA8Tmg1FEmT-c7_fvWZ_uoTuoih3OvR45_oAK-cwHWhAbXrl2q62iLVTjiyEZ7O7n-CROOY494k7Q3xrs_w",
            "rawId": "9y1xA8Tmg1FEmT-c7_fvWZ_uoTuoih3OvR45_oAK-cwHWhAbXrl2q62iLVTjiyEZ7O7n-CROOY494k7Q3xrs_w",
            "response": {
                "attestationObject": "o2NmbXRkbm9uZWdhdHRTdG10oGhhdXRoRGF0YVjESZYN5YgOjGh0NBcPZHZgW4_krrmihjLHmVzzuoMdl2NFAAAAFwAAAAAAAAAAAAAAAAAAAAAAQPctcQPE5oNRRJk_nO_371mf7qE7qIodzr0eOf6ACvnMB1oQG165dqutoi1U44shGezu5_gkTjmOPeJO0N8a7P-lAQIDJiABIVggSFbUJF-42Ug3pdM8rDRFu_N5oiVEysPDB6n66r_7dZAiWCDUVnB39FlGypL-qAoIO9xWHtJygo2jfDmHl-_eKFRLDA",
                "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoiVHdON240V1R5R0tMYzRaWS1xR3NGcUtuSE00bmdscXN5VjBJQ0psTjJUTzlYaVJ5RnRya2FEd1V2c3FsLWdrTEpYUDZmbkYxTWxyWjUzTW00UjdDdnciLCJvcmlnaW4iOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJjcm9zc09yaWdpbiI6ZmFsc2V9"
            },
            "type": "public-key",
            "clientExtensionResults": {},
            "transports": [
                "nfc",
                "usb"
            ]
        }

        base64_challenge = "TwN7n4WTyGKLc4ZY-qGsFqKnHM4nglqsyV0ICJlN2TO9XiRyFtrkaDwUvsql-gkLJXP6fnF1MlrZ53Mm4R7Cvw"

        return base64_challenge, json.dumps(reg)