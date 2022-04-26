from cerberus import validator

"""
Example Activity Policy
{
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
    'activities': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {'type': 'string'},
                'activity': {'type', 'string'},
                'description': {'type', 'string'},
                'policyStatements': {
                    'type': 'dict',
                    'schema': {
                        'hasOp': {'type': 'list', 'schema': {'type': 'string'}},
                        'hasClassificaton': {'type': 'list', 'schema': {'type': 'string'}},
                        'hasRealm': {'type': 'list', 'schema': {'type': 'string'}},
                        'hasAccessScope': {'type': 'list', 'schema': {'type': 'string'}}
                    }
                }
            }
        }
    }
}

def validate(value):
    val = validator.Validator(schema)
    val.validate(value)
    return val