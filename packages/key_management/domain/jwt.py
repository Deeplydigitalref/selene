from jwcrypto.common import json_decode
from jwcrypto.jwe import JWE
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT
from jwcrypto.jwk import JWK
from pymonad.tools import curry
from pyfuncify import fn, app, monad
from attrs import define, field

from . import key_management

class TokenError(app.AppError):
    pass

@define
class JwtPipline():
    signing_key: JWK
    claims: dict = field(default=None)
    jwt: JWT = field(default=None)
    token: str = field(default=None)


def generate_signed_jwt(claims: dict):
    """
    Generates an RSA signed JWT is serialised form
    """
    result = fn.compose_iter([jwt_pipeline_builder(current_sig_key()), generate_jwt, sign, serialise], claims)
    return result.token

@monad.monadic_try()
def decode_and_validate(encoded_jwt: str) -> dict:
    token = JWT(jwt=encoded_jwt)
    jwt = token.token

    signing_key = key_management.get_key_by_kid(kid=jwt.jose_header['kid'])

    if not isinstance(jwt, JWS) or not signing_key:
        breakpoint()

    jwt.verify(signing_key)
    return json_decode(jwt.payload)

#
# Helper Functions
#

@curry(2)
def jwt_pipeline_builder(signing_key: JWK, claims: dict):
    return JwtPipline(signing_key=signing_key, claims=claims)

def current_sig_key():
    # TODO: where to assume caching
    return key_management.get_key_by_use(key_management.KeyUse.sig)

def jse_decrypt():
    token = jtok.token
    if isinstance(token, JWE):
        token.decrypt(self.kkstore.server_keys[KEY_USAGE_ENC])
        # If an encrypted payload is received then there must be
        # a nested signed payload to verify the provenance.
        payload = token.payload.decode('utf-8')
        token = JWS()
        token.deserialize(payload)
    elif isinstance(token, JWS):
        pass
    else:
        raise TypeError("Invalid Token type: %s" % type(jtok))


def generate_jwt(value: JwtPipline) -> JwtPipline:
    value.jwt = JWT({'kid': value.signing_key.kid, 'alg': 'RS256', 'kty': key_management.KeyUse.sig.name}, value.claims)
    return value


def sign(value: JwtPipline) -> JwtPipline:
    value.jwt.make_signed_token(value.signing_key)
    return value

def serialise(value: JwtPipline) -> JwtPipline:
    value.token = value.jwt.serialize()
    return value

# def generate_expired_signed_jwt():
#     """
#     Generates an RSA signed JWT is serialised form which is expired
#     """
#     return jwt.encode(jwt_claims_expired(), rsa_private_key(), algorithm="RS256")


def generate_valid_signed_jwt():
    return generate_signed_jwt(rsa_private_key())


def jwt_claims_expired():
    claims = jwt_claims()
    claims['exp'] = (int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])) - (60*60))
    return claims
