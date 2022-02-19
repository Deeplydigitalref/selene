from common.util import env

def it_sets_the_current_kek_into_the_env(ssm_setup,
                                         set_up_env):

    assert env.Env.kek()
