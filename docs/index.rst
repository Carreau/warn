
Welcome to warn's documentation!
================================


Warn is an experimental module which attempt to provide a more flexible and
powerful control over python warnings. It mainly allow you to not only filter
warnings depending on the module that trigger the warnings, but to filter
depending on where the warning come from.

Contents:

.. toctree::
   :maxdepth: 2

Direct Usage
------------

Replace your usual import of ``warnings.warn``, ``warnings.warn_explicit``  and
``warnings.filter`` by the same import from ``warn``, use them as usual except
you have some extra options.


To emit a warning:

.. code::
    :language: python

    import warn

    warn.warn("I can use the as usual; this is awesone", DeprecationWarning,
    stacklevel=1 )


To add a filter a warning, use the ``filter`` function as usual:


.. code:: 
    :language: python

    import warn

    warn.filter('default', DeprecationWarning, module='__main__')


Using as long as you do not use ``warn`` specific option, using ``warn.filter``
should have the exact same effect as calling ``warnings.filter`` and affect all
emitted warnings.





Import and usage Styleguide
===========================

Because of the experimental nature of this module, there is some strange
advised style guides. In particular you are encouraged to use the *fully
qualified* name when calling import, both when using the ``warn`` module as
well as when using the standard library ``warnings`` module. For example::

.. code::

    import warnings

    warnings.warn('This is a good way of using warning')

    ########

    from warnings import warn

    warn('Advance features of `warn` will not be available....')

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

