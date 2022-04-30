from key_management.domain import sym_enc, crypto

def test_encrypt_and_decrypt_with_enc_key(new_kek,
                                          rotate_enc_key):

    cypher_text = sym_enc.encrypt("hello")

    decrypted_text = sym_enc.decrypt(cypher_text)

    assert decrypted_text == "hello"

def it_encrypts_using_a_jwk(new_kek,
                            rotate_enc_jwk):

    secret = crypto.generate_random_secret_url_safe()
    jwk_cypher_text = sym_enc.jwe_encrypt(secret)

    decrypted_secret = sym_enc.jwe_decrypt(jwk_cypher_text)

    assert decrypted_secret == secret