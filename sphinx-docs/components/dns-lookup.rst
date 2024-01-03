DNS Lookup
----------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As our main purpose is to check the availability of the given subjects, we make
a DNS lookup to determine it.

How does it work?
^^^^^^^^^^^^^^^^^

For domains
"""""""""""

In order:

1. Request the :code:`NS` record.
2. If not found, request the :code:`A` record.
3. If not found, request the :code:`AAAA` record.
4. If not found, request the :code:`CNAME` record.
5. If not found, request the :code:`DNAME` record.

.. warning::
    If none is found, we call the UNIX/C equivalent of :code:`getaddrinfo()`.

For IP
""""""

We request the :code:`PTR` record for the IP.

.. warning::
    If none is found, we call the UNIX/C equivalent of :code:`gethostbyaddr()`
    or :code:`getaddrinfo()`.

How to use it?
^^^^^^^^^^^^^^

It is activated by default but if not simply change

::

    lookup:
        # Activates the usage of the DNS lookup.
        dns: False

to

::

    lookup:
        # Activates the usage of the DNS lookup.
        dns: True

into your personal :code:`.PyFunceble.yaml` or use the :code:`--no-whois`
argument from the CLI to reactivate it.
