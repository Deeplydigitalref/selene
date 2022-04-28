from pyfuncify import span_tracer, app, app_serialisers, app_value
from webauthn.helpers import structs

from functions.registration.handlers import registration_initiation_handler
from functions.registration.handlers import registration_completion_handler
from common.domain.subject import registration, value, subject
from common.util import serialisers

from tests.shared import *

def setup_module():
    set_up_key_management

#
# Registration Initiation
#
def test_successful_response(api_registration_request_event,
                             ssm_setup,
                             dynamo_mock,
                             set_up_key_management,
                             set_up_env):
    request = request_builder(api_registration_request_event)

    response = request.event.request_function(request)

    assert response.is_right()
    assert response.value.response.is_right()


def test_returns_a_serialisable_result(api_registration_request_event,
                                       ssm_setup,
                                       s3_setup,
                                       dynamo_mock,
                                       set_up_key_management,
                                       set_up_env):
    request = request_builder(api_registration_request_event)

    result = request.event.request_function(request).value.response.value

    assert isinstance(result, serialisers.WebAuthnRegistrationSerialiser)

    serialised_result = result.serialise()

    assert '"user": {"id": "c3ViamVjdDE", "name": "subject1", "displayName": "subject1"}' in serialised_result


def test_provides_registration_options_for_return(api_registration_request_event,
                                                  ssm_setup,
                                                  dynamo_mock,
                                                  set_up_key_management,
                                                  set_up_env):
    request = request_builder(api_registration_request_event)

    reg_opts = request.event.request_function(request).value.response.value.serialisable

    assert reg_opts.subject_name == 'subject1'
    assert isinstance(reg_opts.registration_options, structs.PublicKeyCredentialCreationOptions)
    assert reg_opts.state == value.RegistrationStates.CREATED


#
# Registration Completion
#
def it_handles_a_successful_registration_completion(api_completion_request_event,
                                                    ssm_setup,
                                                    dynamo_mock,
                                                    set_up_key_management,
                                                    set_up_env):
    request = request_builder(set_up_event_and_reg(api_completion_request_event, registration_completion_usb()))

    result = request.event.request_function(request)

    assert result.is_right()
    assert result.value.status_code == app_value.HttpStatusCode.CREATED
    assert result.value.response.is_right()
    assert result.value.response.value.serialise() == '{}'


def it_sets_the_webauthn_reg_to_complete(api_completion_request_event,
                                         ssm_setup,
                                         dynamo_mock,
                                         set_up_key_management,
                                         set_up_env):
    request = request_builder(set_up_event_and_reg(api_completion_request_event, registration_completion_usb()))

    result = request.event.request_function(request)

    reg = registration.get(result.value.results.uuid)

    assert reg.is_right()
    assert reg.value.state == value.RegistrationStates.COMPLETED


def it_creates_a_new_person_subject(api_completion_request_event,
                                    ssm_setup,
                                    dynamo_mock,
                                    set_up_key_management,
                                    set_up_env):
    request = request_builder(set_up_event_and_reg(api_completion_request_event, registration_completion_usb()))

    result = request.event.request_function(request)

    reg = registration.get(result.value.results.uuid, reify=(value.Subject, subject.from_registration))

    assert reg.is_right()
    assert reg.value.subject.state == value.SubjectStates.CREATED
    assert reg.value.subject.is_class_of == value.SubjectClass.PERSON


#
# Failures
#

# Helpers
@app.route(('API', 'GET', '/registration/makeCredential/{subject}'))
def reg_invoker(request):
    return registration_initiation_handler.handle(request)


@app.route(('API', 'POST', '/registration/makeCredential'), opts={'body_parser': app_serialisers.json_parser})
def complete_invoker(request):
    return registration_completion_handler.handle(request)


def request_builder(event):
    return app.Request(event=app.event_factory(event),
                       context={},
                       tracer=span_tracer.SpanTracer(env=env.Env.env, kv={}),
                       request_handler=None,
                       pip=None,
                       results=None,
                       response=None,
                       error=None)
