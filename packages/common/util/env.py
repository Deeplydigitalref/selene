import os
from typing import List, Tuple

# Global Object
class Env:
    env = os.environ.get('ENVIRONMENT', default=None)

    region_name = os.environ.get('REGION_NAME', default='ap-southeast-2')

    expected_envs = ['dynamo_table_name']


    @staticmethod
    def parameter_store_path():
        return os.environ.get('PARAMETER_STORE_PATH', default=None)


    @staticmethod
    def dynamodb_table():
        # When in test the table might not have been setup from the env
        if Env.test() and os.environ.get('DYNAMODB_TABLE_NAME', None) is None:
            os.environ['DYNAMODB_TABLE_NAME'] = 'auth.reference.io'

        return os.environ.get('DYNAMODB_TABLE_NAME', default=None)


    @staticmethod
    def development():
        return Env.env == "development"

    @staticmethod
    def test():
        return Env.env == "test"

    @staticmethod
    def production():
        return not (Env.development() or Env.test())

    @staticmethod
    def expected_set():
        return all(getattr(Env, var)() for var in Env.expected_envs)

    def set_env_var_with_value(self, name: str, value: str) -> Tuple[str, str, str]:
        """
        Sets an ENV variable from a key/value pair
        """
        os.environ[name] = value
        return ('ok', name, value)



def set_env(parameters: List[dict]):
    return monad.Right(list(map(set_env_var, parameters['Parameters'])))

def set_env_var_with_parameter(parameter: dict) -> Tuple:
    """
    Sets an ENV variable from the parameter store data structure
    """
    name = parameter['Name'].split("/")[-1]
    os.environ[name] = parameter['Value']
    return monad.Right(('ok', name, parameter['Value']))

def set_env_var_with_value(name: str, value: str) -> Tuple[str, str, str]:
    """
    Sets an ENV variable from a key/value pair
    """
    os.environ[name] = value
    return ('ok', name, value)
