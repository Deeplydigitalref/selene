import pytest
import os

from key_management.domain import kek, key_management


@pytest.fixture
def set_up_key_management():
    set_up_key_management_env()

def set_up_key_management_env():
    """
    + Adds a new KEK into the env.  This will be picked up by the env initialisers.
    + New public, symmetric, and JWK key are created (via rotating), are encrypted using the KEK and added to the keystore.
    """
    os.environ['KEK'] = kek.create_kek()  # this will then be used on env setup
    key_management.rotate_public_key_pair()
    key_management.rotate_symmetric_key()
    key_management.rotate_symmetric_jwk()



@pytest.fixture
def new_kek():
    os.environ['KEK'] = kek.create_kek()
    pass

@pytest.fixture
def rotate_sig_key_pair():
    key_management.rotate_public_key_pair()
    pass


@pytest.fixture
def rotate_enc_key():
    key_management.rotate_symmetric_key()
    pass


@pytest.fixture
def rotate_enc_jwk():
    key_management.rotate_symmetric_jwk()
    pass
