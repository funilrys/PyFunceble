:code:`cli_testing`
^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the CLI testing.

:code:`cli_testing[hosts_ip]`
"""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`"0.0.0.0"`

    **Description:** Sets the IP to prefix each lines of the hosts file.

:code:`cli_testing[max_workers]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`integer`

    **Default value:** :code:`null`

    **Description:** Sets the number of maximal processes workers that we are
    allowed to allocate for the testing.

.. warning::
    If set to :code:`null`, we use the default value calculated from your
    machine ressources. Meaning:

    ::

        CPU cores - 2

:code:`cli_testing[autocontinue]`
"""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the automatic continuation subsystem.

:code:`cli_testing[inactive_db]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of a "database" to store
    all :code:`INVALID` and :code:`INACTIVE` subject for continuous retest.

:code:`cli_testing[whois_db]`
"""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the uage of a "database" to store
    the expiration date of all domains with a valid expiration date.

.. warning::
    We do not recomend you to disable this. In fact, this is your safety against
    the rate limite imposed by most WHOIS servers.

:code:`cli_testing[cidr_expand]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the expansion of CIDR formatted
    addresses.

:code:`cli_testing[complements]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activate or disables the generation and test of the
    complements of a given subject.

.. note::
    A complement is for example :code:`example.org` if
    :code:`www.example.org` is given and vice-versa.


:code:`cli_testing[cooldown_time]`
""""""""""""""""""""""""""""""""""

    **Type:**: :code:`float`

    **Default value:** :code:`0.0`

    **Description:** Sets the cooldown time to apply between each test.

:code:`cli_testing[db_type]`
""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`csv`

    **Available values:** :code:`csv`, :code:`mariadb`, :code:`mysql`, :code:`postgresql`.

    **Description:** Sets the database type (or engine) to use everytime
    we create a database or a storage of a potentially huge dataset.

:code:`cli_testing[file_filter]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`null`

    **Description:** A regular expression which we use to filter the subjects
    to (actually) test.

:code:`cli_testing[mining]`
"""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the mining subsystem.

:code:`cli_testing[local_network]`
""""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the consideration of the test(s) in
    or for a local or private network context.

:code:`cli_testing[preload_file]`
"""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the preloading of the given input
    files. When this is activates, we preload the given files into the
    auto continue subsystem dataset in order to optimize some of our
    processes regarding the auto continue.

    .. note::
        This option does not have any effect if the auto continue subsystem is
        disabled.

:code:`cli_testing[chancy_tester]`
""""""""""""""""""""""""""""""""""

    .. versionadded:: 4.1.0b4.dev

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates a chancy mode that unleashes the safety workflow
    in place.

    .. warning::
        You shouldn't have to use this unless you feel really lucky and trust your
        machine.

        This mode makes things look 'fast', but it may produce some unexpected
        results if :code:`N` process simultaneously write the same output file.

        This mode makes the graphical CLI output unparsable - either.

        **MAY THE FORCE BE WITH YOU!**

:code:`cli_testing[ci]`
"""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Configures everything related to the Continuous Integration.

:code:`cli_testing[ci][active]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the Continuous Integration mechanism.

:code:`cli_testing[ci][commit_message]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`"PyFunceble - AutoSave"`

    **Description:** Sets the commit message to apply everytime we have
    to apply a commit except for the really last one.

:code:`cli_testing[ci][end_commit_message]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`"PyFunceble - Results"`

    **Description:** Sets the commit message to apply at the really end.

:code:`cli_testing[ci][max_exec_minutes]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`integer`

    **Default value:** :code:`15`

    **Description:** Sets the number of minutes to wait before starting to
    stop a CI session.

.. note::
    As many services are setting a rate limit per IP, it's a good idea to set
    this value between :code:`1` and :code:`15` minute(s).

:code:`cli_testing[ci][branch]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`master`

    **Description:** Sets our git working branch. This is the branch from where
    we are supposed to store the tests (excepts the final results).

:code:`cli_testing[ci][distribution_branch]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`master`

    **Description:** Sets our git distributions branch. This is the branch from
    where we are supposed to store and push the final results.

:code:`cli_testing[ci][command]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`null`

    **Description:** Sets the command to execute before each commit
    (except the final one).

:code:`cli_testing[ci][end_command]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`null`

    **Description:** Sets the command to execute before the final commit.

:code:`cli_testing[display_mode]`
"""""""""""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Configures everything related to what is displayed.

