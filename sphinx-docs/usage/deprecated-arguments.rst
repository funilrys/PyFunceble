Deprecated arguments
--------------------

The following arguments have previous been in use by PyFunceble, these are
now deprecated and should in some cases be replaced with alternative args.

In other cases the old feature have either been included into a other functional
or simply been removed as it was obselete to keep the function within 
Pyfunceble v4.x.

This is happening because PyFunceble is evolving over time and features
comes and goes.

------

:code:`-ad`
^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--adblock <index.html#adblock>`_


------

:code:`-nw` | :code:`--no-whois`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--whois-lookup <index.html#whois-lookup>`_


------

:code:`--shadow-file` | :code:`--shadow`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: N/A


------

:code:`--use-reputation-data`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `reputation-lookup <index.html#reputation-lookup>`_


------

:code:`--dns-lookup-over-tcp`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    See: `--dns-protocol <index.html#dns-protocol>`_


------

:code:`-db | --database`
^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--inactive-db <index.html#inactive-db>`_


------

:code:`-dbc "something" | --days-between-db-clean`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: N/A


------

:code:`-json`
^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: N/A


------

:code:`-less`
^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `-a | --all <index.html#a-all>`_


------

:code:`-nf`
^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--no-files <index.html#no-files>`_


------

:code:`-nl` | :code:`--no-logs`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--no-files <index.html#no-files>`_


------

:code:`-nu | --no-unified`
^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--unified-results <index.html#unified-results>`_


------

:code:`-ns|--no-special`
    .. deprecated:: 4.0.0

    Replacement: `--special-lookup <index.html#special-lookup>`_

In the .code:`.PyFunceble_production.yaml` the value have changed from
:code:`no_special` to :code:`special`


------

:code:`--split`
^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--unified-results <index.html#unified-results>`_


------

:code:`--store-whois`
^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: N/A


------

:code:`-m | --multiprocess`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Integrated into `-w | --max-workers <index.html#w-max-workers>`_


------

:code:`-p | --processes`
^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `-w | --max-workers <index.html#w-max-workers>`_


------

:code:`--multiprocess-merging-mode`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: N/A


------

:code:`--autosave-minutes`
^^^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--ci-max-minutes <index.html#ci-max-minutes>`_


------

:code:`--cmd`
^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: `--ci-command <index.html#ci-command-something-cmd-something>`_


------

:code:`--cmd-before-end`
^^^^^^^^^^^^^^^^^^^^^^^^
    .. deprecated:: 4.0.0

    Replacement: :code:`--ci-end-command`


------
