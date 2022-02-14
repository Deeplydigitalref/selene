from pyfuncify import aws_client_helpers, parameter_store

from . import env

def set_env_from_parameter_store():
    parameter_store.set_env_from_parameter_store(path=parameter_path(), ssm_client=ssm_client())
    pass

def parameter_path() -> str:
    return "{}/environment/".format(env.Env.parameter_store_path())
#
def ssm_client():
    return aws_client_helpers.aws_ctx().ssm
