Logs Sharing
------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

We chose to initiate the logs sharing as some actions can really be random when working with millions of domains.

The idea and purpose of this feature are **ONLY** to make PyFunceble a better tool.

What do we share/collect?
^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+
| **Event**                                       | **Shared**                                      | **URL**                                                 |
+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+
| No WHOIS server (referer) is found.             | - The extension of the currently tested domain. | :code:`https://pyfunceble.funilrys.com/api/no-referer`  |
+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+
| The expiration date is not correctly formatted. | - The extracted expiration date.                | :code:`https://pyfunceble.funilrys.com/api/date-format` |
|                                                 | - The currently tested domain.                  |                                                         |
|                                                 | - The currently used WHOIS server (DNS) name.   |                                                         |
+-------------------------------------------------+-------------------------------------------------+---------------------------------------------------------+

How to share logs?
^^^^^^^^^^^^^^^^^^

If you wish to share your logs simply change

::

   share_logs:                   False

to

::

   share_logs:                   True

into your personal :code:`.PyFunceble.yaml` or use the :code:`--share-logs` argument from the CLI to activate it.