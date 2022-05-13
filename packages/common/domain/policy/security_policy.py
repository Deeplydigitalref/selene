from typing import List, TypeVar, Generic
from enum import Enum
from attrs import define

T = TypeVar('T')

class PolicyStatement(Generic[T]):
    pass


class ActivityOperation(Enum):
    WRITER = 'https://example.com/ontology/sec/op/writer'
    READER = 'https://example.com/ontology/sec/op/reader'

    def statement(self):
        return {'hasOp': self.value}

@define
class HasOp:
    ops: List[ActivityOperation]

    def statement(self):
        return {'hasOp': list(map(lambda o: o.value, self.ops))}


class SecurityClassificationLevel(Enum):
    Level5 = 5   # Highly Protected, for privileged use only
    Level4 = 4
    Level3 = 3
    Level2 = 2
    Level1 = 1
    Level0 = 0   # Open Classificiation

    def statement(self):
        return {'hasClassificationLevel': self.value}

@define
class HasClassificationLevel:
    lvl: SecurityClassificationLevel

    def statement(self):
        return {'hasClassificationLevel': self.lvl.value}


class Realm(Enum):
    INTERNAL = 'https://example.com/ontology/sec/realm/internal'
    CUSTOMER = 'https://example.com/ontology/sec/realm/customer'
    OPEN = 'https://example.com/ontology/sec/realm/open'
    API = 'https://example.com/ontology/sec/realm/api'

    def statement(self):
        return {'hasRealm': self.value}

@define
class HasRealm:
    realms: List[Realm]

    def statement(self):
        return {'hasRealm': list(map(lambda o: o.value, self.realms))}


class AccessScoping(Enum):
    PRIVILEGED = "https://example.com/ontology/sec/scope/privileged"  # only accessible by subjects with privileged rights
    ANY = "https://example.com/ontology/sec/scope/any"                # all subjects within the defined realms have access

    def statement(self):
        return {'hasAccessScope': self.value}

@define
class HasAccessScope:
    scopes: List[AccessScoping]

    def statement(self):
        return {'hasAccessScope': list(map(lambda o: o.value, self.scopes))}


def hasOp(objs: List[str]) -> HasOp:
    return HasOp(ops=list(map(lambda o: ActivityOperation(o), objs)))

def hasClassificationLevel(obj: int) -> HasClassificationLevel:
    return HasClassificationLevel(lvl=SecurityClassificationLevel(obj))

def hasRealm(objs: List[str]) -> HasRealm:
    return HasRealm(realms=list(map(lambda o: Realm(o), objs)))


def hasAccessScope(objs: List[str]) -> HasAccessScope:
    return HasAccessScope(scopes=list(map(lambda o: AccessScoping(o), objs)))
