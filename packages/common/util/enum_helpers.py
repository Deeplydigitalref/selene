from enum import EnumMeta
from pyfuncify import monad

class DefaultEnumMeta(EnumMeta):
    def __call__(cls, value=None, *args, **kwargs):
        if (value is None or not cls.value_in_range(value)) and (cls.has_default_set()):
            return cls.default
        return super().__call__(value, *args, **kwargs)

    def either(cls, value=None) -> monad.EitherMonad:
        try:
            return monad.Right(cls(value))
        except Exception as e:
            return monad.Left(None)

    def has_default_set(cls):
        return hasattr(cls, 'default')

    def value_in_range(cls, value):
        return value in list(map(lambda e: e.value, iter(cls)))
