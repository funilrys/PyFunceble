:code:`adblock`
^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the adblock format decoding.

.. note::

    If this index is set to :code:`True`, every time we read a given file, we try to extract the elements that are present.

    We basically only decode the adblock format.

.. note::

    If this index is set to :code:`False`, every time we read a given file, we will consider one line as an element to test.

:code:`aggressive`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable some aggressive settings.

.. warning::
    This option is available but please keep in mind that the some settings which it enable are experimental.

:code:`auto_continue`
^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the auto continue system.

:code:`command`
^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the command to run before each commit (except the final one).

.. note::
    The parsed command is called only if :code:`auto_continue` and :code:`ci` are set to :code:`True`.

:code:`command_before_end`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the command to run before the final commit.

.. note::
    The parsed command is called only if :code:`auto_continue` and :code:`ci` are set to :code:`True`.

.. note::
    Understand by final commit the commit which will deliver the last element we have to test.

:code:`cooldow_time`
^^^^^^^^^^^^^^^^^^^^

    **Type:**: :code:`float`

    **Default value:** :code:`null`

    **Description:** Set the cooldown time to apply between each test.

.. note::
    This index take only effect from the CLI. Not from the API.

:code:`custom_ip`
^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`"0.0.0.0"`

    **Description:** Set the custom IP to use when we generate a line in the hosts file format.

.. note::
    This index has no effect if :code:`generate_hosts` is set to :code:`False`.

:code:`days_between_db_retest`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`integer`

    **Default value:** :code:`1`

    **Description:** Set the number of day(s) between each retest of the :code:`INACTIVE` and :code:`INVALID` elements which are present into :code:`inactive_db.json`.

.. note::
    This index has no effect if :code:`inactive_database` is set to :code:`False`.

:code:`days_between_inactive_db_clean`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`integer`

    **Default value:** :code:`28`

    **Description:**  Set the numbers of days since the introduction of a subject into :code:`inactive-db.json` for it to qualifies for deletion.

.. note::
    This index has no effect if :code:`inactive_database` is set to :code:`False`.

:code:`db_type`
^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`json`

    **Available values:** :code:`json`, :code:`mariadb`, :code:`mysql`

    **Description:** Set the database type to use everytime we create a database.


.. note::
    This feature is applied to the following subsystems:

    * Autocontinue physically located (JSON) at :code:`output/continue.json`.
    * InactiveDB physically located (JSON) at :code:`[config_dir]/inactive_db.json`.
    * Mining physically located (JSON) at :code:`[config_dir]/mining.json`.
    * WhoisDB physically located (JSON) at :code:`[config_dir]/whois.json`.

:code:`debug`
^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the generation of debug file(s).

.. note::
    This index has no effect if :code:`logs` is set to :code:`False`

.. warning::
    Do not touch this index unless you a have good reason to.

.. warning::
    Do not touch this index unless you have been invited to.

:code:`dns_lookup_over_tcp`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Make all DNS lookup with TCP instead of UDP.

:code:`dns_server`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`None` or :code:`list`

    **Default value:** :code:`null`

    **Description:** Set the DNS server(s) to work with.

.. note::
    When a list is given the following format is expected.

    ::

        dns_server:
          - dns1.example.org
          - dns2.example.org

.. note::
    You can specify a port number to use to the DNS server if needed.

    As example:

    ::

        - 127.0.1.53:5353

.. warning::
    We expect a DNS server(s). If no DNS server(s) is given. You'll almost for certain get all
    results as :code:`INACTIVE`

    This could happens in case you use :code:`--dns -f`

:code:`filter`
^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the element to filter.

.. note::
    This index should be initiated with a regular expression.

:code:`generate_complements`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the generation and test of the complements.

.. note::
    A complement is for example :code:`example.org` if :code:`www.example.org` is given and vice-versa.


:code:`generate_hosts`
^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the generation of the hosts file(s).

:code:`generate_json`
^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the generation of the JSON file(s).

:code:`header_printed`
^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Say to the system if the header has been already printed or not.

.. warning::
    Do not touch this index unless you have a good reason to.

:code:`hierarchical_sorting`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Say to the system if we have to sort the list and the outputs in a hierarchical order.

:code:`iana_whois_server`
^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`whois.iana.org`

    **Description:** Set the server to call to get the :code:`whois` referer of a given element.

.. note::
    This index is only used when generating the :code:`iana-domains-db.json` file.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`idna_conversion`
^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Tell the system to convert all domains to IDNA before testing.

.. note::
    We use `domain2idna`_ for the conversion.

.. warning:
    This feature is not supported for the URL testing.

.. _domain2idna: https://github.com/PyFunceble/domain2idna

:code:`inactive_database`
^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the usage of a database to store the :code:`INACTIVE` and :code:`INVALID` element to retest overtime.

:code:`less`
^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the output of every information of screen.

:code:`local`
^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the execution of the test(s) in a local or private network.

:code:`logs`
^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the output of all logs.

