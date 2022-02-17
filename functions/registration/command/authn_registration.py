from typing import Dict
from pyfuncify import monad, app

from ..domain import registration, webauthn_registration
from common.typing.custom_types import Either

def initiate(event: app.ApiGatewayRequestEvent) -> Either[registration.Registration]:
    result = new_registration(event) >> auth_factory >> initiate_registration

    breakpoint()

def new_registration(event: app.ApiGatewayRequestEvent) -> Either[registration.Registration]:
    return monad.Right(registration.new(subject_name=event.path_params['subject']))

def auth_factory(registration_value: registration.Registration) -> Either[registration.Registration]:
    result = webauthn_registration.registration_obligations(registration_value)

    return result

def initiate_registration(registration_value):
    result = registration.initiate(registration_value)
    if result.is_right():
        return result
    breakpoint()