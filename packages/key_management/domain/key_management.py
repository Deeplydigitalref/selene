from pyfuncify import fn
from cryptography.fernet import Fernet
import uuid
from enum import Enum

from common.util import encoding_helpers

from . import public_key, kek
from ..repository import key_store

class KeyUse(Enum):
    sig = 1
    enc = 2

def rotate_public_key_pair():
    kid, exportable_pair = create_exportable_public_key_pair()
    key_store.KeyStore().add_key(kid=kid, cyphertext=exportable_pair, alg= 'RSA', use=KeyUse.sig.name, state='active')
    return kid, exportable_pair

def rotate_symmetric_key():
    kid, exportable_key = create_exportable_symmetric_key()
    key_store.KeyStore().add_key(kid=kid, cyphertext=exportable_key, alg='ASE-CBC-128-HMAC-SHA256', use=KeyUse.enc.name, state='active')
    return kid, exportable_key

def get_key_by_use(use: KeyUse):
    stored_key = key_store.KeyStore().get_key_by_use(use.name)
    if not stored_key:
        return None
    if use == KeyUse.sig:
        return decrypt_public_key_pair(stored_key['cyphertext'])
    return decrypt_sym_key(stored_key['cyphertext'])


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

def create_exportable_symmetric_key():
    kid = assign_kid()
    key = fn.compose_iter(new_exportable_sym_key_fns(), kid)
    return kid, key


#
# Helpers
#

def new_exportable_pair_fns():
    return [create_rsa_key_pair, public_key.export_pair_as_json, kek.encrypt]

def new_exportable_sym_key_fns():
    return [create_sym_key, encoding_helpers.decode, kek.encrypt]

def decrypt_exported_pair_fns():
    return [kek.decrypt, public_key.load_pair_from_json]

def decrypt_exported_sym_key_fns():
    return [kek.decrypt, to_fernet_key]

def to_fernet_key(key):
    return Fernet(encoding_helpers.encode(key))

def assign_kid():
    return str(uuid.uuid4())

def create_rsa_key_pair(kid):
    return public_key.create_rsa_key_pair(kid=kid)

def create_sym_key(_kid):
    return Fernet.generate_key()
