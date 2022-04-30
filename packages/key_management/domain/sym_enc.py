from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode

from common.util import encoding_helpers
from . import key_management

def encrypt(data: str) -> str:
    key = _get_enc_key()
    return encoding_helpers.decode(key.encrypt(encoding_helpers.encode(data)))

def decrypt(cypher_text: str) -> str:
    key = _get_enc_key()
    return  encoding_helpers.decode(key.decrypt(encoding_helpers.encode(cypher_text)))

def jwe_encrypt(data: str) -> str:
    """
    Generates a JWE encoded str
    The advantage of JWE is that the json encoded str contains the KID (and ALG/ENC) allowing cypher text to be stored
    across key rotations.

    Use this technique for long lived cypher text, such as client secrets.
    """
    key = _get_enc_jwk()
    jwetoken = jwe.JWE(encoding_helpers.encode(data),
                       json_encode({"kid": key.kid,
                                    "alg": "A256KW",
                                    "enc": "A256CBC-HS512"}))
    jwetoken.add_recipient(key)
    return jwetoken.serialize()

def jwe_decrypt(cypher_text):
    jwetoken = jwe.JWE()
    jwetoken.deserialize(cypher_text)
    key = _get_enc_jwk_by_kid(jwetoken.jose_header['kid'])
    jwetoken.decrypt(key)
    return encoding_helpers.decode(jwetoken.payload)

#
# Helpers
#
def _get_enc_key():
    return key_management.get_key_by_use(key_management.KeyUse.enc)


def _get_enc_jwk():
    return key_management.get_key_by_use(key_management.KeyUse.jwtenc)

def _get_enc_jwk_by_kid(kid: str) -> jwk.JWK:
    return key_management.get_key_by_kid(kid)
