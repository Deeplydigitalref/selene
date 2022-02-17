import pytest
from pyfuncify import span_tracer, chronos, app
from webauthn.helpers import structs

from functions.registration.handlers import registration_initiation_handler
from functions.registration.domain import registration
from common.util import env, parameter_store, error

def test_successful_response(api_registration_request_event,
                             ssm_setup,
                             s3_setup,
                             dynamo_mock,
                             set_up_env):
    request = request_builder(api_registration_request_event)

    response = request.event.request_function(request)

    assert response.is_right()
    assert response.value.response.is_right()

def test_creates_a_registration(api_registration_request_event,
                                ssm_setup,
                                s3_setup,
                                dynamo_mock,
                                set_up_env):
    request = request_builder(api_registration_request_event)

    reg = request.event.request_function(request).value.response.value

    assert reg.subject_name == 'subject1'
    assert isinstance(reg.registration_options, structs.PublicKeyCredentialCreationOptions)
    assert reg.registration_state == registration.RegistrationStates.CREATED



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
