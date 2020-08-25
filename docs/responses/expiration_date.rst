Expiration Date
---------------

Give us the expiration date of the tested element.

.. note::
    The API equivalent is :code:`expiration_date`.

Unknown (CLI)
^^^^^^^^^^^^^

:code:`Unknown` is returned when we could not extract the expiration date from :func:`PyFunceble.lookup.whois.WhoisLookup.request` outputs.

:code:`None` (API)
^^^^^^^^^^^^^^^^^^

:code:`None` is returned when we could not extract the expiration date from :func:`PyFunceble.lookup.whois.WhoisLookup.request` outputs.

A date
^^^^^^

Only if we could extract the expiration date from :func:`PyFunceble.lookup.whois.WhoisLookup.request`, the date becomes formatted like :code:`02-jan-2017`.
