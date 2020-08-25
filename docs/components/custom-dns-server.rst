Custom DNS Server
-----------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

Some times the testing environment is setup to use DNS-server which isn't
suited for running a PyFunceble test of actually expired or active domains or
urls. This could by example be your own DNS-Firewall.

To avoid these situations, the program allows you to setup test DNS-Server.

How does it work?
^^^^^^^^^^^^^^^^^

Thanks to :code:`python-dns` we can parse the given DNS server.

How to use it?
^^^^^^^^^^^^^^

By default, PyFunceble will use the system-wide DNS settings. This can be
changed with the ability to configure which DNS-Servers you like PyFunceble to
use doing the test.

You set this up with the CLI command :code:`--dns` **or** insert it into your
personal :code:`.PyFunceble.yaml`

::

    dns_server: null

to

::

    dns_server:
        - "8.8.8.8"
        - "8.8.8.8"


Since :code:`v3.0.0` it is possible to assign a specific port to use with the
DNS-Server.

.. hint::

    --dns 95.216.209.53:53 116.203.32.67:53 9.9.9.9:853

.. warning::
    If you don't append a port number, the default DNS port (53) will be used.
