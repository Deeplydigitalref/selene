from typing import Tuple, Dict, Union
from pyfuncify import monad, chronos

from . import value as Val
from common.domain import subject as Sub
from common.domain import subject as Sub
from common.util import env
from key_management.domain import jwt

from common.repository.oauth import authorisation as repo

ErrorType = Tuple[str, str, str]

def client_credentials_authoriser(grant_tuple: Tuple[Dict, Dict]) -> monad.EitherMonad[Union[Val.Authorisation, ErrorType]]:
    """
    Grants access based on the client credentials grant type.
    The Subject is also the AZP.  An authorisation is generated along with a token (JWT)
    :param grant_tuple:
    :return: monad.EitherMonad[Tuple[Dict, Dict]]
    """
    grant, ctx = grant_tuple

    if _invalid_subject(ctx):
        return monad.Left((Val.OauthErrors.INVALID_SUBJECT,
                          "Invalid Subject for Client Credentials Grant",
                          Val.OauthTokenRecommendations.DO_NOT_GRANT))
    subject = ctx['azp'].value
    return _grant_access(subject)


#
# Helpers
#

def _to_domain(model: monad.EitherMonad[repo.AuthorisationModel]) -> monad.EitherMonad[Val.Authorisation]:
    if model.is_left():
        breakpoint()

def _to_model(domain: Val.Authorisation) -> repo.AuthorisationModel:
    return repo.AuthorisationModel(uuid=domain.uuid,
                                   exp=domain.exp,
                                   sub=domain.sub,
                                   azp=domain.azp,
                                   jwt=domain.jwt,
                                   state=domain.state,
                                   is_class_of=domain.is_class_of.value)


def _invalid_subject(ctx: Dict) -> bool:
    azp = ctx.get('azp', None)
    return not(azp and azp.is_right())


def _grant_access(subject: Sub.value.Subject):
    existing_authz = _unexpired_authz(subject)
    if existing_authz:
        return existing_authz

    exp = epoch_exp()
    authz = Val.Authorisation(uuid=subject.uuid,
                              is_class_of=Val.AuthorisationClass.CLIENT_CREDENTIALS,
                              state="blah",
                              sub=subject.uuid,
                              azp=subject.uuid,
                              exp=exp,
                              jwt=_generate_jwt(subject, exp))
    model = _to_model(authz)
    repo.batch_create(model)
    return monad.Right(authz)



def _unexpired_authz(subject):
    existing_authz = repo.find_current_authorisations(subject.uuid, epoch_time_now())
    if existing_authz.is_right() and existing_authz.value:
        return _to_domain(existing_authz.value[0])  #TODO: way better way of determining the first valid authz
    return None

def _generate_jwt(subject: Sub.value.Subject, exp: int) -> str:
    return jwt.generate_signed_jwt(_id_token_claims(subject.uuid, exp))



def _id_token_claims(sub, exp):
    return dict(iss=env.Env.relying_party_id(),
                sub=sub,
                aud="https://api.reference.io",
                iat=epoch_time_now(),
                exp=exp,
                azp=sub,
                gty="client-credentials")


def epoch_time_now():
    return int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()]))

def epoch_exp():
    return (int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()])) + (60 * 60 * 24))