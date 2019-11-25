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

Simply use the :code:`-m | --multiprocess` argument to activate the usage of multiple processes.
You can in addition to that use the :code:`-p | --processes` argument to tell us the number of simultaneous process to run.

.. note::
    A god number for :code:`-p` is your number of CPU cores -1, to leave room for orther processes to work. Unless you have a dedicated installation for this work.
    
    You can use this code snippet to see how many CPU and cores you have. This snippet can also be used on CI/CD's like `Travis-CI <https://travis-ci.org/>`_ and `Gitlab <https://gitlab.com/>`_.
Find number or cores:
::
    echo "CPU's" && lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('

.. warning::
    Try not to exceed your total number of CPU cores (as :code:`-p | --processes`) if you want to keep your machine somehow alive and healthy.

I do not have multiple CPU
^^^^^^^^^^^^^^^^^^^^^^^^^^

In case you only have a single core you should be disabling the usage of the WHOIS lookup by adding the :code:`-wdb | --whois-database` to your line of commands.

Example:
::
    pyfunceble -wdb -d example.net


This action will speed up the script because it only use the equivalent of :code:`nslookup` and the `HTTP status code` to determine the availebilty status.

.. warning::

    PyFunceble request the WHOIS databses (ripe.tld) in order to avoid specific false positive case.
    If the usage of WHOIS request was disabled all domains, which are still registered but not assigned to a IP address, would be flagged as :code:`INACTIVE`.

    It's not a problem if you keep/use the database system because the domain will be retested over time.
    But please keep in mind that without the database system you are not guarantee an accurate result.
