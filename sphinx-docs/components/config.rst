Configuration
-------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we wanted to be able to manage the options without having to always update
the CLI call, we introduced the configuration logic and file.


How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the configuration loader code ?
    It's here :class:`~PyFunceble.config.loader.ConfigLoader`!

When you are using an argument from the CLI, what we actually do is parse them
into our configuration logic.

In the other side, if we first look for the :code:`.PyFunceble.yaml` file.
If not found, we get/generate it and then parse it to our system.

.. note::
    We also wanted to get rid of the configuration for an end-user
    point of view, therefore almost all configuration indexed can be updated
    from the CLI.

    In that case, we update the configuration with the different argument you gives
    us before parsing it to the system.

How to configure?
^^^^^^^^^^^^^^^^^

Update the :code:`.PyFunceble.yaml` file or use the CLI.