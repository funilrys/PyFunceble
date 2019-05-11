Status
======

There's 3 possible output for this column.

ACTIVE
------

This status is returned when **one of the following cases** is met:

- We can extract the expiration date from :func:`PyFunceble.whois.Whois.request`.

  - *Please note that we don't check if the date is in the past.*

- :func:`PyFunceble.dns_lookup.DNSLookup.request` don't return an error.

  - *Please note that we don't read the returned value.*

- :func:`PyFunceble.http_code.HTTPCode.get` return one the following code :code:`[100, 101, 200, 201, 202, 203, 204, 205, 206]`.

INACTIVE
--------

This status is returned when **all the following cases** are met:

- We could not extract the expiration date from :func:`PyFunceble.whois.Whois.request`.
- :func:`PyFunceble.dns_lookup.DNSLookup.request` returns nothing.

INVALID
-------

This status is returned when **all the following cases** are met:

- Domain/IP does not match pass our syntax checker.

- Domain extension is unregistered in `IANA`_ Root Zone Database.

   .. note::
      Understand by this that the extension is not present in the :code:`iana-domains-db.json` file.

.. _IANA: https://www.iana.org/domains/root/db

VALID
-----

This status is returned when we are checking for syntax. It is the equivalent of :code:`ACTIVE` but for syntax checking.