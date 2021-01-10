Source
------

Give us the source of the status.

.. note::
    The API equivalent is :code:`status_source`.


HTTP Code
^^^^^^^^^

This source is returned when **all the following cases** are met:

- We can't extract the expiration date from
  :func:`PyFunceble.lookup.whois.WhoisLookup.request`.
- The :code:`INACTIVE` status is the one returned by other methods.
- :func:`PyFunceble.lookup.http_code.HTTPCode.get` outputs is different from
  the default one (:code:`99999999`) and the other methods gives the
  :code:`INACTIVE` status.


SYNTAX
^^^^^^

This source is always returned when the domain has the status :code:`INVALID`
or in the case that we are only checking for syntax instead of availability.
The usage of this source comes from the comparison of the element against our
domain, IP or URL syntax validation system.


DNSLOOKUP
^^^^^^^^^

This source is always returned when the taken decision of the status of the
domain/IP comes from :func:`PyFunceble.lookup.dns.DNSLookup.request` outputs.


.. include:: special_rules.rst


IP with range
"""""""""""""

- All IPv4 with a range (for example :code:`0.0.0.0/24`) are returned as
  :code:`ACTIVE`
- All IPv6 with a range (for example :code:`2001:db8::/43`) are returned as
  :code:`ACTIVE`


Reputation
""""""""""

.. note::
  If the :code:`--use-reputation-data` argument is activated
  or the :code:`use_reputation_data` index of your
  configuration file is active, the following apply.

- All IPv4 and IPv6 which are present into the AlienVault public
  reputation data are returned as :code:`ACTIVE`



.. _issue: https://github.com/funilrys/PyFunceble/issues
