import uuid
from typing import Dict, Tuple, List, Callable, Any, Optional, Union
from pyfuncify import monad
from pymonad.tools import curry

from . import activity_group_validator, value
from common.domain import subject
from common.domain.policy import security_policy
from common.repository.activity import activity_group as repo

ActivityGroupTuple = Tuple[Dict, Dict]

#
# API
#

def register(activity_request: Dict) -> monad.EitherMonad:
    result = (_validate((activity_request, {})) >> _find_oauth_client >> _build_domain >> _register_activity_groups)

    return result

def get(group: str, reify: Tuple[Any, Callable] = None) -> monad.EitherMonad[value.ActivityGroup]:
    return _query_by_group(group, reify)


#
# Helpers
#
def _query_by_group(group: str, reify) -> monad.EitherMonad[value.ActivityGroup]:
    result = repo.find_by_group(group)
    if result.is_right():
        return monad.Right(_to_domain(result.value))
    breakpoint()


def _validate(activity_group_tuple: ActivityGroupTuple) -> monad.EitherMonad[ActivityGroupTuple]:
    activity_group_request, ctx = activity_group_tuple
    result, validator = activity_group_validator.validate(activity_group_request)
    if result:
        return monad.Right(activity_group_tuple)
    breakpoint()


def _find_oauth_client(activity_group_tuple: ActivityGroupTuple) -> monad.EitherMonad[ActivityGroupTuple]:
    activity_group, ctx = activity_group_tuple
    result = subject.subject.get(activity_group.get('assertedByClient', ""))
    if result.is_left() or not result.value.is_system():
        return monad.Left((value.ActivityError.CLIENT_NOT_SUPPORTED,
                           "Activities not supported for client type",
                           value.ActivityRecommendation.VALIDATION_ERROR))

    ctx['sub'] = result.value
    return monad.Right((activity_group, ctx))


def _build_domain(activity_group_tuple: ActivityGroupTuple) -> monad.EitherMonad[List[value.Activity]]:
    activity_group, ctx = activity_group_tuple
    return monad.Right(list(map(_domain_builder(ctx['sub']), activity_group['activityGroups'])))


def _register_activity_groups(activity_groups: List[value.ActivityGroup]) -> monad.EitherMonad[List[str]]:
    result = repo.batch_create(list(map(_to_model, activity_groups)))
    if result.is_right():
        return monad.Right(activity_groups)
    breakpoint()


@curry(2)
def _domain_builder(client: subject.value.Subject, atg: Dict) -> value.ActivityGroup:
    return value.ActivityGroup(uuid=str(uuid.uuid4()),
                               asserted_client=client.uuid,
                               label=atg['label'],
                               activity_group=atg['activityGroup'],
                               definition=atg['definition'],
                               policy_statements=list(
                                   map(security_policy.to_policy_statement, atg['policyStatements'].items())),
                               client=client)


def _to_model(activity_group: value.ActivityGroup) -> repo.ActivityGroupModel:
    return repo.ActivityGroupModel(uuid=activity_group.uuid,
                                   asserted_client=activity_group.asserted_client,
                                   label=activity_group.label,
                                   activity_group=activity_group.activity_group,
                                   definition=activity_group.definition,
                                   policy_statements=_policy_statements_to_dict(activity_group.policy_statements))


def _policy_statements_to_dict(stmts) -> Dict:
    return [stmt.statement() for stmt in stmts]


def _to_domain(model: repo.ActivityGroupModel) -> value.ActivityGroup:
    return value.ActivityGroup(uuid=model.uuid,
                               asserted_client=model.asserted_client,
                               label=model.label,
                               activity_group=model.activity_group,
                               definition=model.definition,
                               policy_statements=list(
                                   map(security_policy.to_policy_statement, model.policy_statements)))
