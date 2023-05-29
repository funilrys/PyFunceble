API Responses (explained)
-------------------------

In this page, we intend to explain the most useful parts of the API responses.

:code:`checker_type`
^^^^^^^^^^^^^^^^^^^^

The checker type. It describes the checker which was used to provide
the given response.

It should be one of the following:

- :code:`SYNTAX`
- :code:`AVAILABILITY`
- :code:`REPUTATION`

:code:`idna_subject`
^^^^^^^^^^^^^^^^^^^^

The IDNA formatted subject. It is the subject that is internally exposed the all
supported testing methods.

You should consider this as the subject and consider the :code:`subject` key as
a placeholder of what was given by you.

:code:`params`
^^^^^^^^^^^^^^

The parameters. It describes the parameter applied to the checker. In most case,
if you are using the Python API, you should be able to control most of them
through the **class constructor** or their **property setters** with the same
name.

Syntax Checker
""""""""""""""

As of now, there is no known parameters.

Availability Checker
""""""""""""""""""""

With the availability checker, the following is provided.

.. code-block:: json

    {
        "do_syntax_check_first": false,
        "use_dns_lookup": true,
        "use_extra_rules": true,
        "use_http_code_lookup": true,
        "use_netinfo_lookup": true,
        "use_reputation_lookup": false,
        "use_whois_db": true,
        "use_whois_lookup": false,
        "use_collection": false
    }

:code:`do_syntax_check_first`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it has to do a syntax check before
starting an extensive test. Meaning that the status strongly depends on the
caught syntax.

:code:`use_dns_lookup`
~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to perform some DNS
lookup to determine the status of the given subject.

:code:`use_extra_rules`
~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to check against our own
sets of SPECIAL rules in order to escalate or deescalate the status of the given
subject.

:code:`use_http_code_lookup`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to gather and use the
HTTP status code of the given subject to determine its status.

:code:`use_netinfo_lookup`
~~~~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to perform a network
information lookup to determine the status of the given subject.

:code:`use_reputation_lookup`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that is allowed to perform a reputation
lookup to determine the status of the given subject.

:code:`use_whois_db`
~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to look at the WHOIS
local WHOIS database before even trying to perform a WHOIS lookup to determine
the status of the given subject.

.. warning::
    If the :code:`use_whois_lookup` parameter is deactivated, this parameter is
    ignored.

:code:`use_whois_lookup`
~~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that is it allowed to perform a WHOIS
lookup to determine the status of the given subject.

:code:`use_collection`
~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to perform a lookup into
the collection API before starting an extensive local test.

Reputation Checker
""""""""""""""""""

With the availability checker, the following is provided.

.. code-block:: json

    {
        "do_syntax_check_first": false,
        "use_collection": false
    }

:code:`do_syntax_check_first`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it has to do a syntax check before
starting an extensive test. Meaning that the status strongly depends on the
caught syntax.

:code:`use_collection`
~~~~~~~~~~~~~~~~~~~~~~

This parameter lets the checker know that it is allowed to perform a lookup into
the collection API before starting an extensive local test.

:code:`status`
^^^^^^^^^^^^^^

The status. It describes the final status gathered by the checker.

Syntax Checker
""""""""""""""

With the syntax checker, it may be one of the following:

- :code:`VALID`
- :code:`INVALID`

Availability Checker
""""""""""""""""""""

With the availability checker, it may be one of the following:

- :code:`ACTIVE`
- :code:`INACTIVE`
- :code:`INVALID`

Reputation Checker
""""""""""""""""""

With the reputation checker, it may be one of the following:

- :code:`SANE`
- :code:`MALICIOUS`

:code:`registrar`
^^^^^^^^^^^^^^^^^

The registrar. It describes the registrar of the given subject as described in
its WHOIS record.

Syntax Checker
""""""""""""""

Non-existent.

Availability Checker
""""""""""""""""""""

Provides the - found - registrar. Otherwise, :code:`null` is provided.

Reputation Checker
""""""""""""""""""

Non-existent.

:code:`status_after_extra_rules`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The status after our extra rules lookup. It describes the status after the
lookup against our own sets of rules.

If no rules were matched, :code:`null` is provided.

.. warning::
    Beware, this is only provided by the **availability** checker.

:code:`status_before_extra_rules`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The status before our extra rules lookup. It describes the status before the
lookup against our own sets of rules. In other words, it is the status provided
by our standard status lookup strategy.

If no rules were matched, :code:`null` is provided.

.. warning::
    Beware, this is only provided by the **availability** checker.

:code:`status_source`
^^^^^^^^^^^^^^^^^^^^^

