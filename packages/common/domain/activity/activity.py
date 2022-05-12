import uuid
from typing import Dict, Tuple, List, Callable, Any, Optional, Union
from pyfuncify import monad
from pymonad.tools import curry

from . import activity_validator, value
from common.domain import subject
from common.repository.activity import activity as repo

ActivityTuple = Tuple[Dict, Dict]


def register(activity_request: Dict) -> monad.EitherMonad:
    result = (_validate((activity_request, {})) >> _find_oauth_client >> _build_domain >> _register_activities)

    return result

def get(uuid: str, reify: Tuple[Any, Callable] = None) -> List[Optional[value.Activity]]:
    return _query_by_uuid(uuid, reify)

def for_client(client: subject.value.subject, reify=None) -> List[Optional[value.Activity]]:
    return get(client.subject_name, reify)

#
# Helpers
#
def _query_by_uuid(service: str, reify) -> monad.EitherMonad[List[Optional[value.Activity]]]:
    result = repo.find_activities_by_service(service)
    if result.is_right():
        return monad.Right([_to_domain(model) for model in result.value])
    return monad.Right([])

def _validate(activity_tuple: ActivityTuple) -> monad.EitherMonad[ActivityTuple]:
    activity_request, ctx = activity_tuple
    result, validator = activity_validator.validate(activity_request)
    if result:
        return monad.Right(activity_tuple)
    breakpoint()


def _find_oauth_client(activity_tuple: ActivityTuple) -> monad.EitherMonad[ActivityTuple]:
    activity_request, ctx = activity_tuple
    result = subject.subject.get(activity_request.get('assertedByClient', ""))
    if result.is_left() or not result.value.is_system():
        return monad.Left((value.ActivityError.CLIENT_NOT_SUPPORTED,
                           "Activities not supported for client type",
                           value.ActivityRecommendation.VALIDATION_ERROR))

    ctx['sub'] = result.value
    return monad.Right((activity_request, ctx))


def _build_domain(activity_tuple: ActivityTuple) -> monad.EitherMonad[List[value.Activity]]:
    activity_request, ctx = activity_tuple
    return monad.Right(list(map(_domain_builder(ctx['sub']), activity_request['activities'])))


def _register_activities(activities: List[value.Activity]) -> monad.EitherMonad[List[str]]:
    result = repo.batch_create(list(map(_to_model, activities)))
    if result.is_right():
        return monad.Right(activities)
    breakpoint()

@curry(2)
def _domain_builder(client: subject.value.Subject, act: Dict) -> value.Activity:
    return value.Activity(uuid=str(uuid.uuid4()),
                          service_urn=act['service'],
                          label=act['name'],
                          activity=act['activity'],
                          definition=act['description'],
                          policy_statements=list(map(_to_policy_statement, act['policyStatements'].items())),
                          client=client)


def _to_policy_statement(statement: Union[Tuple, Dict]) -> value.PolicyStatement:
    """
    When from the domain, the policy statement is a triple, e.g. ('hasOp', ['writer', 'reader'])
    When from the model, its a Dict containing a single statement, e.g. {'hasOp': ['writer', 'reader']}
    :param statement:
    :return:
    """
    if isinstance(statement, tuple):
        predicate, object = statement
    else:
        predicate = next(iter(statement))
        object = statement[predicate]
    return value.PolicyStatement(predicate=predicate, attributes=object)


def _to_model(activity: value.Activity) -> repo.ActivityModel:
    return repo.ActivityModel(uuid=activity.uuid,
                              service_urn=activity.service_urn,
                              label=activity.label,
                              activity=activity.activity,
                              definition=activity.definition,
                              policy_statements=_policy_statements_to_dict(activity.policy_statements),
                              client_uuid=activity.client.uuid)


def _policy_statements_to_dict(stmts) -> Dict:
    return [stmt.to_dict() for stmt in stmts]


def _to_domain(model: repo.ActivityModel) -> value.Activity:
    return value.Activity(uuid=model.uuid,
                          service_urn=model.service_urn,
                          label=model.label,
                          activity=model.activity,
                          definition=model.definition,
                          policy_statements=list(map(_to_policy_statement, model.policy_statements)),
                          client_uuid=model.uuid)

