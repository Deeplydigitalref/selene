from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode


key = jwk.JWK.generate(kty='oct', size=256)
payload = "My Encrypted message"
jwetoken = jwe.JWE(payload.encode('utf-8'),
                       json_encode({"alg": "A256KW",
                                    "enc": "A256CBC-HS512"}))
jwetoken.add_recipient(key)
enc = jwetoken.serialize()