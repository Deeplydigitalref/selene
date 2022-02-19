import pytest
import os
from key_management.domain import key_management, kek

def it_creates_a_key_public_key_pair_encrypted_by_the_kek(new_kek):
    kid, encrypted_pair = key_management.create_exportable_public_key_pair()

    assert kid
    assert isinstance(encrypted_pair, str)

def it_decrypts_an_encrypted_key_pair(new_kek):
    kid, encrypted_pair = key_management.create_exportable_public_key_pair()

    decrypted_pair = key_management.decrypt_public_key_pair(encrypted_pair)

    assert decrypted_pair.kid == kid


@pytest.fixture
def new_kek():
    os.environ['KEK'] = kek.create_kek()
    pass