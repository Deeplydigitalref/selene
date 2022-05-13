import sys
from common.util import layer


def it_augments_object_with_reifier():
    result = reifyee(reify=(type_of_thing_that_is_to_be_added, reifier_fn))

    assert result == {'main': "main", 'added': 1}

def it_doesnt_augment_when_not_setup():
    result = reifyee()

    assert result == {'main': "main"}

def it_doesnt_augment_when_reifier_cant_be_found():
    result = reifyee_with_no_mod(reify=(type_of_thing_that_is_to_be_added, reifier_fn))

    assert result == {'main': "main"}

def it_doesnt_augment_when_reifier_mod_has_no_reifier():
    result = reifyee_with_bad_mod(reify=(type_of_thing_that_is_to_be_added, reifier_fn))

    assert result == {'main': "main"}


@layer.reifier(reifier_module=sys.modules[__name__])
def reifyee(reify=None):
    return {'main': "main"}


@layer.reifier(reifier_module=None)
def reifyee_with_no_mod(reify=None):
    return {'main': "main"}

@layer.reifier(reifier_module=layer)
def reifyee_with_bad_mod(reify=None):
    return {'main': "main"}


#
# Helpers
#
def type_of_thing_that_is_to_be_added():
    """
    This stands in for the type of thing that the reifier will add.po
    :return:
    """
    pass

def type_of_thing_that_is_to_be_added_reifier(reifyee, fn):
    reifyee['added'] = fn()
    return reifyee

def reifier_fn():
    return 1