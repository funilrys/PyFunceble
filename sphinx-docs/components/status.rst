Status
------

Why do we need it?
^^^^^^^^^^^^^^^^^^

We use it to provide a representation of the availability, syntax, or reputation
of a given subject.

How does it work?
^^^^^^^^^^^^^^^^^

Multiple statuses are available to each checker. Each has its meaning and
root.

INVALID
"""""""

This the status that is supplied by the **availability**, **syntax**, or
**reputation** checkers when the given subject is INVALID.

It is provided the subject does not pass our internal syntax checker.

The internal syntax checker analyzes the following against the given subject:

- If you are testing for a domain, is the extension registered in the IANA
  Root Zone Database?

- If you are testing for an IP, is it a valid IP (v4 or v6)?

- If you are testing for a URL, is it a valid one?

.. warning::
    While using the CLI against a local network, this is ignored.

ACTIVE
""""""

This is the status that is supplied by the **availability** checker.

It is provided when one of the following is effective:

- We could query the WHOIS record and extract the expiration date out of it.

- We could query any of the :code:`NS`, :code:`A`, :code:`AAAA`, :code:`CNAME`
  or :code:`DNAME` of the given subject.

- We could query the network information of the given subject.

- We could query the HTTP status code of the given subject.


VALID
"""""

This is the status that is supplied by the **syntax** checker.

It is provided when the syntax check of the given subject was successful.

Consider it as the equivalent of :code:`ACTIVE` but for syntax checking.


MALICIOUS
"""""""""

This is the status that is supplied by the **reputation** checker.

It is provided when the following is effective:

- If you are testing for a domain, is its IPv4 known to be malicious?

- If you are testing for an IP, is its IPv4 known to be malicious?

- If you are testing for a URL, is the IPv4 of the hostname known to be
  malicious?

SANE
""""

This is the status that is supplied by the **reputation** checker when the
:code:`MALICIOUS` status is not effective.
