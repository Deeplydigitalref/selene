import pytest

from tests.shared import key_management_helpers, oauth_client_helpers

from common.domain.activity import activity, value
from common.domain.subject import subject


def setup_module():
    key_management_helpers.set_up_key_management_env()
    pass


def it_adds_activity_to_the_client(set_up_env_without_ssm,
                                     dynamo_mock):
    client_registration, _client_id, _none = oauth_client_helpers.internal_client()

    result = activity.register(activity_request(client_registration.subject))

    updated_client = azp = subject.get(client_registration.subject.uuid, reify=(value.Activity, activity.for_client)).value

    assert len(updated_client.activities) == 1
    assert updated_client.activities[0].activity == "party:resource:customer:registration"


#
# Helpers
#
def activity_request(client):
    return {
        'assertedByClient': client.uuid,
        'activities': service_activity(client.subject_name)
    }


def service_activity(service_name):
    return [
        {
            'service': service_name,
            'name': 'customer-registration',
            'activity': 'party:resource:customer:registration',
            'description': 'Registers a new tenant and tenant party.',
            'policyStatements': {
                'hasOp': ['https://example.com/ontology/sec/op/writer', 'https://example.com/ontology/sec/op/reader'],
                'hasClassificationLevel': 4,
                'hasRealm': ['https://example.com/ontology/sec/realm/internal', 'https://example.com/ontology/sec/realm/api'],
                'hasAccessScope': ['https://example.com/ontology/sec/scope/privileged']
            }
        }
    ]
