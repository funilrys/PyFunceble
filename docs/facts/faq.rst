Frequently Asked Questions
==========================

How to speed up the test process?
---------------------------------

.. warning::
    Beware, when talking about speed a lot a thing have to be taken in consideration.
    Indeed here is a non exhaustive list of things which fluctuate testing speed.

    * Bandwidth.
    * DNS Server response time.
    * CPU.
    * ISP blocking a big amount of connection to the outside world.
    * Our databases management (do not apply for MySQL and MariaDB format).
    * Amount of data to test.
    * ...

I have a dedicated server or machine just for PyFunceble
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply increase the number of maximal workers PyFunceble is allowed to use
through the `--max-workers <../usage/index.html#w-max-workers>`_ argument.

By default the number of workers is equal to:

::

    CPU CORES - 2

meaning that if you have 8 CPU cores, the value will be automatically set to
:code:`6`.


.. warning::
    Keep in mind that the :code:`--max-workers` mostly - if not only - affects
    the tester processes. Because we want to safely write the files, we still
    need a single processes which read the submitted results and generate the
    outputs.

    The reason we added this to PyFunceble :code:`4.0.0` is we don't want to
    have a wrongly formatted output file.
