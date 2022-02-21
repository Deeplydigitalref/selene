from . import key_management
from common.util import encoding_helpers

def encrypt(data: str) -> str:
    key = get_enc_key()
    return encoding_helpers.decode(key.encrypt(encoding_helpers.encode(data)))

def decrypt(cypher_text: str) -> str:
    key = get_enc_key()
    return  encoding_helpers.decode(key.decrypt(encoding_helpers.encode(cypher_text)))

def get_enc_key():
    return key_management.get_key_by_use(key_management.KeyUse.enc)

