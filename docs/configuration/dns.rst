:code:`dns`
^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the DNS lookup.

:code:`dns[server]`
"""""""""""""""""""

    **Type:** :code:`list`

    **Default value:** :code:`null`

    **Description:** Sets the DNS server(s) to work with.

.. note::
    When a list is given the following format is expected.

    .. code-block:: yaml

        dns_server:
          - dns1.example.org
          - dns2.example.org

.. note::
    You can specify a port number to use to the DNS server if needed.

    As example:

    .. code-block:: yaml

        - 127.0.1.53:5353

.. warning::
    Please be careful when you overwrite this option. If one is not correct,
    you can almost sure that all results are going to be flagged as
    :code:`INACTIVE`.

:code:`dns[protocol]`
"""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`UDP`

    **Available values:** :code:`UDP`, :code:`TCP`, :code:`HTTPS`, :code:`TLS`.

    **Description:** Sets the protocol to use for all DNS queries.

:code:`dns[follow_server_order]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the follow-up of the given order.

:code:`dns[trust_server]`
"""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the trust mode. When the trust mode
    is active and the first read DNS server gives us a negative response
    (without any error), we take it as it is.

    Otherwise, when the trust mode is disabled, when the first read DNS server
    gives us a negative response (without any error), we still ask all other
    DNS servers that were given or found.

:code:`dns[delay]`
""""""""""""""""""

    **Type:** :code:`float`

    **Default value:** :code:`0.0`

    **Description:** Sets the delay to apply between each DNS query.
