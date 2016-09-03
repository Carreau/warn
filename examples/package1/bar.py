import warnings

def func2():
    warnings.warn("I don't set the right stacklevel and I am deprecated !", DeprecationWarning)
    return None

