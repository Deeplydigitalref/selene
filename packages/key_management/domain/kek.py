from typing import Union
from cryptography.fernet import Fernet
from simple_memory_cache import GLOBAL_CACHE

from common.util import env

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
    return Fernet(encode(key_str))

def create_kek():
    return Fernet.generate_key().decode('utf-8')

def encrypt(data: str, as_str: bool = True) -> Union[bytes, str]:
    token = kek().encrypt(encode(data))
    if as_str:
        return decode(token)
    return token

def decrypt(token: str):
    data = kek().decrypt(encode(token))
    return decode(data)

def decode(by: bytes) -> str:
    return by.decode('utf-8')

def encode(st: str) -> bytes:
    return st.encode('utf-8')
