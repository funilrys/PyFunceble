Steps before commit
===================

.. note::

    The following do not apply if you do not touch the :code:`PyFunceble` nor the :code:`tests` directory.

::

    $ # We format our code.
    $ black PyFunceble && black tests/*.py
    $ # We lint our code. Please make sure to fix all reported issues.
    $ pylint PyFunceble && pylint tests/*.py
    $ # We check the tests coverage. Please ensure that at lease 95% of the code is covered.
    $ coverage run setup.py test && coverage report -m
    $ # Prepare our files, :code:`version.yaml` and code for pushing.
    $ PyFunceble --production