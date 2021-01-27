Frequently Asked Questions
==========================

How to speed up the test process?
---------------------------------

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

Simply use the :code:`-m | --multiprocess` argument to activate
the usage of multiple processes.
You should in addition to the :code:`-m` specify the :code:`-p | --processes`
argument.

If :code:`-p | --processes` is avoided, the script will use the number of
available CPU cores.

You might therefore which to specify the number of simultaneous processes to
be used, otherwise your will be "unable" to use the computer/server for other
things while running PyFunceble as all of your CPU threads is used by PyFunceble.

.. note::
    A good number for :code:`-p` is your number of :code:`CPU_cores -1`, to leave room for orther processes to work.
    Unless you have a dedicated installation for this work.


    Inside a Unix based system, you can use this code snippet to see how many CPU and cores you have.

    ::

        $: lscpu | grep -E '^Thread|^Core|^Socket|^CPU\('

    or

    ::

	$: nproc --ignore=1

	This will count the number of CPU threads subtracted 1 to use for DB,
	SQL. If you runs PyFunceble on your workstation you might subtract 2
	threads, or you computer will be pretty "dead"

	See also ``man nproc`` or ``nproc --help``

.. warning::
    DO NOT try to exceed your total number of CPU cores with (:code:`-p | --processes`),
    if you want to keep your machine somehow alive and healthy.

I do not have multiple CPU
^^^^^^^^^^^^^^^^^^^^^^^^^^

In case you only have a single core, you should disable the usage of
the WHOIS lookup by adding the :code:`--no-whois` to your command line
or switching the value of :code:`no_whois` to :code:`True` in your
configuration file.

As example:

::

    $ PyFunceble --no-whois -d example.net


This action will speed up the script because it only
use the equivalent of :code:`nslookup` and the
:code:`HTTP status code` to determine the availability status.

.. warning::

    PyFunceble request the WHOIS record in order to avoid specific false
    positive cases.
    If the usage of WHOIS request is disabled, all domains which are still
    registered but not assigned to an IP address, would be flagged as
    :code:`INACTIVE`.

    It's not a problem if you keep/use the database system because the domain
    will be retested over time.
    But please keep in mind, that without the database system, the accuracy
    of the result is not guaranteed.
