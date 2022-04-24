from pyfuncify import monad, app, app_web_session

from common.domain.subject import registration, value
from common.domain import constants
from key_management.domain import crypto


def invoke(event: app.ApiGatewayRequestEvent) -> monad.EitherMonad[value.Registration]:
    result = new_registration(event) >> auth_factory >> initiate_registration >> set_session
    return result

def new_registration(event: app.ApiGatewayRequestEvent) -> monad.EitherMonad[value.Registration]:
    return monad.Right(registration.new(subject_name=event.path_params['subject']))

def auth_factory(registration_value: value.Registration) -> monad.EitherMonad[value.Registration]:
    result = registration.registration_obligations(registration_value)

    return result

def initiate_registration(registration_value: value.Registration) -> monad.EitherMonad[value.Registration]:
    result = registration.initiate(registration_value)
    if result.is_right():
        return result
    breakpoint()

def set_session(registration_value: value.Registration) -> monad.EitherMonad[value.Registration]:
    registration_value.registration_session = build_session_token(registration_value.uuid)

    return monad.Right(registration_value)

def build_session_token(uuid):
    return app_web_session.WebSession().set(constants.SESSION_ID, crypto.generate_secure_cookie({"regid": uuid}))
