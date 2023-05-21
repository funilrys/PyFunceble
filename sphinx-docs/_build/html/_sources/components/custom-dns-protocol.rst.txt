Custom DNS Protocol
-------------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

Sometimes, your firewall may block the UDP protocol over port 53 or you simply
want to use DNS-Over-TLS or why not DNS-Over-HTTPS and why not DNS-Over-TCP.

Since PyFunceble 4.0.0, to simplify such situations, it is possible to define
the protocol to use for the DNS queries.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the DNS query tool source code ?
    It's here :class:`~PyFunceble.query.dns.query_tool.DNSQueryTool`!

We read your preferred protocol and use it.

How to use it?
^^^^^^^^^^^^^^

By default, PyFunceble will use the UDP protocol. This can be
changed with the ability to configure which DNS-Servers you like PyFunceble to
use during the test.

You set this up with the CLI command :code:`--dns-protocol` **or** insert it
into your personal :code:`.PyFunceble.yaml`.

.. note::
    As of today, here is the list of supported protocols.

    - :code:`UDP` (default)
    - :code:`TCP`
    - :code:`HTTPS`
    - :code:`TLS`

::

    dns:
        # Sets the protocol to use.
        # Available: UDP | TCP | HTTPS | TLS
        protocol: UDP

to

::

    dns:
        # Sets the protocol to use.
        # Available: UDP | TCP | HTTPS | TLS
        protocol: TCP

