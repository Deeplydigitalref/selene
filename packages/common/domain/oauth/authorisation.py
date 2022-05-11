from typing import Any, Callable, Tuple, List

from pyfuncify import monad

from . import value
from common.domain.subject import value as subject_value
from common.util import time_helpers
from common.repository.oauth import authorisation as repo


#
# API
#
def get_for_sub(uuid: str, reify: Tuple[Any, Callable] = None) -> value.Authorisation:
    return _find_for_sub(uuid, reify)

def get_for_azp(uuid: str, reify: Tuple[Any, Callable] = None) -> value.Authorisation:
    return _find_for_azp(uuid, reify)

def from_subject(subject: subject_value.Subject) -> monad.EitherMonad[List[value.Authorisation]]:
    return get_for_sub(subject.uuid)

def from_azp(subject_as_azp: subject_value.Subject) -> monad.EitherMonad[List[value.Authorisation]]:
    return get_for_azp(subject_as_azp.uuid)


#
# Helpers
#

def _find_for_sub(uuid: str, reify: Tuple[value.Authorisation, Callable]) -> monad.EitherMonad[List[value.Authorisation]]:
    return _to_result(repo.find_current_authorisations_by_sub(uuid, exp=_now_as_epoch()))

def _find_for_azp(uuid: str, reify: Tuple[value.Authorisation, Callable]) -> monad.EitherMonad[List[value.Authorisation]]:
    return _to_result(repo.find_current_authorisations_by_azp(uuid, exp=_now_as_epoch()))

def _to_result(models: monad.EitherMonad[List[repo.AuthorisationModel]]) -> monad.EitherMonad[List[value.Authorisation]]:
    authz = list(map(_to_domain, models.value))
    # if reify:
    #     cls, reify_fn = reify
    #     breakpoint()
    #     return reify_token_caller(cls)(reg, reify_fn)
    return monad.Right(authz)



def _to_domain(model):
    return value.Authorisation(uuid=model.uuid,
                               is_class_of=value.AuthorisationClass[model.is_class_of],
                               state=model.state,
                               sub=model.sub,
                               azp=model.azp,
                               exp=model.exp,
                               jwt=model.jwt,
                               model=model)


def _now_as_epoch():
    return time_helpers.epoch_exp(seconds_from_now=0)