:code:`maximal_processes`
^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`integer`

    **Default value:** :code:`25`

    **Description:** Set the number of maximal simultaneous processes to use/create/run.

.. warning::
    If you omit the :code:`--processes` argument,
    we overwrite the default with the number of available CPU.

:code:`mining`
^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the mining subsystem.

:code:`multiprocess`
^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage of multiple processes instead of the default single process.

:code:`multiprocess_merging_mode`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`end`

    **Available values:** :code:`end`, :code:`live`

    **Description:** Set the multiprocess merging mode.

.. note::
    With the :code:`end` value, the merging of cross process data is made at the very end of the current instance.

.. note::
    With the :code:`live` value, the merging of cross process data is made after the processing of the maximal number of process.

    Which means that if you allow 5 processes, we will run 5 tests, merge, run 5 tests, merge and so on until the end.

:code:`no_files`
^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of any file(s).

:code:`no_special`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage of the SPECIAL rules - which are discribes in the source column section.

:code:`no_whois`
^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage of :code:`whois` in the tests.

:code:`plain_list_domain`
^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of the plain list of elements sorted by statuses.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`print_dots`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the printing of dots (:code:`.`) for the skipped subjects.

.. note::
    The idea is to not given the impression that we hang. Because most of the time, we don't.

:code:`quiet`
^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of output on the screen.

:code:`referer`
^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the referer of the element that is currently under test.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`reputation`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the reputation (only) testing.

.. warning::
    If this index is set to :code:`True`, we **ONLY** check for reputation, not availability nor syntax.

:code:`shadow_file`
^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage and generation of a shadow file before a the test of a file.

.. note::
    The shadow file, will just contain the actual list of subjects to test.

:code:`share_logs`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the logs sharing.


.. note::
    This index has no effect if :code:`logs` is set to :code:`False`.

:code:`show_execution_time`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the output of the execution time.

:code:`show_percentage`
^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the output of the percentage of each status.

:code:`simple`
^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the simple output mode.

.. note::
    If this index is set to :code:`True`, the system will only return the result inf format: :code:`tested.element STATUS`.

:code:`split`
^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the split of the results files.

.. note::
    Understand with "results files" the mirror of what is shown on screen.

:code:`store_whois_record`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the storage of the WHOIS record into the WHOIS DB.

.. warning::
    This does not disable the WHOIS DB functionality. It just not storing the full
    :code:`WHOIS` reply in the database.

.. note: See also `storing-whois <usage/index.html#store-whois>`_ for more information



:code:`syntax`
^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the syntax (only) testing.

.. warning::
    If this index is set to :code:`True`, we **ONLY** check for syntax, not availability nor reputation.

:code:`timeout`
^^^^^^^^^^^^^^^

    **Type:** :code:`integer`

    **Default value:** :code:`5`

    **Description:** Set the timeout to apply everytime it's possible to set one.

:code:`ci`
^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the CI autosaving system.

.. warning::
    Do not activate this index unless you are using PyFunceble under a supported CI environment/platform.

:code:`ci_autosave_commit`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`"PyFunceble - AutoSave"`

    **Description:** Set the default commit message we want to use when have to commit (save) but our tests are not yet completed.

:code:`ci_autosave_final_commit`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`"PyFunceble - Results"`

    **Description:** Set the default final commit message we want to use when we all tests are finished.

:code:`ci_autosave_minutes`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`integer`

    **Default value:** :code:`15`

    **Description:** Set the minimum of minutes we have to run before to automatically save our test results.

.. note::
    As many services are setting a rate limit per IP, it's a good idea to set this value between :code:`1` and :code:`15` minutes.

:code:`ci_distribution_branch`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`master`

    **Description:** Set the git branch where we are going to push our results.

.. note::
    The difference between this and :code:`ci_branch` is the fact
    that this branch will get the result only when the test were finished
    under the given :code:`ci_branch`.

    As example, this allow us to have 2 branches:

    - :code:`proceessing` (ci branch), for the tests with PyFunceble.
    - :code:`master` (ci distribution branch), for the distribution of the results of PyFunceble.

:code:`ci_branch`
^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`master`

    **Description:** Set the git branch where we are going to push our results.

:code:`unified`
^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of the unified results.

.. note::
    This index has no effect if :code:`split` is set to :code:`True`.

:code:`use_reputation_data`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage of reputation data while testing the availability of a given subject.

.. warning::
    This only have an effect when used along with the availability test.

:code:`verify_ssl_certificate`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the verification of the SSL/TLS certificate when testing for URL.

.. warning::
    If you set this index to :code:`True`, you may get **false positive** result.

    Indeed if the certificate is not registered to the CA or is simply invalid and the domain is still alive, you will always get :code:`INACTIVE` as output.


:code:`whois_database`
^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the usage of the whois database to avoid/bypass whois server requests rate limit.

:code:`wildcard`
^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the test of wildcards when testing for syntax.

.. warning::
    This is not taken into consideration if :code:`syntax` is set to :code:`False`.
