Status
======

There's 3 possible output for this column.

ACTIVE
------

This status is returned when **one of the following cases** is met:

- We can extract the expiration date from :func:`~PyFunceble.lookup.whois.WhoisLookup.request`.

   .. note::
      We don't check if the extracted date is in the past.


- :func:`~PyFunceble.lookup.dns.DNSLookup.request` don't return an error.

   - *Please note that we don't read the returned value.*

   .. note::
      We distribute but don't take the non-:code:`None` retuned value in consideration.

- :func:`~PyFunceble.lookup.http_code.HTTPCode.get` return one the following code :code:`[100, 101, 200, 201, 202, 203, 204, 205, 206]`.

INACTIVE
--------

This status is returned when **all the following cases** are met:

- We could not extract the expiration date from :func:`~PyFunceble.lookup.whois.Whois.request`.
- :func:`~PyFunceble.lookup.dns.DNSLookup.request` returns nothing.
- :func:`~PyFunceble.lookup.http_code.HTTPCode.get` is not in the list of :code:`ACTIVE` status codes.

INVALID
-------

This status is returned when **all the following cases** are met:

- Domain/IP does not match/pass our syntax checker.

- Domain extension is unregistered in the `IANA`_ Root Zone Database, our internal list nor in the `Public Suffix List`_.

   .. note::
      Understand by this that the extension is not present:

         - in the :code:`iana-domains-db.json` file
         - in the :code:`public-suffix.json` file
         - in the :py:attr:`PyFunceble.check.Check.SPECIAL_USE_DOMAIN_NAMES_EXTENSIONS` attribute.

.. _IANA: https://www.iana.org/domains/root/db
.. _Public Suffix List: https://publicsuffix.org/

VALID
-----

This status is returned when we are checking for syntax. It is the equivalent of :code:`ACTIVE` but for syntax checking.