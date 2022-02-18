from typing import Tuple, Any
from pyfuncify import monad, app

from common.util import error, env

from .handlers import registration_initiation_handler

# Warm Start Pattern
from common.initialisers import aws_client_setup, parameter_store

def handle(event: dict, context: dict) -> dict:
    return app.pipeline(event=event,
                        context=context,
                        env=env.Env().env,
                        params_parser=request_builder,
                        pip_initiator=pip,
                        handler_guard_fn=check_env_established)


# Handles /registration/makeCredential/subject1
@app.route(('API', 'GET', '/registration/makeCredential/{subject}'))
def registration_initiation(request: app.RequestEvent) -> monad.MEither:
    return registration_initiation_handler.handle(request=request)


@app.route('no_matching_route')
def noop_event(request):
    return monad.Right(request.replace('response', monad.Right(app.DictToJsonSerialiser({}))))


def request_builder(request) -> monad.Either:
    """
    Takes the middleware request and transforms it as necessary before invoking the handler.

    In this case, no transformations are performed.
    """
    return monad.Right(request)


def pip(request):
    """
    No PIP injected as the only route is from S3.

    :param request:
    :return: Either

    """
    return monad.Right(request)


# Guard Condition for the entire function to execute.
def check_env_established(event: dict) -> Tuple[bool, Any]:
    if env.Env.expected_set():
        return monad.Right(None)
    return monad.Left(error.EnvironmentNotSetup(message="Env expectations failure", code=500))
