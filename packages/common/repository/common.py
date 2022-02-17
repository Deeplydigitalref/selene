from typing import Tuple, Callable, Dict
from pyfuncify import monad, logger, chronos, aws_client_helpers

from ..model import base_model

class DbAction(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbAction, cls).__new__(cls)
            cls.actions = []
        return cls._instance

    def add(self, action, write_tester: Callable = None):
        self.actions.append((action, write_tester))
        pass

    def clear(self):
        self.actions = []
        pass

    def exec(self, ctx: Dict, tracer=None):
        with base_model.BaseModel.batch_write() as batch:
            for action in self.actions:
                self.save_action(batch, action, ctx)
        self.actions = []
        pass

    def save_action(self, batch, action: Tuple, ctx):
        model, write_tester = action
        if write_tester is None or (not callable(write_tester)):
            return batch.save(model)
        if write_tester(ctx):
            batch.save(model)
        pass


def table():
    return aws_client_helpers.aws_ctx().table
