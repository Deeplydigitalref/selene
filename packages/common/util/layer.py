from typing import Callable, Any


def finaliser(finaliser_fn: Callable):
    """
    """
    def inner(f):
        def post_processor(*args, **kwargs):
            # x = {'fin': finaliser_fn, 'f': f, 'args': args}
            finaliser_args, result = f(*args, **kwargs)
            return finaliser_fn(finaliser_args, result)
        return post_processor
    return inner

