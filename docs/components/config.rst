Configuration
-------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we wanted to be hybrid and allow different modes and options, we introduced the configuration logic.


How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the configuration loader code ? It's here :func:`PyFunceble.config.load.Load`!

We first look for the :code:`.PyFunceble.yaml`. If not found, we get/generate it.
Then we parse it to the system.

.. note::
    Because we also wanted to get rid of the configuration for an end-user point of view,
    almost all configuration indexed can be updated from the CLI.

    In that case, we update the configuration with the different argument you gives
    us before parsing it to the system.

.. note::
    If in the future a new configuration key is introduced, you will be asked to choose if you want to merge it into your :code:`.PyFunceble.yaml`.

    In that case, we get a copy of the new one and keep/set all previously set indexes. Which means that you don't have to care about reconfiguring previously
    set indexes.

How to configure?
^^^^^^^^^^^^^^^^^

Update the :code:`.PyFunceble.yaml` file or use the CLI.