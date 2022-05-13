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


def reifier(reifier_module=None):
    def inner(fn):
        def try_it(*args, **kwargs):
            reify = kwargs.get('reify', None)
            fn_result = fn(*args, **kwargs)

            if reify:
                cls, reify_fn = reify
                return reify_token_caller(cls, reifier_module)(fn_result, reify_fn)
            return fn_result
        return try_it
    return inner

def reify_token_caller(cls, mod: Callable):
    if not mod or not cls:
        return default_identity_fn
    callable = "{}_reifier".format(cls.__name__.lower())
    if hasattr(mod, callable):
        return getattr(mod, callable)
    return default_identity_fn


def default_identity_fn(result, _reifier):
    return result

