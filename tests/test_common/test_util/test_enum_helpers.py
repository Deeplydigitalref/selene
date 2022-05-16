import pytest
from enum import Enum
from common.util import enum_helpers

def it_returns_a_default_value():
    assert MyEnum('missing') == MyEnum.A


def it_returns_an_error_when_no_default():
    with pytest.raises(Exception) as e:
        MyEnumWithoutDefault('missing')

    assert str(e.value) == "'missing' is not a valid MyEnumWithoutDefault"

def it_returns_a_right_on_success():
    result = MyEnum.either('missing')
    assert result.is_right()
    assert result.value == MyEnum.A

def it_returns_a_left_on_failure():
    result = MyEnumWithoutDefault.either('missing')
    assert result.is_left()


#
# Fixtures
#
class MyEnum(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    A = "a"
    B = "b"
    C = "c"
    default = A


class MyEnumWithoutDefault(Enum, metaclass=enum_helpers.DefaultEnumMeta):
    A = "a"
    B = "b"
    C = "c"
