def jwk_key_set(rsa_key_pair):
    """
    Takes an RSA key pair and returns a JWKS containing the public key
    """
    priv, pub = jwk_rsa_keys(rsa_key_pair)
    return dict(keys=[json.loads(pub)])


def jwk_rsa_keys(pair) -> Tuple:
    """
    Returns a tuple of the priv and pub keys as a JSON encoded JWK
    """
    return pair.export_private(), pair.export_public()