The status source. It describes the test method that led to the given status.

It should be one of the following:

- :code:`SYNTAX`
- :code:`WHOIS`
- :code:`DNSLOOKUP`
- :code:`NETINFO`
- :code:`HTTP CODE`
- :code:`SPECIAL` (extra rules)
- :code:`COLLECTION`

:code:`status_source_after_extra_rules`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The status source after our extra rules lookup. It describes the status source
after the lookup against our own sets of rules.

It should be :code:`SPECIAL`.

If no rules were matched, :code:`null` is provided.

.. warning::
    Beware, this is only provided by the **availability** checker.

:code:`status_source_before_extra_rules`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The status source before our extra rules lookup. It describes the status source
before the lookup against our own sets of rules.

In other words, it is the status source provided by our standard status
lookup strategy.

It should be one of the following:

- :code:`SYNTAX`
- :code:`WHOIS`
- :code:`DNSLOOKUP`
- :code:`NETINFO`
- :code:`HTTP CODE`
- :code:`COLLECTION`

If no rules were matched, :code:`null` is provided.

.. warning::
    Beware, this is only provided by the **availability** checker.


:code:`subject`
^^^^^^^^^^^^^^^

The subject. It describes the subject that was given by you.

:code:`tested_at`
^^^^^^^^^^^^^^^^^

The test date. It may not be useful to everyone, but it describes the date and
time of the generation of the given output.

:code:`dns_lookup`
^^^^^^^^^^^^^^^^^^

The DNS lookup summary. It describes the summary of the DNS Lookup that was
performed.

Syntax Checker
""""""""""""""

Non-existent.

Availability Checker
""""""""""""""""""""

With the availability checker, the following format (or :code:`null`) is provided:

.. code-block:: json

    {
        "QUERY TYPE": [
            "string",
            "string"
        ]
    }

Where :code:`QUERY TYPE` is one of the following:

- :code:`NS`
- :code:`A`
- :code:`AAAA`
- :code:`CNAME`
- :code:`DNAME`

Reputation Checker
""""""""""""""""""

With the reputation checker, the following format (or :code:`null`) is provided:

.. code-block:: json

    [
        "string",
        "string"
    ]

It is just a simple list of IPs that we check against. When the given
subject is an IPv4, :code:`null` is provided.

:code:`dns_lookup_record`
^^^^^^^^^^^^^^^^^^^^^^^^^

The DNS lookup record. It describes the latest performed DNS lookup record.

Syntax Checker
""""""""""""""

Non-existent.

