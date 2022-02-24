import pytest
from moto import mock_dynamodb2
import uuid

@pytest.fixture
def dynamo_mock():

    mock_dynamodb2().start()

    from common.model.base_model import BaseModel

    if not BaseModel.exists():
        BaseModel.create_table()
        # add_gsi(boto3.client('dynamodb', region_name=env.Env.region_name))

    yield BaseModel

    mock_dynamodb2().stop()


def initiated_registration(challenge):
    from common.util import encoding_helpers
    from common.repository import registration
    from key_management.domain import crypto
    model = registration.RegistrationModel(uuid=str(uuid.uuid4()),
                                           subject_name="subject1",
                                           registration_state="CREATED",
                                           registration_challenge=encoding_helpers.base64url_to_bytes(challenge))
    registration.create(model)
    return model
