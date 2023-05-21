Checkers
--------

As of PyFunceble :code:`4.0.0`, it is possible to use our checker without any
configuration of initialization of any sort. Simply choose your checker,
interact with it and get what you are looking for!


Getting started
^^^^^^^^^^^^^^^

Before starting to play with any checkers you need to understand 2 things:

- :class:`~PyFunceble.checker.base.CheckerBase`
- :class:`~PyFunceble.checker.status_base.CheckerStatusBase`

The first one is the base of all checkers, and the second is the base of all
status you get when you call the
:meth:`~PyFunceble.checker.base.CheckerBase.get_status` method.

Interaction with checkers
^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This method is the same for all available checkers.

Let's say we want to test the availability of :code:`github.com`.

We first have to select and prepare the checker.

.. code-block:: python3

    from PyFunceble import DomainAvailabilityChecker

    # Here we take the default configuration.
    checker = DomainAvailabilityChecker()


Then we just set the subject to work with.

.. code-block:: python3

    checker.set_subject("github.com")

We can then get the status.

.. code-block:: python3

    status = checker.get_status()

    # Note: You can also do it in one shot.
    status = checker.set_subject("github.com").get_status()

Once we have a status object, we can convert it to a different format.

.. code-block:: python3

    # To dict.
    status_dict = status.to_dict()

    # To JSON.
    status_json = status.to_json()

We can also interact with any of the attributes of the status object.

.. code-block:: python3

    # This is the status.
    print("GitHub is", status.status)

But finally, and probably most importantly, we can ask questions.

.. warning::
    Each checker have their own set of methods. Be sure to read them or follow
    the autocomplete of your editor.

.. code-block:: python3

    # Is it active ?
    print("Is GitHub active ?", status.is_active())

    # Is it inactive ?
    print("Is GitHub inactive ?", status.is_inactive())

    # Is it invalid ?
    print("Is github.com invalid ?", status.is_invalid())


Available Checkers
^^^^^^^^^^^^^^^^^^

In this section you can find the list of available checkers and how to import
them.

Availability checkers
"""""""""""""""""""""

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
