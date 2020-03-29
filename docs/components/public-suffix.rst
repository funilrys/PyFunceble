The Public Suffix List
----------------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

We use it in the process of checking the validity of domains.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the parser code ? It's here :func:`PyFunceble.lookup.publicsuffix.PublicSuffix`!

The copy of the public suffix list we use is saved into the :code:`public-suffix.json` file.
It is formatted like below and is automatically merged for the end-user before
each test run.

::

    {
        "extension": [
            "suffix1.extension",
            "suffix2.extension",
            "suffix3.extension"
        ]
    }


In-app, while testing for domain(s), we use it in order to know if we are checking
for a subdomain or not.

How to generate it manually?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can't and should not as we are automatically generating it every 24 hours.
But, using the :code:`--public-suffix` argument will do the job on purpose.