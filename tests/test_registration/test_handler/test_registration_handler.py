import pytest
from pyfuncify import span_tracer, chronos, app
from webauthn.helpers import structs

from functions.registration.handlers import registration_initiation_handler
from functions.registration.domain import value
from common.util import env, serialisers

def test_successful_response(api_registration_request_event,
                             ssm_setup,
                             dynamo_mock,
                             set_up_env):
    request = request_builder(api_registration_request_event)

    response = request.event.request_function(request)

    assert response.is_right()
    assert response.value.response.is_right()

def test_returns_a_seialisable_result(api_registration_request_event,
                                ssm_setup,
                                s3_setup,
                                dynamo_mock,
                                set_up_env):

    request = request_builder(api_registration_request_event)

    result = request.event.request_function(request).value.response.value

    assert isinstance(result, serialisers.WebAuthnSerialiser)

    serialised_result = result.serialise()

    assert '"user": {"id": "c3ViamVjdDE", "name": "subject1", "displayName": "subject1"}' in serialised_result

def test_provides_registration_options_for_return(api_registration_request_event,
                                                  ssm_setup,
                                                  dynamo_mock,
                                                  set_up_env):

    request = request_builder(api_registration_request_event)

    reg_opts = request.event.request_function(request).value.response.value.serialisable

    assert reg_opts.subject_name == 'subject1'
    assert isinstance(reg_opts.registration_options, structs.PublicKeyCredentialCreationOptions)
    assert reg_opts.registration_state == value.RegistrationStates.CREATED



#
# Failures
#

# Helpers
@app.route(('API', 'GET', '/registration/makeCredential/{subject}'))
def invoker(request):
    return registration_initiation_handler.handle(request)

def request_builder(event):
    return app.Request(event=app.event_factory(event),
                       context={},
                       tracer=span_tracer.SpanTracer(env=env.Env.env, kv={}),
                       request_handler=None,
                       pip=None,
                       results=None,
                       response=None,
                       error=None)
