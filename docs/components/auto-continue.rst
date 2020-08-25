Autocontinue
------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

The auto-continue logic was mainly created for one purpose: Testing long files inside Travis CI.
As Travis CI has a time limit of 45 minutes, it became vital for us to be able to stop and continue
the test from where we were under those 45 minutes. That's how it started.

Today, - and it might be controversial - it is used by most people who aren't under a Travis CI container
to continue when the machine or tool crashes.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here :func:`PyFunceble.engine.auto_continue.AutoContinue`!

We log every subject already tested previously and remove them when the same file path
is given again.

How to use it?
^^^^^^^^^^^^^^

It is activated by default but if not simply change

::

    auto_continue: False

to

::

    auto_continue: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--auto-continue` argument from the CLI to reactivate it.
