import pytest
import os

from key_management.domain import kek, key_management

@pytest.fixture
def set_up_key_management():
    os.environ['KEK'] = kek.create_kek()
    key_management.rotate_public_key_pair()
    key_management.rotate_symmetric_key()

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

