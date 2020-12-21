Custom DNS Server
-----------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

Our testing tool may sometime use a DNS-server which isn't
suited for PyFunceble. This could by example be your own DNS-Firewall.

To avoid these situations, the program allows you to setup the DNS-Server that
we need to use.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the DNS query tool source code ?
    It's here :class:`~PyFunceble.query.dns.query_tool.DNSQueryTool`!

What we do is that we parse and use your given server.

How to use it?
^^^^^^^^^^^^^^

By default, PyFunceble will use the system-wide DNS settings. This can be
changed with the ability to configure which DNS-Servers you like PyFunceble to
use during the test.

You set this up with the CLI command :code:`--dns` **or** insert it into your
personal :code:`.PyFunceble.yaml`

::

    dns;
        server: null

to

::

    dns:
        server:
            - 95.216.209.53
            - 116.203.32.67
            - 116.203.32.67


Since :code:`v3.0.0` it is possible to assign a specific port to use with the
DNS-Server.

.. hint::

    :code:`--dns 95.216.209.53:53 116.203.32.67:53 116.203.32.67:853`

.. warning::
    If you don't append a port number, the default DNS port (53) will be used.
