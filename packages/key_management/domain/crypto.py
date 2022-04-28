from typing import Dict, Union
import secrets
import json

from . import sym_enc
from common.util import encoding_helpers

def generate_challenge(length: int = 64, base64_encoded: bool=False) -> Union[str, bytes]:
    """
    Generate a random authenticator challenge (which is in bytes) and converts is to a base64 encoded str
    """
    if base64_encoded:
        return encoding_helpers.bytes_to_base64url(secrets.token_bytes(length))
    return secrets.token_bytes(length)

def generate_random_secret_url_safe():
    return secrets.token_urlsafe()

def generate_secure_cookie(tokens: Dict) -> bytes:
    return sym_enc.encrypt(serialise_token(tokens))

def decrypt_secure_cookie(cookie: bytes) -> Dict:
    return deserialise_token(sym_enc.decrypt(cookie))

def serialise_token(tokens: Dict) -> str:
    return json.dumps(tokens)

def deserialise_token(serialised_tokens: str) -> Dict:
    return json.loads(serialised_tokens)
