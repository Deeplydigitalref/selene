from base64 import urlsafe_b64decode, urlsafe_b64encode

def base64url_to_bytes(val: str) -> bytes:
    """
    Convert a Base64URL-encoded string to bytes.
    """
    # Padding is optional in Base64URL. Unfortunately, Python's decoder requires the
    # padding. Given the fact that urlsafe_b64decode will ignore too _much_ padding,
    # we can tack on a constant amount of padding to ensure encoded values can always be
    # decoded.
    return urlsafe_b64decode(f"{val}===")

def bytes_to_base64url(val: bytes) -> str:
    """
    Base64URL-encode the provided bytes
    """
    return urlsafe_b64encode(val).decode("utf-8").replace("=", "")