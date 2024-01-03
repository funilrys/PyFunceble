Status Source
-------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

We use it to provide a representation of the testing method that led to the
status.

How does it work?
^^^^^^^^^^^^^^^^^

Multiple status sources are available. Each has its meaning and root.

SYNTAX
""""""

This is the status source that is supplied when the syntax is the reason behind
the status. It is exclusively followed by the :code:`INVALID` status.

You may find this status source behind the **availability**, **syntax**, or
**reputation** checkers.

DNSLOOKUP
"""""""""

This is the status source that is supplied when the DNS lookup is the reason
behind the status. It is generally followed by either the :code:`ACTIVE` or
:code:`INACTIVE` status.

You will find this status source exclusively behind the **availability**
checker.

NETINFO
"""""""

This is the status source that is supplied when the Network Information is the
reason behind the status. It is exclusively followed by the :code:`ACTIVE`
status.

You will find this status source exclusively behind the **availability**
checker.

HTTP CODE
"""""""""

This is the status source that is supplied when the HTTP Status Code is the
reason behind the status. It is generally followed by either the
:code:`ACTIVE`, or :code:`INACTIVE` status.

You will find this status source exclusively behind the **availability**
checker.

REPUTATION
""""""""""

This is the status source that is supplied when the reputation lookup is the
reason behind the status. It is generally followed by either the
:code:`ACTIVE`, :code:`SANE`, or :code:`MALICIOUS` status.

You may find this status source behind the **availability** or **reputation**
checkers.

SPECIAL
"""""""

This is the status source that is supplied when our own sets of special rules
are the reasons behind the status. It is generally followed by either the
:code:`ACTIVE`, or :code:`INACTIVE` status.

You will find this status source exclusively behind the **availability**
checker.