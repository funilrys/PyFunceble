Frequently Asked Questions
==========================

.. include:: dead-hosts/global-note.rst

How to speed up a bit the process/test?
----------------------------------------

For now, we only invite you to disable the usage/request of the WHOIS record.


This action will let the script speed up because we only use the equivalent of :code:`nslookup` and the HTTP status code to determine the status.

.. warning::

    We use/request the WHOIS record in order to avoid a specific false positive case.
    Indeed, if we disable the usage/request all domains which are still registered but not assigned to a specific IP will be flagged as :code:`INACTIVE`.

    It's not a problem if you keep/use the database system because the domain will be retested over time.
    But please keep in mind that without the database system we do not guarantee an accurate result.