Availability and Reputation Checker
"""""""""""""""""""""""""""""""""""

With the availability or reputation checker, the following is provided.

.. code-block:: json

    {
        "dns_name": "example.com.",
        "follow_nameserver_order": true,
        "nameserver": "9.9.9.9",
        "port": 53,
        "preferred_protocol": "UDP",
        "query_record_type": "NS",
        "query_timeout": 5.0,
        "response": [
            "a.iana-servers.net.",
            "b.iana-servers.net."
        ],
        "subject": "example.com",
        "used_protocol": "UDP"
    }

:code:`dns_name`
~~~~~~~~~~~~~~~~

The DNS name. It describes the DNS name that was queried.

:code:`follow_nameserver_order`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It describes if we followed the nameserver order.

:code:`nameserver`
~~~~~~~~~~~~~~~~~~

The nameserver. It describes the nameserver that was queried last.

:code:`port`
~~~~~~~~~~~~

The port. It describes the port that was used to communicate with the
nameserver.

:code:`query_record_type`
~~~~~~~~~~~~~~~~~~~~~~~~~

The query record type. It describes the record type that was queried last.

:code:`query_timeout`
~~~~~~~~~~~~~~~~~~~~~

The query timeout. It describes the query timeout that was used to perform the
query.

:code:`response`
~~~~~~~~~~~~~~~~

The response. It describes a list of domains or IPs given by the nameserver as
response.

:code:`subject`
~~~~~~~~~~~~~~~

The subject. It describes the subject that was given to the query tool.

:code:`used_protocol`
~~~~~~~~~~~~~~~~~~~~~

The used protocol. It describes the used protocol.

It should be one of the following:

- :code:`UDP` (default)
- :code:`TCP`
- :code:`HTTPS`
- :code:`TLS`

:code:`domain_syntax`
^^^^^^^^^^^^^^^^^^^^^

The domain syntax. It describes through a boolean the state of the given
subject.

In other words: :code:`true` is provided when the given subject is a 2nd level
domain or a subdomain.

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`expiration_date`
^^^^^^^^^^^^^^^^^^^^^^^

The expiration date. It describes the expiration date of the given subject as
extracted from the WHOIS record.

If none is found, :code:`null` will be provided.

.. warning::
    Beware, this is only provided by the **availability** checker.

:code:`http_status_code`
^^^^^^^^^^^^^^^^^^^^^^^^

The HTTP status code. It describes the HTTP status code which was discovered.

If none is found, :code:`null` or :code:`0` will be provided.

.. warning::
    Beware, this is only provided by the **availability** checker.

:code:`ip_syntax`
^^^^^^^^^^^^^^^^^

The IP syntax. It describes through a boolean the state of the given
subject.

In other words: :code:`true` is provided when the given subject is an IPv4 or
an IPv6 (range excluded).

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`ipv4_range_syntax`
^^^^^^^^^^^^^^^^^^^^^^^^^

The IPv4 range syntax. It describes through a boolean the state of the given
subject.

In other words: :code:`true` is provided when the given subject is an IPv4
range.

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`ipv4_syntax`
^^^^^^^^^^^^^^^^^^^

The IPv4 syntax. It describes through a boolean the state of the given
subject.

In other words: :code:`true` is provided when the given subject is an IPv4
(range excluded).

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`ipv6_range_syntax`
^^^^^^^^^^^^^^^^^^^^^^^^^

The IPv6 range syntax. It describes through a boolean the state of the given
subject.

In other words: :code:`true` is provided when the given subject is an IPv6
range.

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`ipv6_syntax`
^^^^^^^^^^^^^^^^^^^

The IPv6 syntax. It describes through a boolean the state of the given
subject.

In other words: :code:`true` is provided when the given subject is an IPv6
(range excluded).

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`second_level_domain_syntax`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The 2nd level domain syntax. It describes through a boolean the state of the
given subject.

In other words: :code:`true` is provided when the given subject is a 2nd level
domain.

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`subdomain_syntax`
^^^^^^^^^^^^^^^^^^^^^^^^

The subdomain syntax. It describes through a boolean the state of the
given subject.

In other words: :code:`true` is provided when the given subject is a subdomain.

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`url_syntax`
^^^^^^^^^^^^^^^^^^

The subdomain syntax. It describes through a boolean the state of the
given subject.

In other words: :code:`true` is provided when the given subject is a URL.

.. warning::
    This key may give you a :code:`null` if nothing was performed (yet).

.. warning::
    Beware, this is only provided by the **availability** and **reputation**
    checkers.

:code:`netinfo`
^^^^^^^^^^^^^^^

The network information summary. It describes the summary of the network
information lookup.

Syntax Checker
""""""""""""""

Non-existent.

Availability Checker
""""""""""""""""""""


With the availability checker, the following format (or :code:`null`) is
provided:

.. code-block:: json

    [
        "string",
        "string"
    ]

It is just a simple list of IPs or domains that were found. Otherwise,
:code:`null` will be supplied.

Reputation Checker
""""""""""""""""""

Non-existent.

:code:`netloc`
^^^^^^^^^^^^^^

The network location. It describe the network location of the tested subject.
This can be useful when working with URLs. When working with URLs the value of
:code:`netloc` will be in the :code:`domain:port` formet if the port is
explicitly given and :code:`domain` otherwise.

:code:`whois_lookup_record`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The WHOIS lookup record. It describes the latest performed WHOIS lookup record.

Syntax Checker
""""""""""""""

Non-existent.

Availability Checker
""""""""""""""""""""

With the availability checker, the following is provided.

.. code-block:: json

    {
        "expiration_date": null,
        "port": 43,
        "query_timeout": 5.0,
        "record": null,
        "server": null,
        "subject": "example.com"
    }

:code:`expiration_date`
~~~~~~~~~~~~~~~~~~~~~~~

The expiration date. It describes the extracted expiration date.

It should be a string if the format `09-oct-1970` or :code:`null` otherwise.

:code:`port`
~~~~~~~~~~~~

The port. It describes the port used to communicate with the WHOIS server.

:code:`query_timeout`
~~~~~~~~~~~~~~~~~~~~~

The query timeout. It describes the query timeout that was applied during the
query.

:code:`record`
~~~~~~~~~~~~~~

The WHOIS record. It describes the record or response of the WHOIS server.

:code:`subject`
~~~~~~~~~~~~~~~

The subject. It describes the subject which was queried.

Reputation Checker
""""""""""""""""""

Non-existent.


:code:`whois_lookup`
^^^^^^^^^^^^^^^^^^^^

The WHOIS record. It describes the WHOIS record as given by the (root) WHOIS
server.

.. warning::
    Beware, this is only provided by the **availability** checker.