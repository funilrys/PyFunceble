Autocontinue
------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

The auto-continue logic was originaly created for one purpose: Testing long
files inside Travis CI.
As Travis CI session has a time limit of 45 minutes, it became vital for us to
be able to stop and continue the test from where we were under those 45 minutes.
This is how it started.

Today, - and it might be controversial - it is used by most people who aren't
under a Travis CI container to continue when the machine or tool crashes.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here:
    :meth:`~PyFunceble.dataset.autocontinue.base.ContinueDatasetBase`!

We log every subject already tested previously and remove them completely
when we are done with the test of the given file.

How to use it?
^^^^^^^^^^^^^^

It is activated by default but you can simply change

::

    cli_testing:
        autocontinue: False

to

::

    cli_testing:
        autocontinue: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--continue`
argument from the CLI to reactivate it.
