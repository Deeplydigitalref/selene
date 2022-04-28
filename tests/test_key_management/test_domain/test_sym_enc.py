from key_management.domain import sym_enc

def test_encrypt_and_decrypt_with_enc_key(new_kek,
                                          rotate_enc_key):

    cypher_text = sym_enc.encrypt("hello")

    decrypted_text = sym_enc.decrypt(cypher_text)

    assert decrypted_text == "hello"