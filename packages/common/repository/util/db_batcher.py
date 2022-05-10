from typing import Callable, Dict, Tuple
from pyfuncify import singleton, monad

from common.model import base_model

class DbBatchAction(singleton.Singleton):

    actions = []

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
        self.clear()
        pass

    def save_action(self, batch, action: Tuple, ctx):
        model, write_tester = action
        if self.do_write(write_tester, ctx):
            return batch.save(model)
        pass

    def do_write(self, write_tester, ctx) -> bool:
        return (write_tester is None or (not callable(write_tester))) or write_tester(ctx)

@monad.monadic_try()
def commit(ctx=None, tracer=None):
    DbBatchAction().exec(ctx=ctx, tracer=tracer)
    pass
