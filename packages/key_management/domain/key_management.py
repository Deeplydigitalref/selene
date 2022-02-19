from pyfuncify import fn
import uuid

from common.util import env
from . import public_key, kek

def create_exportable_public_key_pair():
    kid = assign_kid()
    exportable_pair = fn.compose_iter(new_exportable_pair_fns(), kid)
    return kid, exportable_pair

def decrypt_public_key_pair(serialised_pair):
    return fn.compose_iter(decrypt_exported_pair_fns(), serialised_pair)

def new_exportable_pair_fns():
    return [create_rsa_key_pair, public_key.export_pair_as_json, kek.encrypt]

def decrypt_exported_pair_fns():
    return [kek.decrypt, public_key.load_pair_from_json]

def assign_kid():
    return str(uuid.uuid4())

def create_rsa_key_pair(kid):
    return public_key.create_rsa_key_pair(kid=kid)
