import pytest
from pyfuncify import chronos

from key_management.domain import jwt, public_key

def it_generates_a_jwt(rsa_key_pair,
                       id_token_claims):

    signed_jwt = jwt.generate_signed_jwt(rsa_key_pair, id_token_claims)

    assert len(signed_jwt.split(".")) == 3


def it_validates_the_jwt(rsa_key_pair,
                         id_token_claims):
    signed_jwt = jwt.generate_signed_jwt(rsa_key_pair, id_token_claims)

    id_token = jwt.decode_and_validate(rsa_key_pair, signed_jwt)

    assert id_token.is_right()
    assert id_token.value['sub'] == '1@selene'

def it_fails_when_the_token_is_invalid(rsa_key_pair):
    t = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.NHVaYe26MbtOYhSKkoKYdFVomg4i8ZJd8_-RU8VNbftc4TSMb4bXP3l3YlNWACwyXPGffz5aXHc6lty1Y2t4SWRqGteragsVdZufDn5BlnJl9pdR_kdVFUsra2rWKEofkZeIC4yWytE58sMIihvo9H1ScmmVwBcQP6XETqYd0aSHp1gOa9RdUPDvoXQ5oqygTqVtxaDr6wUFKrKItgBMzWIdNZ6y7O9E0DhEPTbE9rfBo6KTFsHAZnMg4k68CDp2woYIaXbmYTWcvbzIuHO7_37GT79XdIwkm95QJ7hYC9RiwrV7mesbY4PAahERJawntho0my942XheVLmGwLMBkQ"
    id_token = jwt.decode_and_validate(rsa_key_pair, t)

    assert id_token.is_left()



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
                azp="client-id-1",
                gty="client-credentials")
