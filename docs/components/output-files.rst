Outputed Files
--------------

.. note::
    This section does not cover the logs files.

Why do we need it?
^^^^^^^^^^^^^^^^^^

We need a way to deliver our results.

How does it work?
^^^^^^^^^^^^^^^^^

After testing a given subject, we generate its output file based on what's needed.

Host format
"""""""""""

This is the default output file.

A line is formatted like :code:`0.0.0.0 example.org`.

.. note::
    A custom IP can be set with the help of the :code:`custom_ip` index or the :code:`-ip` argument from the CLI.

Don't need it? Simply change

::

    generate_hosts: True

to

::

    generate_hosts: False


into your personal :code:`.PyFunceble.yaml` or use the :code:`--hosts` argument from the CLI to deactivate it.


Plain format
""""""""""""

A line is formatted like :code:`example.org`.
.
Need it? Simply change

::

    plain_list_domain: False

to

::

    plain_list_domain: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--plain` argument from the CLI to activate it.

JSON format
"""""""""""

Need it? Simply change

::

    generate_json: False

to

::

    generate_json: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--json` argument from the CLI to activate it.
