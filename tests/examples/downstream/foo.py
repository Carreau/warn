from ..dependency import func, func2
import warnings

def consumer():
    warnings.warn('Consumer is deprecated', DeprecationWarning, stacklevel=2)
    func()
    func2()
    print("consumer called")
