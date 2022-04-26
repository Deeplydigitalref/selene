from common.util import env
from key_management.domain import kek

def it_sets_the_current_kek_into_the_env(ssm_setup,
                                         set_up_env):

    assert env.Env.kek()

def it_encrypts_and_decrypts_data_with_the_kek(ssm_setup,
                                               set_up_env):

    token = kek.encrypt("hello")
    assert kek.decrypt(token) == "hello"