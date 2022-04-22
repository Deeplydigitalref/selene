from typing import Dict
from common.domain import constants
from pyfuncify import monad
from webauthn.helpers import structs
from common.domain import webauthn_helpers
from common.repository import webauthn_registration
from common.util import env
from . import value

def registration_obligations(registration: value.Registration) -> value.Registration:
    opts = webauthn_helpers.generate_options(rp_id=env.Env.relying_party_id(),
                                             rp_name=env.Env.relying_party_name(),
                                             subject_name=registration.subject_name)
    registration.registration_options = opts
    return monad.Right(registration)

def regenerate_opts(model: webauthn_registration.RegistrationModel) -> structs.PublicKeyCredentialCreationOptions:
    return webauthn_helpers.generate(rp_id=env.Env.relying_party_id(),
                                     rp_name=env.Env.relying_party_name(),
                                     user_id=model.subject_name,
                                     user_name=model.subject_name,
                                     user_display_name=model.subject_name,
                                     challenge=model.registration_challenge)

def validate_registration(challenge_response: Dict, registration: value.Registration):
    return webauthn_helpers.reg_verify(credential=webauthn_helpers.reg_credential(challenge_response),
                                       challenge=registration.registration_options.challenge,
                                       expected_origin=env.Env.relying_party_name(),
                                       expected_rp_id=env.Env.relying_party_id(),
                                       require_user_verification=True)


# Registration Response Verification
# registration_verification = verify_registration_response(
#     credential=RegistrationCredential.parse_raw(
#         """{
#         "id": "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s",
#         "rawId": "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s",
#         "response": {
#             "attestationObject": "o2NmbXRkbm9uZWdhdHRTdG10oGhhdXRoRGF0YVkBZ0mWDeWIDoxodDQXD2R2YFuP5K65ooYyx5lc87qDHZdjRQAAAAAAAAAAAAAAAAAAAAAAAAAAACBmggo_UlC8p2tiPVtNQ8nZ5NSxst4WS_5fnElA2viTq6QBAwM5AQAgWQEA31dtHqc70D_h7XHQ6V_nBs3Tscu91kBL7FOw56_VFiaKYRH6Z4KLr4J0S12hFJ_3fBxpKfxyMfK66ZMeAVbOl_wemY4S5Xs4yHSWy21Xm_dgWhLJjZ9R1tjfV49kDPHB_ssdvP7wo3_NmoUPYMgK-edgZ_ehttp_I6hUUCnVaTvn_m76b2j9yEPReSwl-wlGsabYG6INUhTuhSOqG-UpVVQdNJVV7GmIPHCA2cQpJBDZBohT4MBGme_feUgm4sgqVCWzKk6CzIKIz5AIVnspLbu05SulAVnSTB3NxTwCLNJR_9v9oSkvphiNbmQBVQH1tV_psyi9HM1Jtj9VJVKMeyFDAQAB",
#             "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoiQ2VUV29nbWcwY2NodWlZdUZydjhEWFhkTVpTSVFSVlpKT2dhX3hheVZWRWNCajBDdzN5NzN5aEQ0RmtHU2UtUnJQNmhQSkpBSW0zTFZpZW40aFhFTGciLCJvcmlnaW4iOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJjcm9zc09yaWdpbiI6ZmFsc2V9"
#         },
#         "type": "public-key",
#         "clientExtensionResults": {},
#         "transports": ["internal"]
#     }"""
#     ),
#     expected_challenge=base64url_to_bytes(
#         "CeTWogmg0cchuiYuFrv8DXXdMZSIQRVZJOga_xayVVEcBj0Cw3y73yhD4FkGSe-RrP6hPJJAIm3LVien4hXELg"
#     ),
#     expected_origin="http://localhost:5000",
#     expected_rp_id="localhost",
#     require_user_verification=True,
# )
#
# print("\n[Registration Verification - None]")
# print(registration_verification.json(indent=2))
# assert registration_verification.credential_id == base64url_to_bytes(
#     "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s"
# )