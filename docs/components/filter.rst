List filtering
--------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

While testing for file, you may find yourself in a situation where you only want to test subject which matches a given pattern.
That's what this component do.

How does it work?
^^^^^^^^^^^^^^^^^

We scan the list against the given pattern/regex and only test those who match it.

How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    filter: ""

to

::

    filter: "\.org"

(for example)


into your personal :code:`.PyFunceble.yaml` or use the :code:`--filter` argument from the CLI.