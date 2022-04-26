from key_management.domain import public_key

def it_generates_a_new_key_pair():
    pair = public_key.create_rsa_key_pair(kid="1")

    assert pair.kid == "1"

def it_exports_pair_to_json():
    exported_pair = public_key.export_pair_as_json(public_key.create_rsa_key_pair(kid="1"))

    assert '"kid":"1"' in exported_pair

def it_imports_key_from_json():
    exported_pair = public_key.export_pair_as_json(public_key.create_rsa_key_pair(kid="1"))

    imported_pair = public_key.load_pair_from_json(exported_pair)

    assert imported_pair.kid == "1"