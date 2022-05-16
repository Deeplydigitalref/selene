import pytest

from tests.shared import key_management_helpers, oauth_client_helpers

from common.domain.activity import activity_group


def setup_module():
    key_management_helpers.set_up_key_management_env()
    pass


def it_adds_activity_group(set_up_env_without_ssm,
                           dynamo_mock):

    client_registration, _client_id, _none = oauth_client_helpers.internal_client()

    result = activity_group.register(activity_group_request(client_registration.subject))

    assert result.is_right()

    group = activity_group.get(realm='https://example.com/ontology/sec/realm/internal',
                               bounded_context='https://example.com/ontology/sec/boundedContext/ANY',
                               label='internalServicesInternalANY').value

    assert group.activity_group == 'internalServicesInternalANY'

#
# Helpers
#
def activity_group_request(client):
    return {
        'assertedByClient': client.uuid,
        'activityGroups': service_activity_groups()
    }


def service_activity_groups():
    return [
        {
            'activityGroup': 'internalServicesInternalANY',
            'label': 'Internal Services across all Contexts',
            'definition': 'Activities for all services within the internal Realm across all bounded contexts',
            'policyStatements': {
                'hasOp': ['https://example.com/ontology/sec/op/writer', 'https://example.com/ontology/sec/op/reader'],
                'hasClassificationLevel': 4,
                'hasRealm': 'https://example.com/ontology/sec/realm/internal',
                'hasAccessScope': ['https://example.com/ontology/sec/scope/privileged'],
                'hasBoundedContext': 'https://example.com/ontology/sec/boundedContext/ANY'
            }
        }
    ]
