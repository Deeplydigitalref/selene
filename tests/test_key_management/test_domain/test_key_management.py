import pytest
import os
from key_management.domain import key_management, sym_enc
from key_management.repository import key_store

def it_creates_a_key_public_key_pair_encrypted_by_the_kek(new_kek):
    kid, encrypted_pair = key_management.create_exportable_public_key_pair()

    assert kid
    assert isinstance(encrypted_pair, str)

def it_decrypts_an_encrypted_key_pair(new_kek):
    kid, encrypted_pair = key_management.create_exportable_public_key_pair()

    decrypted_pair = key_management.decrypt_public_key_pair(encrypted_pair)

    assert decrypted_pair.kid == kid


def it_persists_a_new_active_sig_key(new_kek):
    kid, encrypted_pair = key_management.rotate_public_key_pair()

    stored_key = key_store.KeyStore().get_key_by_kid(kid)

    assert stored_key
    assert stored_key['cyphertext'] == encrypted_pair

def it_gets_a_key_by_kid(new_kek):
    from jwcrypto.jwk import JWK

    kid, encrypted_pair = key_management.rotate_public_key_pair()
    key_store.KeyStore().get_key_by_kid(kid)

    key = key_management.get_key_by_kid(kid)

    assert isinstance(key, JWK)

def it_gets_the_current_public_key_pair(new_kek):
    from jwcrypto.jwk import JWK

    kid, encrypted_pair = key_management.rotate_public_key_pair()

    key = key_management.get_key_by_use(key_management.KeyUse.sig)

    assert isinstance(key, JWK)


def it_creates_a_symmetric_key(new_kek):
    kid, key = key_management.rotate_symmetric_key()

    found_key = key_management.get_key_by_use(key_management.KeyUse.enc)

    assert found_key._signing_key == key_management.decrypt_sym_key(key)._signing_key

