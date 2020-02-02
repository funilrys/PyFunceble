DNS Lookup
==========

Why do we need it?
------------------

As our main purpose is to check the availability of the given subjects, we make a DNS lookup
to determine it.

How does it work?
-----------------

.. note::
    Want to read the code ? It's here :func:`~PyFunceble.lookup.dns.DNSLookup`!

For domains
^^^^^^^^^^^

We request the :code:`NS` record for domains.

.. warning::
    If none is found, we call the UNIX/C equivalent of :code:`getaddrinfo()`.

For IP
^^^^^^

We request the :code:`PTR` record for the IP.

.. warning::
    If none is found, we call the UNIX/C equivalent of :code:`gethostbyaddr()`.
