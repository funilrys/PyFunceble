Multiprocessing
---------------


.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

Many people around the web who talked about PyFunceble were talking about one thing: We take time to run.

This component allows you to use more than one process if your machine has multiple CPU.

.. note::
    If you use this component you have to consider some limits:

    * Your connection speed.
    * Your machine.

    You might not even see a speed if one of both is slow or very slow.


    The following might not be touched by the limits but it really depends:

    * URL availability test.
    * Syntax test.
    * Test with DNS LOOKUP only - without WHOIS.

How does it work?
^^^^^^^^^^^^^^^^^

We test multiple subjects at the same time over several processes (1 process = 1 subject tested) and generate our results normally.

.. note::
    While using the JSON format for the database you might have to wait a bit at the very end
    as we need to merge all data we generated across the past created processes.

    Therefore, we recommend using the MySQL/MariaDB format which will get rid of that
    as everything is saved/synchronized at an almost real-time scale.

How to use it?
^^^^^^^^^^^^^^

Activation
""""""""""

You can simply change

::

    multiprocess: False

to

::

    multiprocess: True

Number of processes to create
"""""""""""""""""""""""""""""

Simply update the default value of

::

    maximal_processes: 25


.. warning::
    If you do not explicitly set the :code:`--processes` argument,
    we overwrite the default to the number of available CPU.

.. warning::
    If this value is less than :code:`2`, the system will
    automatically deactivate the multiprocessing.

Merging mode
""""""""""""

2 merging cross process (data) merging mode are available:

    * :code:`end`
    * :code:`live`

With the :code:`end` mode, we merge all data at the very end of the current instance.
With the :code:`live` mode, we merge all data while testing.

Simply update the default value of

::

    multiprocess_merging_mode: end

to the mode you want.