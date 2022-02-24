import uuid
from typing import Dict
from pymonad.tools import curry

from pyfuncify import fn, monad, logger, app

from common.typing.custom_types import Either
from common.util import serialisers

from .. import command


_CTX = {}

instrumentables = []

"""
"""

def handle(request: app.RequestEvent) -> Either:
    _CTX['tracer'] = request.tracer

    result = complete_registration(request) >> to_result
    return result

def complete_registration(request) -> Either[app.RequestEvent]:
    result = command.authn_registration_complete.invoke(request.event)
    if result.is_right():
        request.event.web_session = result.value.registration_session
        request.response = monad.Right(serialisers.WebAuthnSerialiser(result.value))
    else:
        breakpoint()
    return monad.Right(request)


def to_result(request) -> Either[app.RequestEvent]:
    return monad.Right(request)

#
# Helpers
#
