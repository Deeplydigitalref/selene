from typing import Union
from cryptography.fernet import Fernet
from simple_memory_cache import GLOBAL_CACHE

from common.util import env, encoding_helpers

kek_cache = GLOBAL_CACHE.MemoryCachedVar('kek_cache')

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
