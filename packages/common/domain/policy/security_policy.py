from enum import Enum

class ActivityOperation(Enum):
    WRITER = 'https://example.com/ontologies/sec/writer'
    READER = 'https://example.com/ontologies/sec/reader'

    def statement(self):
        return {'hasOp': self.value}


class SecurityClassificationLevel(Enum):
    Level5 = 5   # Highly Protected, for privileged use only
    Level4 = 4
    Level3 = 3
    Level2 = 2
    Level1 = 1
    Level0 = 0   # Open Classificiation

    def statement(self):
        return {'hasClassificationLevel': self.value}

class Realm(Enum):
    INTERNAL = 'https://example.com/ontologies/sec/realm/internal'
    CUSTOMER = 'https://example.com/ontologies/sec/realm/customer'
    OPEN = 'https://example.com/ontologies/sec/realm/open'
    API = 'https://example.com/ontologies/sec/realm/api'

    def statement(self):
        return {'hasRealm': self.value}


class AccessScoping(Enum):
    PRIVILEGED = "https://example.com/ontologies/sec/scope/privileged"  # only accessible by subjects with privileged rights
    ANY = "https://example.com/ontologies/sec/scope/any"                # all subjects within the defined realms have access

    def statement(self):
        return {'hasAccessScope': self.value}
