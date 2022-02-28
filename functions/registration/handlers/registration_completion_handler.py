import uuid
from typing import Dict
from pymonad.tools import curry

from pyfuncify import fn, monad, logger, app, app_value

from common.typing.custom_types import Either
from common.util import serialisers

from .. import command


_CTX = {}

instrumentables = []

"""
"""

def handle(request: app.RequestEvent) -> Either:
    _CTX['tracer'] = request.tracer

    result = complete_registration(request) >> session_and_response
    return result

def complete_registration(request: app.RequestEvent) -> Either[app.RequestEvent]:
    result = command.authn_registration_complete.invoke(request.event)
    if result.is_right():
        request.results = result.value
    else:
        breakpoint()
    return monad.Right(request)


def session_and_response(request: app.RequestEvent) -> Either[app.RequestEvent]:
    """
    The registration session is set in the domain value.  This is copied to the request value as the new
    web session to be set, and the WebAuthnRegistrationSerialiser is injected to enable the response body creation
    from the registration.

    :param request:
    :return: Either[request]
    """
    request.status_code = app_value.HttpStatusCode.CREATED
    request.event.web_session = request.results.registration_session
    request.response = monad.Right(serialisers.WebAuthnRegistrationCompletionSerialiser(request.results))
    return monad.Right(request)

#
# Helpers
#
