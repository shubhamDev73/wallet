from functools import wraps

def transaction(function):
    def wrap(*args, **kwargs):
        return function(*args, **kwargs)
    wrap.transaction = True
    return wraps(function)(wrap)
