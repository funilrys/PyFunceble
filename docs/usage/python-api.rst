PyFunceble Python API
---------------------

If you are working with a python script, module or even class,
you can integrate **PyFunceble** to your main logic by importing
it and using its API (cf: :ref:`api`).

This section will present some example of the way you can interact
with PyFunceble from anything written in Python.


Check the availability of a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import DomainAvailabilityChecker


    checker = DomainAvailabilityChecker()
    to_test = "github.com"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} ACTIVE ?", status.is_active())
    print(f"Is {to_test} INACTIVE ?", status.is_inactive())
    print(f"Is {to_test} INVALID ?", status.is_invalid())


Check the availability of an IP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import IPAvailabilityChecker


    checker = IPAvailabilityChecker()

    to_test = "192.0.2.1"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} ACTIVE ?", status.is_active())
    print(f"Is {to_test} INACTIVE ?", status.is_inactive())
    print(f"Is {to_test} INVALID ?", status.is_invalid())


Check the availability of an IP or domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import DomainAndIPAvailabilityChecker


    checker = DomainAndIPAvailabilityChecker()

    to_test = "github.com"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} ACTIVE ?", status.is_active())
    print(f"Is {to_test} INACTIVE ?", status.is_inactive())
    print(f"Is {to_test} INVALID ?", status.is_invalid())


Check the availability of URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import URLAvailabilityChecker


    checker = URLAvailabilityChecker()

    to_test = "http://github.com/PyFunceble"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} ACTIVE ?", status.is_active())
    print(f"Is {to_test} INACTIVE ?", status.is_inactive())
    print(f"Is {to_test} INVALID ?", status.is_invalid())


Check the syntax of domains
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import DomainSyntaxChecker


    checker = DomainSyntaxChecker()

    to_test = "github.com"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} VALID ?", status.is_valid())
    print(f"Is {to_test} INVALID ?", status.is_invalid())



Check the syntax of IP (v4 or v6)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import IPSyntaxChecker


    checker = IPSyntaxChecker()

    to_test = "192.0.2.1"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} VALID ?", status.is_valid())
    print(f"Is {to_test} INVALID ?", status.is_invalid())


Check the syntax of URLs
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python3

    from PyFunceble import URLSyntaxChecker


    checker = URLSyntaxChecker()

    to_test = "https://github.com/PyFunceble"

    # You can do it this way.
    status = checker.set_subject(to_test).get_status()

    # Or this way.
    checker.set_subject(to_test)
    status = checker.get_status()

    # We can convert the status to json.
    status_json = status.to_json()

    # We can convert the status to dict.
    status_dict = status.to_dict()

    # We can ask "questions".
    print(f"Is {to_test} VALID ?", status.is_valid())
    print(f"Is {to_test} INVALID ?", status.is_invalid())




.. _`our examples repository`: https://github.com/PyFunceble/examples
