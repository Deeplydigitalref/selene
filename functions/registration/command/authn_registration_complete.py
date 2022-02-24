from pyfuncify import monad, app
from pymonad.tools import curry

from ..domain import registration, value
from common.typing.custom_types import Either
from common.domain import constants
from key_management.domain import crypto


def invoke(event: app.ApiGatewayRequestEvent) -> Either[value.Registration]:
    result = get_registration(event) >> validate_registration(event) >> complete_registration >> set_session
    return result

def get_registration(event: app.ApiGatewayRequestEvent) -> Either[value.Registration]:
    reg = registration.get(retrieve_session_token(event.web_session))
    return reg

@curry(2)
def validate_registration(event: app.ApiGatewayRequestEvent, registration_value: value.Registration) -> Either[value.Registration]:
    result = monad.Right(registration.validation(event.body, registration_value))
    breakpoint()


def complete_registration(registration_value: value.Registration) -> Either[value.Registration]:
    result = registration.initiate(registration_value)
    if result.is_right():
        return result
    breakpoint()

#
# Helpers
#

def set_session(registration_value: value.Registration) -> Either[value.Registration]:
    registration_value.registration_session = session_token(registration_value.uuid)

    return monad.Right(registration_value)

def retrieve_session_token(web_session) -> str:
    return web_session.get(constants.SESSION_ID, decrypt_and_extract_reg_id).value()

def decrypt_and_extract_reg_id(cookie_value: str) -> str:
    return crypto.decrypt_secure_cookie(cookie_value).get('regid', None)