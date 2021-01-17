Whois Lookup
------------

.. note::
    While testing using PyFunceble, subdomains, IPv4 and IPv6 are not used
    against our whois lookup logic.

Why do we need it?
^^^^^^^^^^^^^^^^^^

As our main purpose is to check the availability of the given subjects, we make
a WHOIS lookup (if authorized) to determine it.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here
    :class:`~PyFunceble.query.whois.query_tool.WhoisQueryTool`!

For us the only relevant part is the extraction of the expiration date.
Indeed, it's an indicator if a domains is still owned by someone, we use it
first to get the availability of domains.


How to use it?
^^^^^^^^^^^^^^

It is activated by default but if not simply change

::

    lookup:
        # Activates the usage of the WHOIS record.
        whois: False

to

::

    lookup:
        # Activates the usage of the WHOIS record.
        whois: True

into your personal :code:`.PyFunceble.yaml` or use the :code:`--no-whois`
argument from the CLI to reactivate it.
