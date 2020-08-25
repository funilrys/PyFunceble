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
    Want to read the code ? It's here :func:`PyFunceble.cli.execution_time.ExecutionTime`!

It shows the exection time on screen (:code:`stdout`) and at the end of the :code:`output/logs/percentage/percentage.txt` file if :code:`show_percentage` is activated.

How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    show_execution_time: False

to

::

    show_execution_time: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--execution` argument from the CLI to activate it.
