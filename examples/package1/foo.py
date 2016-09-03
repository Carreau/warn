import warnings

def func():
    warnings.warn('I do nothing but I am deprecated !', DeprecationWarning,
            stacklevel=2)
    return None
