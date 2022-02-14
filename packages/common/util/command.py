from typing import Callable, Any
from pyfuncify import monad
from pymonad.tools import curry

from . import error

"""
Common Command Functions
"""

def try_success_unwrapper(result):
    """
    Each controller returns an Either, as does the monadic_try decorator.  A success result is TryEither(CommandEither(result))
    A Try exception only returns 1 layer of Either.
    Unwrap the success Either so that there is only the CommandEither
    """
    if result.is_left():
        return result
    return result.value

@curry(2)
def add_error_to_event(value, result):
    """
    Takes the value and the unexpected exception and adds the exception to the error arg.
    """
    if not value:
        return result
    return monad.Left(value.replace('error', result.error()))


@monad.monadic_try(status=500, exception_test_fn=try_success_unwrapper, error_cls=error.UnExpectedServiceException, error_result_fn=add_error_to_event)
def try_command(command: Callable, value: Any, tracer=None, error_result_fn_arg=None):
    """
    :param command: Callable.  The command fn must have the value object as the first arg.
    :param value: Any value Object to be passes as the main arg to the command
    :param tracer:
    :param error_result_fn_arg:
    :return: Either wrapped result of calling command with value
             In the case of an exception, the result of applying the error and error_result_arg to the error_result_fn
    """
    return command(value, tracer)
