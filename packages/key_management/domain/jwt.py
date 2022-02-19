from jwcrypto import jwt

def generate_signed_jwt(rsa_private_key):
    """
    Generates an RSA signed JWT is serialised form
    """
    return jwt.encode(jwt_claims(), rsa_private_key, algorithm="RS256")


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

def jwt_claims():
    return dict(iss="https://jarden-uat.au.auth0.com/",
                sub="1@clients",
                aud="https://api.jarden.io",
                iat=int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])),
                exp=(int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])) + (60*60*24)),
                azp="CJ5HhFu2H303aKMukkW9SDhJS1mQVzVD",
                gty="client-credentials")
