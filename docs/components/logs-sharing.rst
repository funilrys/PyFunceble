Logs Sharing
------------

.. note::
    This component is not activated by default.


Why do we need it?
^^^^^^^^^^^^^^^^^^

We chose to initiate the logs sharing as some actions can really be random when
working with millions of domains.

The idea and purpose of this feature are **ONLY** to make PyFunceble a better
tool.


What is collected
^^^^^^^^^^^^^^^^^

.. versionchanged:: 4.0.0

As of :code:`4.0.0`, we temporarly disabled and removed all data collection.

Indeed, I need to rewrite the infrastructure behind it. Therefore, I refused
to implement any of the data collection source code until the infrastructure
behind it is ready.


.. warning::
   The following table only represent the option as available in the :code:`3.x`
   version of PyFunceble.

+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+
| **Event**                                       | **Shared**                                      | **URL**                                                 |
+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+
| No WHOIS server (referrer) is found.            | - The extension of the currently tested domain. | :code:`https://pyfunceble.funilrys.com/api/no-referrer` |
+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+
| The expiration date is not correctly formatted. | - The extracted expiration date.                | :code:`https://pyfunceble.funilrys.com/api/date-format` |
|                                                 | - The currently tested domain.                  |                                                         |
|                                                 | - The currently used WHOIS server (DNS) name.   |                                                         |
+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+


How to share logs?
^^^^^^^^^^^^^^^^^^

If you wish to share your logs simply change

.. code-block:: yaml

   share_logs:                   False

to

.. code-block:: yaml

   share_logs:                   True

into your personal :code:`.PyFunceble.yaml` or use the :code:`--share-logs`
argument from the CLI to activate it.
