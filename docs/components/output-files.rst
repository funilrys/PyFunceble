Outputted Files
---------------

.. note::
    This section does not cover the log files.

Why do we need it?
^^^^^^^^^^^^^^^^^^

We need a way to deliver our results.

How does it work?
^^^^^^^^^^^^^^^^^

After testing a given subject, we generate its output file based on what's
needed.

Host format
"""""""""""

This is the default output file.

A line is formatted like :code:`0.0.0.0 example.org`.

.. note::
    A custom IP can be set with the help of the :code:`custom_ip` index or the
    :code:`--hosts-ip` argument from the CLI.

Don't need it? Simply change

::

    cli_testing:
        file_generation:
            # Activates the generation of the hosts file(s).
            hosts: False

to

::

    cli_testing:
        file_generation:
            # Activates the generation of the hosts file(s).
            hosts: False


into your personal :code:`.PyFunceble.yaml` or use the :code:`--hosts` argument
from the CLI to deactivate it.


Plain format
""""""""""""

A line is formatted like :code:`example.org`.

Need it? Simply change

::

    cli_testing:
        file_generation:
            # Activates the generation of the plain (or raw) file(s).
            plain: False

to

::

   cli_testing:
        file_generation:
            # Activates the generation of the plain (or raw) file(s).
            plain: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--plain` argument
from the CLI to activate it.
