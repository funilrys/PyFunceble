Custom DNS Server
=================

Why do we need it?
------------------

As some time we can't trust the default DNS server into a container/machine, we allow you to communicate us a list
of DNS server to ask for the records.

How does it work?
-----------------

Thanks to :code:`python-dns` we can parse the given DNS server.

How to use it?
--------------

Simply give us a list of DNS server like follow from

::

    dns_server: null

to

::

    dns_server:
        - "1.1.1.1"
        - "1.0.0.1"


into your personal :code:`.PyFunceble.yaml` or use the :code:`--DNS` argument from the CLI.
