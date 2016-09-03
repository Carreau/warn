import warn
warn.patch()

from examples.package2 import consumer
import warnings

print("=================================================================================")
print("Let's call the function package2.consumer() which call deprecated from package 1:\n")
consumer()
print("=================================================================================")
print()
print("=================================================================================")
print("Let's filter all warnings that arise in package 1:\n")
warnings.filterwarnings('default', category=DeprecationWarning, module='examples.package2')
consumer()
print("=================================================================================")
print()
print("=================================================================================")
print("Now let's activate all the warnings that come from package1\n")
warnings.filterwarnings('default', category=DeprecationWarning, emodule='examples.package1')
consumer()
print("=================================================================================")
print()
print("=================================================================================")
print("And ignore the one that come from the submodule bar\n")
warnings.filterwarnings('ignore',
    category=DeprecationWarning,
    emodule='examples.package1.bar')
consumer()
print("=================================================================================")
print()
