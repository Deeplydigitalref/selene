import json
from webauthn.registration import generate_registration_options as webauthn_opts
from webauthn.registration import verify_registration_response as webauthn_verify
from webauthn.helpers import cose, structs, options_to_json

from key_management.domain import crypto


def generate_options(rp_id, rp_name, subject_name) -> structs.PublicKeyCredentialCreationOptions:
    challenge = crypto.generate_challenge()
    return generate(rp_id=rp_id,
                    rp_name=rp_name,
                    user_id=subject_name,
                    user_name=subject_name,
                    user_display_name=subject_name,
                    challenge=challenge)

def generate(rp_id, rp_name, user_id, user_name, user_display_name, challenge) -> structs.PublicKeyCredentialCreationOptions:
    return webauthn_opts.generate_registration_options(rp_id=rp_id,
                                                      rp_name=rp_name,
                                                      user_id=user_id,
                                                      user_name=user_name,
                                                      user_display_name=user_display_name,
                                                      attestation=structs.AttestationConveyancePreference.DIRECT,
                                                      authenticator_selection=structs.AuthenticatorSelectionCriteria(
                                                            authenticator_attachment=structs.AuthenticatorAttachment.PLATFORM,
                                                            resident_key=structs.ResidentKeyRequirement.REQUIRED,
                                                        ),
                                                      challenge=challenge,
                                                      exclude_credentials=[
                                                          structs.PublicKeyCredentialDescriptor(id=challenge),
                                                      ],
                                                      supported_pub_key_algs=[cose.COSEAlgorithmIdentifier.ECDSA_SHA_512],
                                                      timeout=12000)


def reg_credential(challenge_response: dict) -> structs.RegistrationCredential:
    return structs.RegistrationCredential.parse_raw(json.dumps(challenge_response))

def reg_verify(credential: structs.RegistrationCredential,
               challenge: bytes,
               expected_origin: str,
               expected_rp_id: str,
               require_user_verification: bool):
        return webauthn_verify.verify_registration_response(credential=credential,
                                                            expected_challenge=challenge,
                                                            expected_origin=expected_origin,
                                                            expected_rp_id=expected_rp_id,
                                                            require_user_verification=require_user_verification)

def serialise_options(options: structs.PublicKeyCredentialCreationOptions) -> str:
    return options_to_json(options)