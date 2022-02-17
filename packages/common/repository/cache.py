from pyfuncify import monad

from .. model import base_model
from common import error

cas_meta = "CAS#"
key_meta = "KEY#"

"""
The Cache is modelled as a PK with the cache name (provided as an argument)
and an SK of the cached key itself.  The value is the key value.

e.g. CAS#parameter_cache, KEY#BEARER_TOKEN, <value>

"""

@monad.monadic_try(name="create_cache_value", error_cls=error.ServiceError)
def write(cache_name: str, key: str, value: str):
    result = read(cache_name, key)
    if result.is_left():
        model = base_model.Cache(hash_key=format_cache_pk(cache_name),
                                 range_key=format_cache_sk(key),
                                 value=value)
        model.save()
        return model.value

    result.value.update(
        actions=[
            base_model.Cache.value.set(value)
        ]
    )
    return value

def read(cache_name, key):
    return find_item_by_key(cache_name, key)

@monad.monadic_try(name="find_cache_item_by_key", error_cls=error.DynamoError)
def find_item_by_key(cache_name, key):
    return base_model.Cache.get(format_cache_pk(cache_name), format_cache_sk(key))

def format_cache_pk(name: str):
    return "{}{}".format(cas_meta, name)

def format_cache_sk(key: str):
    return "{}{}".format(key_meta, key)
