from typing import Tuple
from cerberus import validator

"""
Example Activity Policy
{
    'assertedByClient': "{uuid}",
    'activityGroups', [
        {
            'activityGroup': 'internalServices',
            'label': 'Internal Services',
            'definition': 'Activities used by an internal service',
            'policyStatements': {
                'hasOp': ['https://example.com/ontology/sec/op/writer', 'https://example.com/ontology/sec/op/reader'],
                'hasClassificationLevel': 4,
                'hasRealm': ['https://example.com/ontology/sec/realm/internal', 'https://example.com/ontology/sec/realm/api'],
                'hasAccessScope': ['https://example.com/ontology/sec/scope/privileged']
            }
        }
    ]
}
"""
schema = {
    'assertedByClient': {'type': 'string'},
    'activityGroups': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'activityGroup': {'type': 'string'},
                'label': {'type': 'string'},
                'definition': {'type': 'string'},
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
