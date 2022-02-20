import pytest
import os

from key_management.domain import kek

@pytest.fixture
def new_kek():
    os.environ['KEK'] = kek.create_kek()
    pass