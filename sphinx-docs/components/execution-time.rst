Execution time
--------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

As it is always nice to see how long we worked, we added this logic!

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here
    :class:`PyFunceble.cli.execution_time.ExecutionTime`!

It shows the execution time on screen (:code:`stdout`).

How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    display_mode:
        # Activates the printing of the execution time.
        execution_time: False

to

::

    display_mode:
        # Activates the printing of the execution time.
        execution_time: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--execution`
argument from the CLI to activate it.
