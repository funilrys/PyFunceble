Multiprocessing
---------------


Why do we need it?
^^^^^^^^^^^^^^^^^^

Many people around the web who talked about PyFunceble were talking about
one thing: We take time to run.

In the past, we implemented what was then called the "multiprocessing" method.
As of :code:`4.0.0`, we went away from the original multiprocessing logic.
The reason behind it was that the multiprocessing method we developed at the
time was becoming a nightmare to manage because we always had to take into
consideration that a process does not have access to the memory space of
the main process.


Therefore, we decided to rewrite it to be a bit more efficient.
In the new layout, we work with queues to split the testing work
through multiple test workers. That simplifies our data workflow and
maintainability.


How does it work?
^^^^^^^^^^^^^^^^^

We read the given inputs, add them into some queues and generate some outputs
through other queues or processes.

Here is a short representation of the process model behind the CLI testing:

.. image:: https://raw.githubusercontent.com/PyFunceble/draw.io/master/dist/Process_Model_PyFunceble_CLI.png
    :alt: PyFunceble CLI Thread Model
    :target: https://raw.githubusercontent.com/PyFunceble/draw.io/master/dist/Process_Model_PyFunceble_CLI.png


How to use it?
^^^^^^^^^^^^^^

As of :code:`4.0.0`, you don't have the choice. It is available and is
systematically used as soon as you use the `PyFunceble` CLI.

But, you can control the maximum about of test worker through the
:code:`--max-workers` argument or its configuration counterpart:

.. code-block:: yaml

    cli_testing:
        # Sets the number of maximal workers to use.
        # If set to null, the system use: CPU * Cores - 2
        max_workers: null
