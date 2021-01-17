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

    ::

        dns_server:
          - dns1.example.org
          - dns2.example.org

.. note::
    You can specify a port number to use to the DNS server if needed.

    As example:

    ::

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