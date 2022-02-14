import boto3
from pyfuncify import aws_client_helpers

from common.util import env

services = {'ssm': {},  'dynamodb': {'table': env.Env.dynamodb_table()}}

aws_client_helpers.AwsClientConfig().configure(region_name=env.Env.region_name,
                                               aws_client_lib=boto3,
                                               services=services)
