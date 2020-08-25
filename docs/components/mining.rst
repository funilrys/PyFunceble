Mining
------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

Sometimes you might, for example, want to get the list of domain(s) / URL(s) in a redirecting loop.
This feature reveals them.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here :func:`PyFunceble.engine.mining.Mining`!

We access the given domain/URL and get the redirection history which we then test once we finished the normal test.


.. note::
    This component might evolve with time.

How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    mining: False

to

::

    mining: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--mining` argument from the CLI to activate it.
