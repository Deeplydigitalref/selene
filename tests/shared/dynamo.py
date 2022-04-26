import pytest
from moto import mock_dynamodb
import uuid


@pytest.fixture
def dynamo_mock():
    mock_dynamodb().start()

    from common.model.base_model import BaseModel
    if not BaseModel.exists():
        BaseModel.create_table()
        # add_gsi(boto3.client('dynamodb', region_name=env.Env.region_name))

    yield BaseModel

    mock_dynamodb().stop()
