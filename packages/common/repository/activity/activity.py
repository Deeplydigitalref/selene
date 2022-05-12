from typing import Dict, List
from pyfuncify import monad
from attrs import define, field

from common.model import base_model
from ..util import db_batcher

repo = base_model.Activity


@define
class ActivityModel:
    uuid: str
    service_urn: str
    label: str
    activity: str
    definition: str
    policy_statements: list
    client_uuid: str
    repo: repo = field(default=None)


def batch_create(models: List[ActivityModel]) -> List[ActivityModel]:
    models_with_repo = list(map(_batch_save, models))

    try_commit = db_batcher.commit()
    if try_commit.is_right():
        return monad.Right(models_with_repo)
    breakpoint()


@monad.monadic_try()
def find_activities_by_service(service: str):
    condition = None
    condition &= repo.SK.startswith(_base_sk())

    return [_model_from_repo(act) for act in repo.query(hash_key=_act_pk(service),
                                                        filter_condition=condition)]


#
# Helpers
#
def _batch_save(model: ActivityModel) -> ActivityModel:
    base = _to_base(model)
    db_batcher.DbBatchAction().add(base)
    model.repo = base
    return model


def _to_base(model: ActivityModel) -> base_model.Activity:
    return base_model.Activity(hash_key=_act_pk(model.service_urn),
                               range_key=_act_sk(model.activity),
                               uuid=model.uuid,
                               service_urn=model.service_urn,
                               label=model.label,
                               activity=model.activity,
                               definition=model.definition,
                               policy_statements=model.policy_statements,
                               client_uuid=model.client_uuid)


def _model_from_repo(repo: base_model.Activity) -> ActivityModel:
    return ActivityModel(uuid=repo.uuid,
                         service_urn=repo.service_urn,
                         label=repo.label,
                         activity=repo.activity,
                         definition=repo.definition,
                         policy_statements=repo.policy_statements,
                         client_uuid=repo.client_uuid)


def _act_pk(service: str) -> str:
    return "ACT#{}".format(service)


def _act_sk(activity: str) -> str:
    return "{base_sk}{act}".format(base_sk=_base_sk(), act=activity)


def _base_sk() -> str:
    return "ACT#META#"
