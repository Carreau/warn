from warnings import warn

def foo():
    warn("This is FOO", DeprecationWarning, stacklevel=2)

def bar():
    foo()
    
