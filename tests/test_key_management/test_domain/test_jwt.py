import pytest
from pyfuncify import chronos

from key_management.domain import jwt, public_key

def it_generates_a_jwt(rsa_key_pair,
                       id_token_claims):

    signed_jwt = jwt.generate_signed_jwt(rsa_key_pair, id_token_claims)

    assert len(signed_jwt.split(".")) == 3


@pytest.fixture
def rsa_key_pair():
    return public_key.create_rsa_key_pair(kid="1")

@pytest.fixture
def id_token_claims():
    return dict(iss="https://selene.reference.io",
                sub="1@selene",
                aud="https://api.reference.io",
                iat=int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])),
                exp=(int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])) + (60*60*24)),
                azp="CJ5HhFu2H303aKMukkW9SDhJS1mQVzVD",
                gty="client-credentials")
