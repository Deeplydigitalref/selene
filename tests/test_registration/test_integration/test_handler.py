from key_management.domain import crypto


def test_successful_registration_initiation(api_registration_request_event,
                                            ssm_setup,
                                            dynamo_mock,
                                            set_up_env):
    #
    # Note, dont import the handle outside the test as it will attempt to initialise the env from ParameterStore
    # which will have yet to be mocked.
    #
    from functions.registration import handler as handler

    response = handler.handle(event=api_registration_request_event, context={})

    expected_body_part = '{"rp": {"name": "Example Co", "id": "example.com"}, "user": {"id": "c3ViamVjdDE", "name": "subject1", "displayName": "subject1"}'

    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == "application/json"
    assert expected_body_part in response['body']

def it_adds_a_cookie_referencing_the_regsitration(api_registration_request_event,
                                                  ssm_setup,
                                                  dynamo_mock,
                                                  set_up_env):
    from functions.registration import handler as handler

    response = handler.handle(event=api_registration_request_event, context={})

    reg_session = response['multiValueHeaders']['Set-Cookie'][0].split("seleneSession=")[1]
    assert crypto.validate_secure_cookie(reg_session).get('regid', None)
