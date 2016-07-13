import warnings
def foo():
    warnings.warn("This is FOO", DeprecationWarning, stacklevel=2)
    
