from typing import Dict
import secrets
from secure_cookie.cookie import SecureCookie

def generate_challenge(length: int = 64) -> bytes:
    """
    Generate a random authenticator challenge
    """
    return secrets.token_bytes(length)


def generate_secure_cookie(tokens: Dict) -> bytes:
    return SecureCookie(tokens, "cookie-signing-key").serialize()

def validate_secure_cookie(cookie: bytes) -> Dict:
    return SecureCookie.unserialize(cookie, "cookie-signing-key")