from typing import Tuple
from cerberus import validator

"""
Example Activity Policy
{
    'assertedByClient': "{uuid}",
    'activities', [
        {
            'name': 'customer-registration', 
            'activity': 'party:resource:customer:registringation', 
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
"""
schema = {
    'assertedByClient': {'type': 'string'},
    'activities': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'service': {'type': 'string'},
                'name': {'type': 'string'},
                'activity': {'type': 'string'},
                'description': {'type': 'string'},
                'policyStatements': {
                    'type': 'dict',
                    'schema': {
                        'hasOp': {'type': 'list', 'schema': {'type': 'string'}},
                        'hasClassificationLevel': {'type': 'integer'},
                        'hasRealm': {'type': 'list', 'schema': {'type': 'string'}},
                        'hasAccessScope': {'type': 'list', 'schema': {'type': 'string'}}
                    }
                }
            }
        }
    }
}


def validate(value) -> Tuple[bool, validator.Validator]:
    val = validator.Validator(schema)
    return (val.validate(value), val)
