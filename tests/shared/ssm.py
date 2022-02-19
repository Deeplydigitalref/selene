import pytest
import boto3
from moto import mock_ssm
import os

from pyfuncify import aws_client_helpers

from common.util import env, parameter_store
from key_management.domain import kek

@pytest.fixture
def ssm_empty_setup():
    mock = mock_ssm()
    mock.start()
    yield
    mock.stop()


@pytest.fixture
def ssm_setup():
    mock = mock_ssm()
    mock.start()
    set_up_parameter_store('all')
    yield
    mock.stop()


def set_up_parameter_store(depth):
    ssm = boto3.client('ssm', region_name=env.Env.region_name)
    ssm.put_parameter(Name="{}/environment/DYNAMODB_TABLE".format(env.Env.parameter_store_path()), Value="selenedb", Type="String")
    ssm.put_parameter(Name="{}/environment/KEK".format(env.Env.parameter_store_path()), Value=kek.create_kek(), Type="String")


@pytest.fixture
def set_up_env():
    """
    We need to set up the AWS CTX object after all the mocking has been done.
    Then we hit the mock parameter store to set up the env params.

    This is done by running the initialisers
    """
    from common.initialisers import aws_client_setup, parameter_store
    pass


@pytest.fixture
def clear_env():
    pass

