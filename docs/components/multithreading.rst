Multithreading
--------------


Why do we need it?
^^^^^^^^^^^^^^^^^^

Many people around the web who talked about PyFunceble were talking about
one thing: We take time to run.

In the past, we implemented what was then called the "multiprocessing" method.
As of :code:`4.0.0`, we went away from the multiprocessing logic we created.
The reason behind it was that the multiprocessing method we developed or
designed was becoming a nightmare to manage because we always had to take into
consideration that a process does not have access to the memory space of
the main process.

Therefore, we decided to switch to a more manageable and understandable
method by using multithreading. This will let us test (I/O bound tasks) and
create a data workflow which is easier to maintain and follow.



How does it work?
^^^^^^^^^^^^^^^^^

We read the given inputs, add them into some queues and generate some outputs
through other queues or threads.

Here is a short representation of the thread model behind the CLI testing:

.. image:: https://raw.githubusercontent.com/PyFunceble/draw.io/master/dist/Thread_Model_PyFunceble_CLI.png
    :alt: PyFunceble CLI Thread Model
    :target: https://raw.githubusercontent.com/PyFunceble/draw.io/master/dist/Thread_Model_PyFunceble_CLI.png


How to use it?
^^^^^^^^^^^^^^

As of :code:`4.0.0`, you don't have the choice. It is available and is
systematically used as soon as you use the `PyFunceble` CLI.