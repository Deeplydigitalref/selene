from pyfuncify import fn
import uuid
from enum import Enum

from . import public_key, kek
from ..repository import key_store

class KeyUse(Enum):
    sig = 1

def rotate_public_key_pair():
    kid, exportable_pair = create_exportable_public_key_pair()
    key_store.KeyStore().add_key(kid=kid, cyphertext=exportable_pair, alg= 'RSA', use=KeyUse.sig.name, state='active')
    return kid, exportable_pair

def get_key_by_use(use: KeyUse):
    stored_key = key_store.KeyStore().get_key_by_use(use.name)
    if not stored_key:
        return None
    return decrypt_public_key_pair(stored_key['cyphertext'])


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

#
# Helpers
#

def new_exportable_pair_fns():
    return [create_rsa_key_pair, public_key.export_pair_as_json, kek.encrypt]

def decrypt_exported_pair_fns():
    return [kek.decrypt, public_key.load_pair_from_json]

def assign_kid():
    return str(uuid.uuid4())

def create_rsa_key_pair(kid):
    return public_key.create_rsa_key_pair(kid=kid)
