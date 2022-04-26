from typing import Dict
from pyfuncify import monad
from attrs import define, field

from common.model import base_model
from common.util import encoding_helpers

"""
Data Model:

Registration:  Tracking the registration workflow for a subject.
+ PK: REG#{id}
+ SK: META#{subject-name}
"""

repo = base_model.ServiceSubjectRegistration


@define
class RegistrationModel:
    """
    The Value object passed between the domain and the repository
    """
    uuid: str
    subject_name: str
    state: str
    registration_challenge: bytes  # = field()
    encoded_challenge: str = field()
    sub: str = field(default=None)

    @encoded_challenge.default
    def _to_base64(self):
        return encoding_helpers.bytes_to_base64url(self.registration_challenge)

    credential: str = field(default=None)
    repo: repo = field(default=None)


def create(model: RegistrationModel) -> RegistrationModel:
    pk = format_registration_pk(model.uuid)
    sk = format_registration_sk(model.uuid)
    repo = base_model.WebAuthnSubjectRegistration(hash_key=pk,
                                                  range_key=sk,
                                                  reg_uuid=model.uuid,
                                                  subject_name=model.subject_name,
                                                  sub=None,
                                                  state=model.state,
                                                  encoded_challenge=model.encoded_challenge)
    try_save = save(repo)

    if try_save.is_right():
        model.repo = monad.Right(repo)
        return model
    breakpoint()


def completed_state_change(model: RegistrationModel) -> RegistrationModel:
    """
    Adds the credential and sets the completion state
    :param model:
    :return RegistrationModel:
    """
    model.repo.state = model.state
    model.repo.credential = model.credential
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
    return model_from_repo(base_model.WebAuthnSubjectRegistration.get(hash_key=format_registration_pk(uuid),
                                                                      range_key=format_registration_sk(uuid)))


def model_from_repo(repo: base_model.WebAuthnSubjectRegistration) -> RegistrationModel:
    return RegistrationModel(uuid=repo.reg_uuid,
                             subject_name=repo.subject_name,
                             sub=repo.sub,
                             state=repo.state,
                             registration_challenge=encoding_helpers.base64url_to_bytes(repo.encoded_challenge),
                             encoded_challenge=repo.encoded_challenge,
                             repo=repo)


def format_registration_pk(uuid):
    return "WAR#{}".format(uuid)


def format_registration_sk(uuid):
    return "WAR#META#{}".format(uuid)
