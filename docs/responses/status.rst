Status
------

Give us the test result/status of the tested element.

.. note::
    The API equivalent is :code:`status`.

ACTIVE
^^^^^^

This status is returned when **one of the following cases** is met:

- We can extract the expiration date from :func:`PyFunceble.lookup.whois.WhoisLookup.request`.

   .. note::
      We don't check if the extracted date is in the past.
      Indeed, if we start to do the registry work, it becomes a never
      ending work for us.


- :func:`PyFunceble.lookup.dns.DNSLookup.request` does not return :code:`{}`.

   .. note::
      We don't read nor interpret the returned data.

      As the request :func:`PyFunceble.lookup.dns.DNSLookup.request` method
      already handle everything, we don't need to read the given data.

      We just check that it is not an empty dictionary.

- :func:`PyFunceble.lookup.dns.DNSLookup.request` returns :code:`{}`,
  :func:`PyFunceble.lookup.whois.WhoisLookup.request` provides nothing exploitable,
  but :func:`PyFunceble.lookup.http_code.HTTPCode.get` returned something which is not the default value (:code:`XXX`).

INACTIVE
^^^^^^^^

This status is returned when **all the following cases** are met:

- We could not extract the expiration date from :func:`PyFunceble.lookup.whois.WhoisLookup.request`.
- :func:`PyFunceble.lookup.dns.DNSLookup.request` returns nothing.
- :func:`PyFunceble.lookup.http_code.HTTPCode.get` is not in the list of :code:`ACTIVE` status codes.

INVALID
^^^^^^^

This status is returned when **all the following cases** are met:

- The Domain/IP does not match/pass our syntax checker.

- The domain extension is unregistered in the `IANA`_ Root Zone Database, our internal list nor in the `Public Suffix List`_.

   .. note::
      Understand by this that the extension is not present:

         - in the :code:`iana-domains-db.json` file
         - in the :code:`public-suffix.json` file
         - in the :py:attr:`PyFunceble.check.Check.SPECIAL_USE_DOMAIN_NAMES_EXTENSIONS` attribute.

.. _IANA: https://www.iana.org/domains/root/db
.. _Public Suffix List: https://publicsuffix.org/

VALID
^^^^^

This status is returned when we are checking for syntax. It is the equivalent of :code:`ACTIVE` but for syntax checking.

MALICIOUS
^^^^^^^^^

This status is returned when we are checking for the reputation.

SANE
^^^^

This status is returned when we are checking for the reputation.