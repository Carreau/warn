# warn

Better warnings. 

The Python standard [warning
module](https://docs.python.org/3/library/warnings.html) is extremely good, and
I believe underutilized; Though it missed a few functionality; in particular it
allows filtering only on the code that triggered/called a deprecated functions,
but have no ability to filter depending on the module that emitted the warning. 

This is an attempt to fix that.

## Too long didn't read:

Explicit is better than implicit:

```
from warn import patch
patch()

# use the warning module as usual
```

Though the `warnings.filterwarning` function has now gained the `emodule`
keyword parameter to filer by the module that emitted the warning; example:

```
import warnings
warnings.filter('default', category=DeprecationWarnings, emodule='matplotlib\.pyplot.*')
```

All warnings from `matplotlib.pyplot` and its submodule will now be show by
default, regardless of whether you trigger them directly, via pandas, seaborn,
your own code...

## Warning emitter, warning caller. 

Python warnings are a beautiful relative simple piece of code which is
extremely powerful in the right hands once you learned how to use it. 

It allows you to determine a posteriori whether you want a particular piece of
code to trigger an exception, display a message to the user or simply do
nothing. 

It is difficult to show the full power of the waring with a simple piece of
code, but in large code base, and once you start having several layer of
dependency a parsimonious usage of warning , and in particular
`DeprecationWarning` can make a large difference. 

### Caller, vs Emitter

Let's clear up some vocabulary first, to differentiate the warning "Caller" from the warning "Emitter"

```python
# file emitter.py

def public_api(param1, deprecated_parameter=None)::

    if deprecated_parameter:
        return _deprecated_function(param1, deprecated_parameter):
    else:
        return normal_buisnell_logic(param1)


def _deprecated_function(param1, deprecated_parameter):
    import warningsA
    # warning emitted here
    warnings.warn('using `deprecated_parameter` is deprecated ',
            DeprecationWarning,
            stacklevel=3)
```

```python
# file caller.py
from emitter import public_api
public_api(1, True)  # warning triggered here.
```

you can now do something like

```python
from warn import path
patch()

import warnings
warnings.filter('default', category=DeprecationWarnings, emodule='emitter.*')
import emitter
emitter.bar() # will log the warning !
```

Change this to "error" in your test-suite, and filter by all your dependencies !

The Python built-in module allow you to filter warning by caller (assuming the
emitter have set the `stacklevel` options right, which is not always obvious to
do). This is extremely useful when you are developing the caller; but not that
much when you are developing the emitter. 

It is common for a caller to actually have many underlying library the can
trigger warnings, or for a developer to only care about a subset of the emitter
warnings. 

Many libraries are going around this limitation by sub-classing Warnings; two
example are
[Matplolib](https://github.com/matplotlib/matplotlib/blob/d158587a3cd50df3835d3d65a159c08b37b17f43/lib/matplotlib/cbook.py#L36-L47)
and
[sympy](https://github.com/sympy/sympy/blob/deeb5ac6789f97abd4846e03e9f2b2fced384262/sympy/utilities/exceptions.py)
in order to selectively enable them. Still this only give a coarse way of
filtering warnings, and it required to know where the warnings are defined in
order to import and filter for them.

Because of Python default choice to filter out deprecation warnings, this also
forced either inherit `UserWarning` (choice of matplotlib), which removes the
semantic meaning of `DeprecationWarning` offered by Python or to inject a
custom filter in the warnings filter module on import (choice of Sympy), which
can lead to surprising behavior. 

## Usage without patching 

TODO. You should be able to use that in your own library without using `patch()`


## Availability on Python 2

I don't know if if works on Python 2; I don't really have the time to
investigate; I don't particularly care a lot; but feel free to send a PR that
ads support if necessary.


## limitations

This does not work on packages that either :

- Got and keep a reference on `warnings.warn` before `patch()` have been
  called; that is to say things of the form: `from warnings iport warn`

- Cannot work on C-extensions (aka won't filter on `numpy`) ; Both of the above
  are technically possible with Assembly Patching which I'm not confortable
  with.

## The Ugly

- as Warnings filters _have to be 5 tuples with specific types_ this works by
  shoving dummy instances in the filters list and using this as keys for a
  proxy to lookup real filter keys. So worse case scenario the filter you
  insert with this module will just be no-op. But you will incur a performance
  penalty if you use this, especially if your codebase triggers a lot of
  warnings.

## Get the upstream

I'd **love** feedback and have a nicer API to deal with warnings at CPython
level in order to provide custom filters, and custom filters functions.

# Aparté 

## Good Deprecation Warnings.

A good warning and in particular Deprecation warning
is extremely helpful and can make the difference for the adoption of an API.
Take the following fiction example:

```python
>>> import warnings

>>> warnings.simplefilter('default')

>>> from quezetraste import frobulate, constribule

>>> frobulate('HI', 3)
DeprecationWarning: The 'frobulate' function is deprecated.

>>> contribule('Hi', 3)

DeprecationWarning: The 'constribule(message, recipient_id)' function of the
                    'quezetraste' package is deprecated since version 7.3. It
                    haz been replaced by 'Recipient(id).send(message)' which
                    was available since 7.2. See http://url.to/documentation/#1337
```


## Turn the DeprecationWarnings into error in your test-suite!

At least  make them visible; at best once you fixed a deprecation warning turn
**this specific one** into an error to not reproduce it. 
