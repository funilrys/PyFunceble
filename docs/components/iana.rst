IANA Root Zone Database
=======================

Why do we need it?
------------------

We use it to check if an extension is valid/exists.

How does it work?
-----------------

.. note::
    Want to read the parser code ? It's here :func:`~PyFunceble.lookup.iana.IANA`!

The root zone database is saved into the :code:`iana-domains-db.json` file.
It is formatted like below and is automatically merged for the end-user before
each test run.

::

    {
        "extension": "whois_server"
    }

In-app, while testing for domain(s), we check if the extension is listed there before doing some extra verifications.
If not, domain(s) will be flagged as :code:`INVALID`.


How to generate it manually?
----------------------------

You can't. But using the :code:`--iana` argument will do the job on purpose.