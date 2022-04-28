from typing import Union
from cryptography.fernet import Fernet
from simple_memory_cache import GLOBAL_CACHE

from common.util import env, encoding_helpers

kek_cache = GLOBAL_CACHE.MemoryCachedVar('kek_cache')

"""
The KEK is the key used to enc all the other keys (public and symmetric) so that they can be stored in the Key store.
Dont use the KEK for anything but this purpose.


TODO: This key will come from AWS key management on initialisation.

For testing use the fixture "set_up_key_management" from tests.shared.key_management_helpers or call the setup directly using
tests.shared.key_management_helpers.set_up_key_management_env

"""

def kek():
    return kek_cache.get()

def invalidate_cache():
    kek.invalidate()
    pass

@kek_cache.on_first_access
def get_kek():
    return build_kek(env.Env.kek())

def build_kek(key_str: str):
    return Fernet(encoding_helpers.encode(key_str))

def create_kek():
    return encoding_helpers.decode(Fernet.generate_key())

def encrypt(data: str, as_str: bool = True) -> Union[bytes, str]:
    token = kek().encrypt(encoding_helpers.encode(data))
    if as_str:
        return encoding_helpers.decode(token)
    return token

def decrypt(token: str):
    data = kek().decrypt(encoding_helpers.encode(token))
    return encoding_helpers.decode(data)
