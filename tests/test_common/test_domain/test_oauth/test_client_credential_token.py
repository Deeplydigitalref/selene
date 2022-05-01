import pytest

from common.domain.oauth import token
from common.domain.subject import registration
from key_management.domain import sym_enc
from tests.shared import key_management_helpers

def setup_module():
    key_management_helpers.set_up_key_management_env()
    pass

#
# success
#
def it_issues_a_token(set_up_env_without_ssm,
                      dynamo_mock):

    result = token.token_grant(token_request(internal_client()))
    breakpoint()



#
# Helpers
#
def internal_client():
    service_value = {
        'serviceName': 'urn:service:service1',
        'realm': 'https://example.com/ontologies/sec/realm/internal'
    }
    client = registration.new_service(service_value)
    secret = sym_enc.jwe_decrypt(client.client_secret)
    return client, secret, None


def token_request(system_client_tuple):
    client, secret, redirect_uri = system_client_tuple
    return {"client_id": client.subject.uuid,
            "client_secret": secret,
            "grant_type": "client_credentials",
            "scope": None,
            "redirect_uri": redirect_uri}
