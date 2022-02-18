from typing import Dict
from pyfuncify import monad, app, app_web_session
from http import cookies

from ..domain import registration, value
from common.typing.custom_types import Either
from common.util import crypto

def initiate(event: app.ApiGatewayRequestEvent) -> Either[value.Registration]:
    result = new_registration(event) >> auth_factory >> initiate_registration >> set_session
    return result

def new_registration(event: app.ApiGatewayRequestEvent) -> Either[value.Registration]:
    return monad.Right(registration.new(subject_name=event.path_params['subject']))

def auth_factory(registration_value: value.Registration) -> Either[value.Registration]:
    result = registration.registration_obligations(registration_value)

    return result

def initiate_registration(registration_value: value.Registration) -> Either[value.Registration]:
    result = registration.initiate(registration_value)
    if result.is_right():
        return result
    breakpoint()

def set_session(registration_value: value.Registration) -> Either[value.Registration]:
    registration_value.registration_session = session_token(registration_value.uuid)

    return monad.Right(registration_value)

def session_token(uuid):
    return app_web_session.WebSession().set("seleneSession", crypto.generate_secure_cookie({"regid": uuid}))
