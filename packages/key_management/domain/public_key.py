from typing import Tuple
from jwcrypto import jwk
import json

def create_rsa_key_pair(kid):
    """
    Args:
        kid: a unique id for the key

    Returns:
        JWK pub/priv key pair with a KID
    """
    return jwk.JWK.generate(kty='RSA', size=2048, kid=kid)


def export_pair_as_json(pair):
    return pair.export()


def load_pair_from_json(json_pair: str) -> jwk.JWK:
    return jwk.JWK(**json.loads(json_pair))
