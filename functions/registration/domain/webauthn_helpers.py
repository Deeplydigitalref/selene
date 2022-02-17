from webauthn.registration import generate_registration_options as webauthn_opts
from webauthn.helpers import cose
from webauthn.helpers import structs

from common.util import crypto


def generate_options(rp_id, rp_name, subject_name) -> structs.PublicKeyCredentialCreationOptions:
    challenge = crypto.generate_challenge()
    return webauthn_opts.generate_registration_options(rp_id=rp_id,
                                                      rp_name=rp_name,
                                                      user_id=subject_name,
                                                      user_name=subject_name,
                                                      user_display_name=subject_name,
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


def options_to_json(options: structs.PublicKeyCredentialCreationOptions) -> str:
    return webauthn_opts.options_to_json(complex_registration_options)