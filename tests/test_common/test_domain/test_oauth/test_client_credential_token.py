import pytest

from common.domain.oauth import token, value, authorisation
from common.domain.subject import subject
from key_management.domain import jwt
from tests.shared import key_management_helpers, oauth_client_helpers


def setup_module():
    key_management_helpers.set_up_key_management_env()
    pass


#
# Successful token generation
#
def it_issues_a_token(set_up_env_without_ssm,
                      dynamo_mock):
    client = oauth_client_helpers.internal_client()
    result = token.token_grant(token_request(client))

    assert result.is_right()

    id_token = jwt.decode_and_validate(result.value.jwt)

    assert id_token.is_right()
    assert id_token.value['azp'] == client[0].subject.uuid
    assert id_token.value['sub'] == client[0].subject.uuid


def test_authz_can_be_found_by_sub(set_up_env_without_ssm,
                                   dynamo_mock):
    client = oauth_client_helpers.internal_client()
    result = token.token_grant(token_request(client))

    sub = subject.get(client[0].subject.uuid, reify=(value.Authorisation, authorisation.from_subject)).value

    assert len(sub.authorisations) == 1
    assert sub.authorisations[0].uuid == result.value.uuid


def test_authz_can_be_found_by_azp(set_up_env_without_ssm,
                                   dynamo_mock):
    client = oauth_client_helpers.internal_client()
    result = token.token_grant(token_request(client))

    azp = subject.get(result.value.azp, reify=(value.Authorisation, authorisation.from_azp)).value

    assert len(azp.authorisations) == 1
    assert azp.authorisations[0].uuid == result.value.uuid


#
# Helpers
#

def token_request(system_client_tuple):
    client, secret, redirect_uri = system_client_tuple
    return {"client_id": client.subject.uuid,
            "client_secret": secret,
            "grant_type": "client_credentials",
            "scope": None,
            "redirect_uri": redirect_uri}
