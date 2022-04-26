from common.domain.activity import activity

#
# Helpers
#
def service_activities():
    return {
        'activities', [
            {
                'service': 'urn:service:party',
                'name': 'customer-registringation',
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
    }
