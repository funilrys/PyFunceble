Status
------

There's 3 possible output for this column.

ACTIVE
^^^^^^

This status is returned when **one of the following cases** is met:

- We can extract the expiration date from :code:`Lookup().whois()`.

  - *Please note that we don't check if the date is in the past.*

- :code:`Lookup().nslookup()` don't return an error.

  - *Please note that we don't read the returned value.*

- :code:`HTTPCode().get()` return one the following code :code:`[100, 101, 200, 201, 202, 203, 204, 205, 206]`.

INACTIVE
^^^^^^^^

This status is returned when **all the following cases** are met:

- We can't extract the expiration date from :code:`Lookup().whois()`.
- :code:`Lookup().nslookup()` don't return an error.

INVALID
^^^^^^^

This status is returned when **all the following cases** are met:

- Domain/IP does not match pass our syntax checker.

- Domain extension is unregistered in `IANA`_ Root Zone Database.

   .. note::
      Understand by this that the extension is not present in the :code:`iana-domains-db.json` file.

.. _IANA: https://www.iana.org/domains/root/db

VALID
^^^^^

This status is returned when we are checking for syntax. It is the equivalent of :code:`ACTIVE` but for syntax checking.