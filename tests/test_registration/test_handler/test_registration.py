import pytest
from datetime import datetime
from pyfuncify import span_tracer, chronos, app

from functions.registration.handlers import registration_initiation_handler
from common.util import env, parameter_store, error

def test_successful_response(api_registration_request_event,
                             ssm_setup,
                             s3_setup,
                             dynamo_mock,
                             set_up_env):

    response = registration_initiation_handler.handle(request_builder(api_registration_request_event))

    assert response.is_right()


#
# Failures
#

# Helpers

def request_builder(event):
    return app.Request(event=app.event_factory(event),
                       context={},
                       tracer=span_tracer.SpanTracer(env=env.Env.env, kv={}),
                       request_handler=None,
                       pip=None,
                       results=None,
                       response=None,
                       error=None)
