Complements Generation
----------------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

Let's say we have :code:`example.org` but :code:`www.example.org`
(or vice-versa) is not into my list.
This component (if activated) let us test :code:`www.example.org`
(or vice-versa) even if it's not into the input list.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here
    :class:`~PyFunceble.converter.subject2complements.Subject2Complements`!

At the end of the normal test process, we generate the list of complements and
test them.

How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    cli_testing:
        # Activates the generation of complements.
        complements: False

to

::

    cli_testing:
        # Activates the generation of complements.
        complements: True

into your personal :code:`.PyFunceble.yaml` or use the :code:`--complements`
argument from the CLI to activate it.