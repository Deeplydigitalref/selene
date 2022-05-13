import pytest

from tests.shared import key_management_helpers, oauth_client_helpers

from common.domain.activity import activity_group, value


def setup_module():
    key_management_helpers.set_up_key_management_env()
    pass


def it_adds_activity_group(set_up_env_without_ssm,
                           dynamo_mock):

    client_registration, _client_id, _none = oauth_client_helpers.internal_client()

    result = activity_group.register(activity_group_request(client_registration.subject))
    breakpoint()

    # updated_client = azp = subject.get(client_registration.subject.uuid,
    #                                    reify=(value.Activity, activity.for_client)).value
    #
    # assert len(updated_client.activities) == 1
    # assert updated_client.activities[0].activity == "party:resource:customer:registration"


#
# Helpers
#
def activity_request(client):
    return {
        'assertedByClient': client.uuid,
        'activity_group': service_activity_groups()
    }


def service_activity_groups():
    return [
        {
            'activityGroup': 'internalServices',
            'label': 'Internal Services',
            'definition': 'Activities used by an internal service',
            'policyStatements': {
                'hasOp': ['writer', 'reader'],
                'hasClassificationLevel': 4,
                'hasRealm': ['internal'],
                'hasAccessScope': ['privileged']
            }
        }
    ]

    return [
        {
            'service': service_name,
            'name': 'customer-registration',
            'activity': 'party:resource:customer:registration',
            'description': 'Registers a new tenant and tenant party.',
            'policyStatements': {
                'hasOp': ['writer', 'reader'],
                'hasClassificationLevel': 4,
                'hasRealm': ['internal', 'api'],
                'hasAccessScope': ['privileged']
            }
        }
    ]
