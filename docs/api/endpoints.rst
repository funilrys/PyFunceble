Available Checkers
------------------

Before starting to play with any checkers you need to understand 2 things:

- :class:`~PyFunceble.checker.base.CheckerBase`
- :class:`~PyFunceble.checker.status_base.CheckerStatusBase`

The first one is the base of all checkers, and the second is the base of all
status you get when you call the
:meth:`~PyFunceble.checker.base.CheckerBase.get_status` method.

Availability checkers
^^^^^^^^^^^^^^^^^^^^^

- Domain:
    - :class:`PyFunceble.checker.availability.domain.DomainAvailabilityChecker`

    or

    - :code:`from PyFunceble import DomainAvailabilityChecker`

- Domain and IP:
    - :class:`PyFunceble.checker.availability.domain_and_ip.DomainAndIPAvailabilityChecker`

    or

    - :code:`from PyFunceble import DomainAndIPAvailabilityChecker`


- URL:
    - :class:`PyFunceble.checker.availability.url.URLAvailabilityChecker`

    or

    - :code:`from PyFunceble import URLAvailabilityChecker`

- IP (v4 / v6):
    - :class:`PyFunceble.checker.availability.ip.IPAvailabilityChecker`

    or

    - :code:`from PyFunceble import IPAvailabilityChecker`

Syntax checkers
^^^^^^^^^^^^^^^

- Domain (Second level domain / Subdomain):
    - :class:`PyFunceble.checker.syntax.domain.DomainSyntaxChecker`

    or

    - :code:`from PyFunceble import DomainAvailabilityChecker`

- Second Level Domain:
    - :class:`PyFunceble.checker.syntax.second_lvl_domain.SecondLvlDomainSyntaxChecker`

    or

    - :code:`from PyFunceble import SecondLvlDomainSyntaxChecker`

- Subdomain:
    - :class:`PyFunceble.checker.syntax.subdomain.SubDomainSyntaxChecker`

    or

    - :code:`from PyFunceble import SubDomainSyntaxChecker`

- URL:
    - :class:`PyFunceble.checker.syntax.url.URLSyntaxChecker`

    or

    - :code:`from PyFunceble import URLSyntaxChecker`

- IP (v4 / v6):
    - :class:`PyFunceble.checker.syntax.ip.IPSyntaxChecker`

    or

    - :code:`from PyFunceble import IPSyntaxChecker`

- IPv4
    - :class:`PyFunceble.checker.syntax.ipv4.IPv4SyntaxChecker`

    or

    - :code:`from PyFunceble import IPv4SyntaxChecker`

- IPv6
    - :class:`PyFunceble.checker.syntax.ipv6.IPv6SyntaxChecker`

    or

    - :code:`from PyFunceble import IPv6SyntaxChecker`

Reputation checkers
^^^^^^^^^^^^^^^^^^^

- Domain:
    - :class:`PyFunceble.checker.reputation.domain.DomainReputationChecker`

    or

    - :code:`from PyFunceble import DomainReputationChecker`

- Domain and IP:
    - :class:`PyFunceble.checker.reputation.domain_and_ip.DomainAndIPReputationChecker`

    or

    - :code:`from PyFunceble import DomainAndIPReputationChecker`


- URL:
    - :class:`PyFunceble.checker.reputation.url.URLReputationChecker`

    or

    - :code:`from PyFunceble import URLReputationChecker`

- IP (v4 / v6):
    - :class:`PyFunceble.checker.reputation.ip.IPReputationChecker`

    or

    - :code:`from PyFunceble import IPReputationChecker`

Endpoints
---------

.. note::
    This section document what you can call directly when you use PyFunceble as an imported module.

.. warning::
    SOme of those methods may be deprecated and removed in the future (open for discussion).

.. automodule:: PyFunceble
   :members: