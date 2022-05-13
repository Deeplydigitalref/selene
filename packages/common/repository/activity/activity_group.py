from typing import Dict, List
from pyfuncify import monad
from attrs import define, field

from common.model import base_model
from ..util import db_batcher

repo = base_model.ActivityGroup


@define
class ActivityGroupModel:
    uuid: str
    asserted_client: str
    label: str
    activity_group: str
    definition: str
    policy_statements: list
    repo: repo = field(default=None)


def batch_create(models: List[ActivityGroupModel]) -> List[ActivityGroupModel]:
    models_with_repo = list(map(_batch_save, models))

    try_commit = db_batcher.commit()
    if try_commit.is_right():
        return monad.Right(models_with_repo)
    breakpoint()


@monad.monadic_try()
def find_by_group(group: str):
    return _model_from_repo(base_model.ActivityGroup.get(hash_key=_atg_pk(group),
                                                         range_key=_atg_sk(group)))


#
# Helpers
#
def _batch_save(model: ActivityGroupModel) -> ActivityGroupModel:
    base = _to_base(model)
    db_batcher.DbBatchAction().add(base)
    model.repo = base
    return model


def _to_base(model: ActivityGroupModel) -> base_model.ActivityGroup:
    return base_model.ActivityGroup(hash_key=_atg_pk(model.activity_group),
                                    range_key=_atg_sk(model.activity_group),
                                    uuid=model.uuid,
                                    asserted_client=model.asserted_client,
                                    label=model.label,
                                    activity_group=model.activity_group,
                                    definition=model.definition,
                                    policy_statements=model.policy_statements)


def _model_from_repo(repo: base_model.ActivityGroup) -> ActivityGroupModel:
    return ActivityGroupModel(uuid=repo.uuid,
                              asserted_client=repo.asserted_client,
                              label=repo.label,
                              activity_group=repo.activity_group,
                              definition=repo.definition,
                              policy_statements=repo.policy_statements)


def _atg_pk(group: str) -> str:
    return "ATG#{}".format(group)


def _atg_sk(group: str) -> str:
    return "{base_sk}{grp}".format(base_sk=_base_sk(), grp=group)


def _base_sk() -> str:
    return "ATG#META#"
