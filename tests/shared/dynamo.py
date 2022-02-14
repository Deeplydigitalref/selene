import pytest
import boto3
from moto import mock_dynamodb2

from common.util import env

@pytest.fixture
def dynamo_mock():

    mock_dynamodb2().start()

    from common.model.base_model import BaseModel

    if not BaseModel.exists():
        BaseModel.create_table()
        # add_gsi(boto3.client('dynamodb', region_name=env.Env.region_name))

    yield BaseModel

    mock_dynamodb2().stop()
