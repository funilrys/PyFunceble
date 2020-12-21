Autoconfiguration
-----------------

As of :code:`4.0.0` PyFunceble won't ask you anything anymore.
You are the one in control of your configuration file.

Therefore, if you run PyFunceble in an automated way, you are recommended to
set the :code:`PYFUNCEBLE_AUTO_CONFIGURATION` as an environment variable.

.. warning::
    As of :code:`4.0.0` the configuration file is automatically copied into
    your configuration directory - if it is not found.
