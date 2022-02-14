import pytest
import boto3
from moto import mock_s3

from common.util import env


# Creates an S3 object using a fixed template
@pytest.fixture
def s3_setup():
    mock = mock_s3()
    mock.start()
    conn = boto3.resource('s3', region_name=env.Env.region_name)
    conn.create_bucket(Bucket='auth.uat.reference.io')
    yield
    mock.stop()

