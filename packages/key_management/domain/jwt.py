from jwcrypto import jwt, jwk

def generate_signed_jwt(rsa_private_key: jwk.JWK, claims: dict):
    """
    Generates an RSA signed JWT is serialised form
    """
    token = jwt.JWT({'kid': rsa_private_key.kid, 'alg': 'RS256'}, claims)
    token.make_signed_token(rsa_private_key)
    return token.serialize()

def generate_expired_signed_jwt():
    """
    Generates an RSA signed JWT is serialised form which is expired
    """
    return jwt.encode(jwt_claims_expired(), rsa_private_key(), algorithm="RS256")


def generate_valid_signed_jwt():
    return generate_signed_jwt(rsa_private_key())


def jwt_claims_expired():
    claims = jwt_claims()
    claims['exp'] = (int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])) - (60*60))
    return claims
