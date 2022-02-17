from typing import Dict
from pyfuncify import monad, app

from ..domain import registration, value
from common.typing.custom_types import Either

def initiate(event: app.ApiGatewayRequestEvent) -> Either[value.Registration]:
    result = new_registration(event) >> auth_factory >> initiate_registration
    return result

def new_registration(event: app.ApiGatewayRequestEvent) -> Either[value.Registration]:
    return monad.Right(registration.new(subject_name=event.path_params['subject']))

def auth_factory(registration_value: value.Registration) -> Either[value.Registration]:
    result = registration.registration_obligations(registration_value)

    return result

def initiate_registration(registration_value):
    result = registration.initiate(registration_value)
    if result.is_right():
        return result
    breakpoint()