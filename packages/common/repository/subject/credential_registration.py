from typing import Dict
from pyfuncify import monad
from attrs import define, field

from common.model import base_model
from common.util import encoding_helpers

"""
Data Model:

Registration:  Tracking the registration workflow for a subject.
+ PK: REG#{id}
+ SK: REG#META#{id}
"""

repo = base_model.CredentialRegistration


@define
class RegistrationModel:
    """
    The Value object passed between the domain and the repository
    """
    uuid: str
    subject_name: str
    state: str
    realm: str
    is_class_of: str
    client_secret: str = field(default=None)
    registration_challenge: bytes  = field(default=None)
    encoded_challenge: str = field(default=None)
    sub: str = field(default=None)
    repo: repo = field(default=None)


def create(model: RegistrationModel) -> RegistrationModel:
    pk = format_registration_pk(model.uuid)
    sk = format_registration_sk(model.uuid)
    repo = base_model.CredentialRegistration(hash_key=pk,
                                             range_key=sk,
                                             reg_uuid=model.uuid,
                                             client_secret=model.client_secret,
                                             realm=model.realm,
                                             subject_name=model.subject_name,
                                             is_class_of=model.is_class_of,
                                             sub=None,
                                             encoded_challenge=model.encoded_challenge,
                                             state=model.state)
    try_save = save(repo)

    if try_save.is_right():
        model.repo = repo
        return monad.Right(model)
    breakpoint()


def completed_state_change(model: RegistrationModel) -> RegistrationModel:
    """
    Adds the credential and sets the completion state
    :param model:
    :return RegistrationModel:
    """
    model.repo.state = model.state
    model.repo.sub = model.sub
    try_save = save(model.repo)
    if try_save.is_right():
        model.repo = monad.Right(model.repo)
        return model
    breakpoint()


@monad.monadic_try()
def save(model) -> monad.EitherMonad[Dict]:
    return model.save()


@monad.monadic_try()
def find_by_uuid(uuid: str) -> monad.EitherMonad[RegistrationModel]:
    return model_from_repo(base_model.CredentialRegistration.get(hash_key=format_registration_pk(uuid),
                                                                 range_key=format_registration_sk(uuid)))


def model_from_repo(repo: base_model.CredentialRegistration) -> RegistrationModel:
    return RegistrationModel(uuid=repo.reg_uuid,
                             subject_name=repo.subject_name,
                             sub=repo.sub,
                             state=repo.state,
                             client_secret=repo.client_secret,
                             realm=repo.realm,
                             is_class_of=repo.is_class_of,
                             registration_challenge=encoding_helpers.base64url_to_bytes(repo.encoded_challenge),
                             encoded_challenge=repo.encoded_challenge,
                             repo=repo)


def format_registration_pk(uuid):
    return "REG#{}".format(uuid)


def format_registration_sk(uuid):
    return "REG#META#{}".format(uuid)
