Autoconfiguration
-----------------

Sometimes, you may find yourself in a position that you do not or you can’t
answer the question which asks you if you would like to merge an upstream
configuration file into your local one.

For that reason, if you can set the :code:`PYFUNCEBLE_AUTO_CONFIGURATION`
as an environment variable. Setting that environment variable will make
PyFunceble merge the upstream configuration when a new key is available but
not found into your configuration file.

.. warning::
    As of :code:`4.0.0` the configuration file is automatically copied into
    your configuration directory - if it is not found.
