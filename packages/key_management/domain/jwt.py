from jwcrypto.common import json_decode
from jwcrypto.jwe import JWE
from jwcrypto.jws import JWS
from jwcrypto.jwt import JWT
from jwcrypto.jwk import JWK
from pymonad.tools import curry
from pyfuncify import fn, app, monad

class TokenError(app.AppError):
    pass

def generate_signed_jwt(rsa_private_key: JWK, claims: dict):
    """
    Generates an RSA signed JWT is serialised form
    """
    return fn.compose_iter([generate_jwt(rsa_private_key.kid), sign(rsa_private_key), serialise], claims)

@monad.monadic_try()
def decode_and_validate(rsa_key_pair, encoded_jwt: str):
    jwt = JWT(jwt=encoded_jwt)
    token = jwt.token
    # token.jose_header => {'alg': 'RS256', 'kid': '1'}

    if not isinstance(token, JWS):
        breakpoint()

    token.verify(rsa_key_pair)
    return json_decode(token.payload)

#
# Helper Functions
#
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

@curry(2)
def generate_jwt(kid, claims):
    return JWT({'kid': kid, 'alg': 'RS256'}, claims)

@curry(2)
def sign(private_key, token):
    token.make_signed_token(private_key)
    return token

def serialise(token):
    return token.serialize()

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
