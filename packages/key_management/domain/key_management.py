import sys

from pyfuncify import fn
from cryptography.fernet import Fernet
from jwcrypto import jwk
import uuid
from enum import Enum

from common.util import encoding_helpers

from . import public_key, kek
from ..repository import key_store

class KeyUse(Enum):
    sig = 'SIG'
    enc = 'ENC'
    jwtenc = 'JWTENC'


def rotate_public_key_pair():
    kid, exportable_pair = create_exportable_public_key_pair()
    key_store.KeyStore().add_key(kid=kid, cyphertext=exportable_pair, alg= 'RSA', use=KeyUse.sig.name, state='active')
    return kid, exportable_pair

def rotate_symmetric_key():
    kid, exportable_key = create_exportable_symmetric_key()
    key_store.KeyStore().add_key(kid=kid, cyphertext=exportable_key, alg='ASE-CBC-128-HMAC-SHA256', use=KeyUse.enc.name, state='active')
    return kid, exportable_key

def rotate_symmetric_jwk():
    kid, exportable_key = create_exportable_symmetric_jwk()
    key_store.KeyStore().add_key(kid=kid, cyphertext=exportable_key, alg='oct', use=KeyUse.jwtenc.name,
                                 state='active')
    return kid, exportable_key

def get_key_by_use(use: KeyUse):
    stored_key = key_store.KeyStore().get_key_by_use(use.name)
    if not stored_key:
        return None
    return getattr(sys.modules[__name__], "decrypt_{}".format(use.value.lower()))(stored_key['cyphertext'])

def decrypt_sig(cyphertext):
    return decrypt_public_key_pair(cyphertext)

def decrypt_enc(cyphertext):
    return decrypt_sym_key(cyphertext)

def decrypt_jwtenc(cyphertext):
    return decrypt_sym_jwk(cyphertext)

def get_key_by_kid(kid):
    stored_key = key_store.KeyStore().get_key_by_kid(kid)
    if not stored_key:
        return None
    return decrypt_public_key_pair(stored_key['cyphertext'])

def create_exportable_public_key_pair():
    kid = assign_kid()
    exportable_pair = fn.compose_iter(new_exportable_pair_fns(), kid)
    return kid, exportable_pair

def decrypt_public_key_pair(serialised_pair):
    return fn.compose_iter(decrypt_exported_pair_fns(), serialised_pair)

def decrypt_sym_key(serialised_key):
    return fn.compose_iter(decrypt_exported_sym_key_fns(), serialised_key)

def decrypt_sym_jwk(serialised_jwk):
    return fn.compose_iter(decrypt_exported_sym_jwk_fns(), serialised_jwk)


def create_exportable_symmetric_key():
    kid = assign_kid()
    key = fn.compose_iter(new_exportable_sym_key_fns(), kid)
    return kid, key

def create_exportable_symmetric_jwk():
    kid = assign_kid()
    key = fn.compose_iter(new_exportable_sym_jwk_fns(), kid)
    return kid, key

#
# Helpers
#

def new_exportable_pair_fns():
    return [create_rsa_key_pair, public_key.export_pair_as_json, kek.encrypt]

def new_exportable_sym_key_fns():
    return [create_sym_key, encoding_helpers.decode, kek.encrypt]

def new_exportable_sym_jwk_fns():
    """
    Create a JWK type symmetric key
    """
    return [create_sym_jwk, jwk_export, kek.encrypt]


def decrypt_exported_pair_fns():
    return [kek.decrypt, public_key.load_pair_from_json]

def decrypt_exported_sym_key_fns():
    return [kek.decrypt, to_fernet_key]

def decrypt_exported_sym_jwk_fns():
    return [kek.decrypt, to_jwk]


def to_fernet_key(key):
    return Fernet(encoding_helpers.encode(key))

def to_jwk(key):
    return jwk.JWK().from_json(key)

def assign_kid():
    return str(uuid.uuid4())

def create_rsa_key_pair(kid):
    return public_key.create_rsa_key_pair(kid=kid)

def create_sym_key(_kid):
    return Fernet.generate_key()

def create_sym_jwk(kid):
    return jwk.JWK.generate(kid=kid, kty='oct', size=256)

def jwk_export(key):
    return key.export()