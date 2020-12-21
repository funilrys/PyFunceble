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

I have a dedicated server or machine just for PyFunceble
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply increase the number of maximal workers PyFunceble is allowed to use
throught the :code:`--max-workers` argument.

By default the number of workers is equal to:

::

    CPU CORES * 5

meaning that if you have 8 CPU cores, the value will be automatically set to
:code:`40`.


.. warning::
    Keep in mind that the :code:`--max-workers` mostly - if not only - affects
    the tester threads. Because we want to safely write the files, we still
    need a single thread which read the submitted results and generate the
    outputs.

    The reason we did that with :code:`4.0.0` is because, we don't want to
    have a wrongly formatted output file.
