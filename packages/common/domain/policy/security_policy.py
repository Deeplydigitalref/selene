from typing import List, Union, Tuple, Dict
from enum import Enum, EnumMeta
from attrs import define
import sys
from pyfuncify import fn, record

from common.util import enum_helpers

class ActivityOperation(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    WRITER = 'https://example.com/ontology/sec/op/writer'
    READER = 'https://example.com/ontology/sec/op/reader'

    default = READER

    def statement(self):
        return {'hasOp': self.value}

@define
class HasOp():
    ops: List[ActivityOperation]

    def statement(self):
        return {'hasOp': list(map(lambda o: o.value, self.ops))}


class SecurityClassificationLevel(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    Level5 = 5   # Highly Protected, for privileged use only
    Level4 = 4
    Level3 = 3
    Level2 = 2
    Level1 = 1
    Level0 = 0   # Open Classificiation

    default = Level0

    def statement(self):
        return {'hasClassificationLevel': self.value}

@define
class HasClassificationLevel:
    lvl: SecurityClassificationLevel

    def statement(self):
        return {'hasClassificationLevel': self.lvl.value}


class Realm(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    INTERNAL = 'https://example.com/ontology/sec/realm/internal'
    API = 'https://example.com/ontology/sec/realm/api'
    CUSTOMER = 'https://example.com/ontology/sec/realm/customer'
    OPEN = 'https://example.com/ontology/sec/realm/open'

    default = OPEN

    def statement(self):
        return {'hasRealm': self.value}

@define
class HasRealm:
    realm: Realm

    def statement(self):
        return {'hasRealm': self.realm.value}

    @classmethod
    def _missing_value_(cls, value):
        breakpoint()


class BoundedContext(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    ALL = 'https://example.com/ontology/sec/boundedContext/ALL'  # applies to all BCs
    NONE = 'https://example.com/ontology/sec/boundedContext/NONE'  # applies to no BCs

    default = NONE

    def statement(self):
        return {'hasBoundedContext': self.value}

@define
class HasBoundedContext:
    boundedContext: BoundedContext

    def statement(self):
        return {'hasBoundedContext': self.boundedContext.value}


class AccessScoping(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    PRIVILEGED = "https://example.com/ontology/sec/scope/privileged"  # only accessible by subjects with privileged attributes
    ANY = "https://example.com/ontology/sec/scope/any"                # all subjects within the defined realms have access
    NONE = "https://example.com/ontology/sec/scope/none"              # no access!

    default = NONE

    def statement(self):
        return {'hasAccessScope': self.value}

@define
class HasAccessScope:
    scopes: List[AccessScoping]

    def statement(self):
        return {'hasAccessScope': list(map(lambda o: o.value, self.scopes))}

PolicyStatementType = Union[HasOp, HasRealm, HasAccessScope, HasClassificationLevel, HasBoundedContext]

def hasOp(objs: List[str]) -> HasOp:
    return HasOp(ops=list(map(lambda o: ActivityOperation(o), objs)))

def hasClassificationLevel(stmt: int) -> HasClassificationLevel:
    return HasClassificationLevel(lvl=SecurityClassificationLevel(stmt))

def hasRealm(stmt: List[str]) -> HasRealm:
    return HasRealm(realm=Realm(stmt))

def hasBoundedContext(stmt: str) -> HasBoundedContext:
    return HasBoundedContext(boundedContext=BoundedContext(stmt))

def hasAccessScope(objs: List[str]) -> HasAccessScope:
    return HasAccessScope(scopes=list(map(lambda o: AccessScoping(o), objs)))

def realm_from_statements(stmts: PolicyStatementType) -> HasRealm:
    return record.at('realm')(fn.find(lambda p: isinstance(p, HasRealm), stmts))

def bounded_context_from_statements(stmts: PolicyStatementType) -> HasBoundedContext:
    return record.at('boundedContext')(fn.find(lambda p: isinstance(p, HasBoundedContext), stmts))


def to_policy_statement(statement: Union[Tuple, Dict]) -> PolicyStatementType:
    """
    When from the domain, the policy statement is a triple, e.g. ('hasOp', ['https://example.com/ontology/sec/op/writer', 'https://example.com/ontology/sec/op/reader'])
    When from the model, its a Dict containing a single statement, e.g. {'hasOp': ['https://example.com/ontology/sec/op/writer', 'https://example.com/ontology/sec/op/reader']}
    :param statement:
    :return:
    """
    if isinstance(statement, tuple):
        predicate, obj = statement
    else:
        predicate = next(iter(statement))
        obj = statement[predicate]
    return getattr(sys.modules[__name__], predicate)(obj)
