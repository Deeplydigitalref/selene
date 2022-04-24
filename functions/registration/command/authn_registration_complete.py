from pyfuncify import monad, app
from pymonad.tools import curry

from common.domain.subject import registration, value
from common.domain import constants
from key_management.domain import crypto


def invoke(event: app.ApiGatewayRequestEvent) -> monad.EitherMonad[value.Registration]:
    result = get_registration(event) >> complete_registration(event) >> clear_session(event)
    return result

def get_registration(event: app.ApiGatewayRequestEvent) -> monad.EitherMonad[value.Registration]:
    reg = registration.get(retrieve_session_token(event.web_session))
    reg.value.registration_session = event.web_session
    return reg

@curry(2)
def complete_registration(event: app.ApiGatewayRequestEvent, registration_value: value.Registration) -> monad.EitherMonad[
    value.Registration]:
    result = registration.complete_registration(event.body, registration_value)
    if result.is_right():
        return result
    breakpoint()


# def onboard_subject(registration_value: value.Registration) -> monad.EitherMonad[value.Registration]:
#     result = subject.new_from_registration(registration_value)
#     if result.is_right():
#         return monad.Right(registration_value)
#     breakpoint()

@curry(2)
def clear_session(event: app.ApiGatewayRequestEvent, registration_value: value.Registration):
    registration_value.registration_session.clear_all()
    return monad.Right(registration_value)

#
# Helpers
#

def retrieve_session_token(web_session) -> str:
    return web_session.get(constants.SESSION_ID, decrypt_and_extract_reg_id).value()

def decrypt_and_extract_reg_id(cookie_value: str) -> str:
    return crypto.decrypt_secure_cookie(cookie_value).get('regid', None)