:code:`cli_testing[display_mode][dots]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activate or disables the printing of dots or other
    characters when we skip the test of a subjec.

:code:`cli_testing[display_mode][dots]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activate or disables the display of dots or other
    characters when we skip the test of a subjec.

:code:`cli_testing[display_mode][execution_time]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the display of the execution time.

:code:`cli_testing[display_mode][percentage]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the display and generation of the
    percentage - file - of each status.

:code:`cli_testing[display_mode][registrar]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the display and generation of the
    (top) registrar - file.

:code:`cli_testing[display_mode][quiet]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the display of output to the
    terminal.

.. warning::
    If the the dots mode is activate, this option will still allow them to work.

:code:`cli_testing[display_mode][less]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the display of the minimal
    information in the table we print to stdout.

:code:`cli_testing[display_mode][all]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the disply of the all
    information in the table we print to stdout.


:code:`cli_testing[display_mode][simple]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the simple output mode.

.. note::
    When this mode is active, the system will only return the result in the
    following format: :code:`example.org ACTIVE`.

:code:`cli_testing[display_mode][status]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string` | :code:`list`

    **Default value:** :code:`all`

    **Available values:** :code:`all`, :code:`ACTIVE`, :code:`INACTIVE`,
    :code:`INVALID`, :code:`VALID`, :code:`SANE`, :code:`MALICIOUS`

    **Description:** Sets the status that we are allowed to print to STDOUT.

.. note::
    A list of status can be given if you want to filter multiple status at once.

:code:`cli_testing[display_mode][colour]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the coloration to STDOUT.

:code:`cli_testing[display_mode][max_registrar]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`integer`

    **Default value:** :code:`15`

    **Description:** Sets the maximum number of registrar to display.

.. warning::
    This value is only used when the registrar mode is activated.

.. note::
    This value doesn't have any effect with the generated files.

:code:`cli_testing[testing_mode]`
"""""""""""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Configures the testing mode to apply.

.. warning::
    Only one of those is take in consideration.

    Here is the priority / checking order:

    1. :code:`syntax`
    2. :code:`reputation`
    3. :code:`availability`

:code:`cli_testing[testing_mode][availability]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the availability checker.

.. note::
    This is the default mode.

:code:`cli_testing[testing_mode][syntax]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the syntax checker.

:code:`cli_testing[testing_mode][reputation]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the reputation checker.


:code:`cli_testing[days_between]`
"""""""""""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Configures some days related events.

:code:`cli_testing[days_between][db_clean]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`integer`

    **Default value:** :code:`28`

    **Description:**  Sets the numbers of days since the introduction of a
    subject into the inactive dataset before it gets deleted.

.. warning::
    As of PyFunceble :code:`4.0.0` this is not actively implemented.

:code:`cli_testing[days_between][db_retest]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`integer`

    **Default value:** :code:`28`

    **Description:**  Sets the numbers of days since the introduction of a
    subject into the inactive dataset before it gets retested.

:code:`cli_testing[sorting_mode]`
"""""""""""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Configures the sorting mode to apply.

.. warning::
    Only one of those is take in consideration.

    Here is the priority / checking order:

    1. :code:`hierarchical`
    2. :code:`standard`

:code:`cli_testing[sorting_mode][hierarchical]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the sorting of the files content
    (output) in a hierarchical order.

:code:`cli_testing[sorting_mode][standard]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the sorting of the files content
    (output) in our standard order.


:code:`cli_testing[file_generation]`
""""""""""""""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Configures everything related to the file generation.

:code:`cli_testing[file_generation][no_file]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the generation of any non-logs
    file(s).

:code:`cli_testing[file_generation][no_file]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the generation of any non-logs
    file(s).

:code:`cli_testing[file_generation][hosts]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the generation of the hosts file(s).

:code:`cli_testing[file_generation][plain]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the generation of the RAW file(s).
    What is meant is a list with only a list of subject (one per line).

:code:`cli_testing[file_generation][analytic]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the generation of the analytic
    file(s).

:code:`cli_testing[file_generation][unified_results]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the generation of the unified results
    file instead of the splitted one.

:code:`cli_testing[file_generation][merge_output_dirs]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the merging of the outputs of all
    inputted files inside a single subdirectory as opposed to the normal
    behavior.


