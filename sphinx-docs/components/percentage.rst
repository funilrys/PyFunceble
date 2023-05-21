Percentage
----------

.. warning::
    This component is activated by default while testing files.

.. note::
    The percentage doesn't show up - by design - while testing for single
    subjects.


Why do we need it?
^^^^^^^^^^^^^^^^^^

We need it in order to get information about the amount of data we just tested.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here
    :class:`~PyFunceble.cli.filesystem.counter.FilesystemCounter`!

Regularly or at the very end of a test we get the number of subjects for
each status along with the number of tested subjects.
We then generate and print the percentage calculation on the screen
(:code:`stdout`) and into
:code:`output/${input_file_name}/logs/percentage/percentage.txt`

How to use it?
^^^^^^^^^^^^^^

It is activated by default, but if not please update

::

    cli_testing:
        display_mode:
            # Activates the output of the percentage information.
            percentage: False

to

::

    cli_testing:
        display_mode:
            # Activates the output of the percentage information.
            percentage: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--percentage`
argument from the CLI to reactivate it.
