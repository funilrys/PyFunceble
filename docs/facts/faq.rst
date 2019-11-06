Frequently Asked Questions
==========================

How to speed up a bit the process/test?
----------------------------------------

.. warning::
    Beware, when talking about speed a lot a thing have to be taken in consideration.
    Indeed here is a non exaustive list of things which fluctuate testing speed.

    * Bandwidth.
    * DNS Server response time.
    * CPU.
    * ISP blocking a big amount of connection to the outside world.
    * Our databases management (do not apply for MySQL and MariaDB format).
    * Amount of data to test.
    * ...

I have multiple CPU
^^^^^^^^^^^^^^^^^^^

Simply use the :code:`--multiprocess` argument to activate the usage of multiple processes.
You can in addition of that use the :code:`--processes` argument to tell us the number of simultaneous process to run.

.. warning::
    Try not to exceed your number of CPU (as :code:`--processes`) if you want to keep your machine somehow alive and healthy.

I do not have multiple CPU
^^^^^^^^^^^^^^^^^^^^^^^^^^

We invite you to disable the usage/request of the WHOIS record.


This action will let the script speed up because we only use the equivalent of :code:`nslookup` and the HTTP status code to determine the status.

.. warning::

    We use/request the WHOIS record in order to avoid a specific false positive case.
    Indeed, if we disable the usage/request all domains which are still registered but not assigned to a specific IP will be flagged as :code:`INACTIVE`.

    It's not a problem if you keep/use the database system because the domain will be retested over time.
    But please keep in mind that without the database system we do not guarantee an accurate result.