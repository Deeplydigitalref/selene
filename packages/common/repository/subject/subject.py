from typing import Dict, List
from pyfuncify import logger, monad
from attrs import define, field

from common.model import base_model

repo = base_model.Subject

@define
class SubjectModel:
    """
    The Value object passed between the domain and the repository
    """
    uuid: str
    subject_name: str
    state: str
    registrations: List
    repo: repo = field(default=None)


def create(model: SubjectModel) -> SubjectModel:
    repo = base_model.Subject(hash_key=sub_pk(model.uuid),
                              range_key=sub_sk(model.uuid),
                              state=model.state,
                              sub=model.uuid,
                              subject_name=model.subject_name,
                              registrations=model.registrations)
    try_save = save(repo)

    if try_save.is_right():
        model.repo = monad.Right(repo)
        return model
    breakpoint()


@monad.monadic_try()
def save(model) -> monad.EitherMonad[Dict]:
    return model.save()

def subject_from_registration(registration):
    if registration.is_left():
        return None

@monad.monadic_try()
def find_by_uuid(uuid: str) -> monad.EitherMonad[SubjectModel]:
    return model_from_repo(base_model.Subject.get(hash_key=sub_pk(uuid),
                                                  range_key=sub_sk(uuid)))


def model_from_repo(repo: base_model.Subject) -> SubjectModel:
    return SubjectModel(uuid=repo.sub,
                        subject_name=repo.subject_name,
                        registrations=repo.registrations,
                        state=repo.state,
                        repo=repo)


def sub_pk(uuid):
    return "SUB#{}".format(uuid)


def sub_sk(uuid):
    return "SUB#META#{}".format(uuid)
