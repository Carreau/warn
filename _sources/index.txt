
Welcome to warn's documentation!
================================


Warn is an experimental module which attempt to provide a more flexible and
powerful control over python warnings. It mainly allow you to not only filter
warnings depending on the module that trigger the warnings, but to filter
depending on where the warning come from.

Direct Usage
------------

Replace your usual import of ``warnings.warn``, ``warnings.warn_explicit``  and
``warnings.filter`` by the same import from ``warn``, use them as usual except
you have some extra options.


To emit a warning:

.. code::

    import warn

    warn.warn("I can use the as usual; this is awesone",
              DeprecationWarning,
              stacklevel=1 )


To add a filter a warning, use the ``filter`` function as usual:


.. code::

    import warn

    warn.filter('default', DeprecationWarning, module='__main__')


Using as long as you do not use ``warn`` specific option, using ``warn.filter``
should have the exact same effect as calling ``warnings.filter`` and affect all
emitted warnings.


Extra Functionality
-------------------

The main extra functionality of the `warn` module is to be able to filter
warnings not only by what _trigger_ them, but what _emit_ them. For example:

.. code::

    # dependency.py

    import warn

    def deprecated_function():
        # the warning is emitted here
        warn.warning("I am a deprecation warning",
                     DeprecationWarning,
                     stacklevel=2


.. code::

    # downstream.py

    from dependency import deprecated_function

    def feature():
        # I will trigger the warning.
        deprecated_function()


While the Python standard library only allow to filter by the module that
_trigger_ the warning (above ``downstream`` module, and this only if
``deprecated_function`` set the ``stacklevel`` correctly, ``warn`` allows you
to filter depending on the _emitter_ module (here ``dependency``). To do so use
the ``emodule`` keyword of ``warn.filter``, which take a string or a regular
expression:

.. code::

    import warn

    warn.filterwarnings('error', DeprecationWarning, emodule='dependency')


Monkey Patching the standard library
------------------------------------

The functionality of warn are usually only available if you are explicitly use
the ``warn`` exposed functions. Though it might be useful occasionally to use
the warn functionality with module that uses the standard library ``warnings``.

For this use case we provide the ``patch`` function that will replace
monkey patch the standard library and automatically provide ``warn``'s function
to all modules that get imported **after** the patch have been applied.

The ``teardown`` function is also provided and attempt to un-patch the
``warnings``. Though any module that have retain a reference to the ``warn``,
``warn_explicit`` and ``filter`` function will still be using the ``warn``
module functionalities.

``patch`` and ``teardown`` keep a reference count of how many time each have
been called to un-patch only when necessary, it should thus be safe to nest
calls.

``patch`` can also be used as a context manager to automatically un-patch on
context manager exit.


Import and usage Styleguide
---------------------------

Because of the experimental nature of this module, there is some strange
advised style guides. In particular you are encouraged to use the *fully
qualified* name when calling import, both when using the ``warn`` module as
well as when using the standard library ``warnings`` module. For example:

.. code::

    import warnings

    warnings.warn('This is a good way of using warning')

    ########

    from warnings import warn

    warn('Advance features of `warn` will not be available....')


Monkey patch and compiled module
--------------------------------

Compiles modules directly access the C-implementation of the ``warning``
module. Monkey Patching thus have no effect. We are aware of the limitation.

How does it work
----------------

Python's warning filter are required to be fives-tuples with restricted types
and values, in particular to be compatible with efficient c-implementation of
the python standard lib.

In order to interoperate with standard library ``warnings``, when using
specific ``warn``'s functionality we actually inject a phony five-tuple which
is no-op into ``warnings.filters`` and use it as a key for a proxy-dict that
store the actual parameters.

This allows complete backward compatibility with the warn module and ensure
that in the worse case scenario, the rules you set using the ``warn`` module
just have no-effects.

We would really welcome any modification into Core Python that allow to have
custom warning filters to make this less hackish.


When to use ``warn``
--------------------

``Warn`` is still experimental and we do not yet recommend it for production.
First as this is a pure python implementation, depending on the number of
warning your code base have, you may notice a performance decrease.

``Warn`` is extremely interesting for integration-testing and unit testing. We
in particular recommend selectively enabling warning-as-error for all your
direct dependencies. This is usually feasible with the default python warning
module, except when warning are raised at import time, or if the underlying
library does not make use of the ``stacklevel`` keyword. More generally you
might want to consider enabling warning-as-error globally and silence them on a
module-by-module basis if you decide they are false positive.

``Warn`` is also extremely useful while developing locally to make sure you
develop your code as early possible without using functionality that might be
removed in the near future.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

