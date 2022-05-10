from typing import Dict, List
from pyfuncify import monad
from attrs import define, field

from common.model import base_model
from ..util import db_batcher

repo = base_model.Authorisation


@define
class AuthorisationModel:
    """
    The Value object passed between the domain and the repository
    """
    uuid: str
    azp: str
    sub: str
    is_class_of: str
    exp: int
    jwt: str
    state: str
    repo: repo = field(default=None)


def batch_create(model: AuthorisationModel) -> AuthorisationModel:
    authz_repo = azp_repo_builder(model)
    db_batcher.DbBatchAction().add(authz_repo)

    sub_repo = sub_repo_builder(model)
    db_batcher.DbBatchAction().add(sub_repo)

    try_commit = db_batcher.commit()
    if try_commit.is_right():
        return model
    breakpoint()


def create(model: AuthorisationModel) -> AuthorisationModel:
    breakpoint()
    repo = base_model.Authorisation(hash_key=_azp_pk(model.uuid),
                                    range_key=_azp_sk(model.uuid),
                                    state=model.state,
                                    is_class_of=model.is_class_of,
                                    sub=model.uuid,
                                    )
    try_save = save(repo)

    if try_save.is_right():
        model.repo = monad.Right(repo)
        return model
    breakpoint()


@monad.monadic_try()
def save(model) -> monad.EitherMonad[Dict]:
    return model.save()


@monad.monadic_try()
def find_current_authorisations(uuid, exp: int):
    condition = None
    condition &= repo.SK > exp

    return [_model_from_repo(r) for r in repo.query(hash_key=_azp_pk(uuid),
                                                    filter_condition=condition)]


#
# Helpers
#

def azp_repo_builder(model: AuthorisationModel) -> base_model.Authorisation:
    """
    The Authz side of the subject authz.
    PK: the Authorised Party (AZP), which is a subject, side of the Authorisation.
        Note that client credential grants have the same AZP and SUB, whereas authorisation code grants dont.
    SK: includes the epoch expiry.
    """
    return base_model.Authorisation(hash_key=_azp_pk(model.uuid),
                                    range_key=_azp_sk(model.exp),
                                    exp=model.exp,
                                    state=model.state,
                                    is_class_of=model.is_class_of,
                                    sub=model.uuid)

def sub_repo_builder(model: AuthorisationModel) -> base_model.Authorisation:
    """
    The Subject side of the subject authz.
    PK: the Subject (SUB), which is a subject, side of the Authorisation
    SK: includes the epoch expiry.
    """
    return base_model.Authorisation(hash_key=_sub_pk(model.sub),
                                    range_key=_sub_sk(model.exp),
                                    state=model.state,
                                    is_class_of=model.is_class_of,
                                    exp=model.exp,
                                    sub=model.uuid)


def _model_from_repo(repo: base_model.Subject) -> AuthorisationModel:
    return AuthorisationModel(uuid=repo.uuid,
                              state=repo.state,
                              exp=repo.exp,
                              is_class_of=repo.is_class_of,
                              repo=repo)


def _azp_pk(uuid):
    return "AUZ#{}".format(uuid)

def _azp_sk(ts):
    return "AUZ#EXP#{}".format(ts)

def _sub_pk(uuid):
    return "SUB#{}".format(uuid)

def _sub_sk(ts):
    return "SUB#EXP#{}".format(ts)
