from typing import Dict
from pyfuncify import logger, monad
from attrs import define, field

from ..typing.custom_types import Either
from ..model import base_model
from ..util import encoding_helpers
"""
Data Model:

Registration:  Tracking the registration workflow for a subject.
+ PK: REG#{id}
+ SK: META#{subject-name}
"""

repo = base_model.SubjectRegistration


@define
class RegistrationModel:
    """
    The Value object passed between the domain and the repository
    """
    uuid: str
    subject_name: str
    registration_state: str
    registration_challenge: bytes
    encoded_challenge: str = field()
    @encoded_challenge.default
    def _to_base64(self):
        return encoding_helpers.bytes_to_base64url(self.registration_challenge)
    # model: repo.repo()
    repo: repo = field(default=None)


def create(model: RegistrationModel) -> RegistrationModel:
    pk = format_registration_pk(model.uuid)
    sk = format_registration_sk(model.uuid)
    repo = base_model.SubjectRegistration(hash_key=pk,
                                          range_key=sk,
                                          subject_name=model.subject_name,
                                          registration_state=model.registration_state,
                                          encoded_challenge=model.encoded_challenge)
    try_save = save(repo)

    if try_save.is_right():
        model.repo = monad.Right(repo)
        return model
    breakpoint()

@monad.monadic_try()
def save(model) -> Either[Dict]:
    return model.save()

@monad.monadic_try()
def find_by_uuid(uuid: str) -> Either[RegistrationModel]:
    return model_from_repo(uuid, base_model.SubjectRegistration.get(hash_key=format_registration_pk(uuid),
                                                                    range_key=format_registration_sk(uuid)))

def model_from_repo(uuid: str, repo: base_model.SubjectRegistration) -> RegistrationModel:
    return RegistrationModel(uuid=uuid,
                             subject_name=repo.subject_name,
                             registration_state=repo.registration_state,
                             registration_challenge=encoding_helpers.base64url_to_bytes(repo.encoded_challenge),
                             encoded_challenge=repo.encoded_challenge,
                             repo=repo)

def format_registration_pk(uuid):
    return "REG#{}".format(uuid)

def format_registration_sk(uuid):
    return "REG#META#{}".format(uuid)


def put_registration(registration_id: str,
                     subject_name: str,
                     tracer) -> None:
    pk = format_event_pk(unique_event_identity['event_time'])
    sk = format_event_sk(unique_event_identity)

    logger.log(level='info', msg='Put Event', tracer=tracer, ctx={'pk': pk, 'sk': sk})

    repo = base_model.Event(hash_key=pk,
                            range_key=sk,
                            event_time=event_time,
                            event_uuid=event_uuid,
                            bucket=bucket,
                            event_identifiers=coerse_identifiers(event_identifiers),
                            key=key)
    repo.save()
    # TODO: errors on save
    pass
