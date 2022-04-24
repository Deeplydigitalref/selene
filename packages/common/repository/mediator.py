from typing import Callable, Dict

from pyfuncify import singleton

class DbAction(singleton.Singleton):

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

def commit(ctx=None, tracer=None):
    DbAction().exec(ctx=ctx, tracer=tracer)
    pass
