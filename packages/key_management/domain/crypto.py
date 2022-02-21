from typing import Dict
import secrets
import json

from . import sym_enc

def generate_challenge(length: int = 64) -> bytes:
    """
    Generate a random authenticator challenge
    """
    return secrets.token_bytes(length)


def generate_secure_cookie(tokens: Dict) -> bytes:
    return sym_enc.encrypt(serialise_token(tokens))

def validate_secure_cookie(cookie: bytes) -> Dict:
    return deserialise_token(sym_enc.decrypt(cookie))

def serialise_token(tokens: Dict) -> str:
    return json.dumps(tokens)

def deserialise_token(serialised_tokens: str) -> Dict:
    return json.loads(serialised_tokens)
