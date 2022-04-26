from tests.shared import *

from common.domain import constants
from key_management.domain import crypto
#
# Route = registration initiation
#
def test_successful_registration_initiation(api_registration_request_event,
                                            ssm_setup,
                                            dynamo_mock,
                                            set_up_key_management,
                                            set_up_env):
    #
    # Note, dont import the handle outside the test as it will attempt to initialise the env from ParameterStore
    # which will have yet to be mocked.
    #
    from functions.registration import handler as handler

    response = handler.handle(event=api_registration_request_event, context={})

    expected_body_part = '{"rp": {"name": "http://localhost:5000", "id": "localhost"}, "user": {"id": "c3ViamVjdDE", "name": "subject1", "displayName": "subject1"}'

    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == "application/json"
    assert expected_body_part in response['body']

def it_adds_a_cookie_referencing_the_registration(api_registration_request_event,
                                                  ssm_setup,
                                                  dynamo_mock,
                                                  set_up_key_management,
                                                  set_up_env):
    from functions.registration import handler as handler

    response = handler.handle(event=api_registration_request_event, context={})

    reg_session = response['multiValueHeaders']['Set-Cookie'][0].split(constants.SESSION_ID)[1]
    assert crypto.decrypt_secure_cookie(reg_session).get('regid', None)


#
# Route = registration completion
#
def it_handles_a_successful_registration_completion(api_completion_request_event,
                                                    ssm_setup,
                                                    dynamo_mock,
                                                    set_up_key_management,
                                                    set_up_env):
    from functions.registration import handler as handler

    event = set_up_event_and_reg(api_completion_request_event)

    response = handler.handle(event=event, context={})

    assert response['statusCode'] == 201
    assert response['headers']['Content-Type'] == "application/json"
    assert response['body'] == '{}'


#
# Helpers
#
def set_up_event_and_reg(event):
    challenge, request, model = create_webauthn_reg_in_created_state()
    mod_event = add_reg_cookie_to_event(event, model.uuid)
    mod_event['body'] = request
    return mod_event


def create_reg_in_created_state():
    challenge, request = registration_completion_usb()
    model = initiated_registration(challenge)
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