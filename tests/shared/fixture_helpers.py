from . import dynamo

from common.domain import constants
from key_management.domain import crypto

def set_up_event_and_reg(event, registration):
    challenge, request, model = create_reg_in_created_state(registration)
    mod_event = add_reg_cookie_to_event(event, model.uuid)
    mod_event['body'] = request
    return mod_event


def create_reg_in_created_state(reg_complection):
    challenge, request = reg_complection
    model = dynamo.initiated_registration(challenge)
    return challenge, request, model


def add_reg_cookie_to_event(event, reg_uuid):
    from pyfuncify import app_web_session
    attrs = {'max-age': 60*5}
    cookie = (app_web_session.WebSession().set(constants.SESSION_ID, crypto.generate_secure_cookie({"regid": reg_uuid}), attrs)
                             .get(constants.SESSION_ID)
                             .serialise())
    # Lets assume the cookie will end up in the headers and not multiValueHeaders
    event['headers']['Cookie'] = cookie
    return event