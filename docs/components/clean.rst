Cleaning
--------

Why do we need it?
^^^^^^^^^^^^^^^^^^

Because we constantly need to clean files which are not needed before starting
a new test, we embedded our cleaning logic.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here
    :class:`~PyFunceble.cli.filesystem.cleanup.FilesystemCleanup`!

It has an internal map of what has to be deleted and how.

How to clean?
^^^^^^^^^^^^^

For a simple clean, run PyFunceble with the :code:`clean-pyfunceble` CLI tool.

For a complete cleaning, run PyFunceble with the :code:`clean-pyfunceble` CLI
tool along with the :code:`--all` argument.
