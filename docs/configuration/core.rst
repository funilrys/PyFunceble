:code:`adblock`
---------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the adblock format decoding.

.. note::

    If this index is set to :code:`True`, every time we read a given file, we try to extract the elements that are present.

    We basically only decode the adblock format.

.. note::

    If this index is set to :code:`False`, every time we read a given file, we will consider one line as an element to test.

:code:`auto_continue`
---------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the auto continue system.

:code:`command`
---------------

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the command to run before each commit (except the final one).

.. note::
    The parsed command is called only if :code:`auto_continue` and :code:`travis` are set to :code:`True`.

:code:`command_before_end`
--------------------------

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the command to run before the final commit.

.. note::
    The parsed command is called only if :code:`auto_continue` and :code:`travis` are set to :code:`True`.

.. note::
    Understand by final commit the commit which will deliver the last element we have to test.

:code:`custom_ip`
-----------------

    **Type:** :code:`string`

    **Default value:** :code:`"0.0.0.0"`

    **Description:** Set the custom IP to use when we generate a line in the hosts file format.

.. note::
    This index has no effect if :code:`generate_hosts` is set to :code:`False`.

:code:`days_between_db_retest`
------------------------------

    **Type:** :code:`integer`

    **Default value:** :code:`1`

    **Description:** Set the number of day(s) between each retest of the :code:`INACTIVE` and :code:`INVALID` elements which are present into :code:`inactive_db.json`.

.. note::
    This index has no effect if :code:`inactive_database` is set to :code:`False`.

:code:`debug`
-------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the generation of debug file(s).

.. note::
    This index has no effect if :code:`logs` is set to :code:`False`

.. warning::
    Do not touch this index unless you a have good reason to.

.. warning::
    Do not touch this index unless you have been invited to.

:code:`filter`
--------------

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the element to filter.

.. note::
    This index should be initiated with a regular expression.

:code:`generate_hosts`
----------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the generation of the hosts file(s).

:code:`generate_json`
---------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the generation of the JSON file(s).

:code:`header_printed`
----------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Say to the system if the header has been already printed or not.

.. warning::
    Do not touch this index unless you have a good reason to.

:code:`hierarchical_sorting`
----------------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Say to the system if we have to sort the list and the outputs in a hierarchical order.

:code:`iana_whois_server`
-------------------------

    **Type:** :code:`string`

    **Default value:** :code:`whois.iana.org`

    **Description:** Set the server to call to get the :code:`whois` referer of a given element.

.. note::
    This index is only used when generating the :code:`iana-domains-db.json` file.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`idna_conversion`
-----------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Tell the system to convert all domains to IDNA before testing.

.. note::
    We use `domain2idna`_ for the conversion.

.. warning:
    This feature is not supported for the URL testing.

.. _domain2idna: https://github.com/funilrys/domain2idna

:code:`inactive_database`
-------------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the usage of a database to store the :code:`INACTIVE` and :code:`INVALID` element to retest overtime.

:code:`less`
------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the output of every information of screen.

:code:`local`
-------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the execution of the test(s) in a local or private network.

:code:`logs`
------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the output of all logs.

:code:`mining`
--------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the mining subsystem.

:code:`no_files`
----------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of any file(s).

:code:`no_special`
------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage of the SPECIAL rules - which are discribes in the source column section.

:code:`no_whois`
----------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the usage of :code:`whois` in the tests.

:code:`plain_list_domain`
-------------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of the plain list of elements sorted by statuses.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`quiet`
-------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of output on the screen.

:code:`referer`
---------------

    **Type:** :code:`string`

    **Default value:** :code:`""`

    **Description:** Set the referer of the element that is currently under test.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`seconds_before_http_timeout`
-----------------------------------

    **Type:** :code:`integer`

    **Default value:** :code:`3`

    **Description:** Set the timeout to apply to every HTTP status code request.

.. note::
    This index must be a multiple of :code:`3`.

:code:`share_logs`
------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the logs sharing.


.. note::
    This index has no effect if :code:`logs` is set to :code:`False`.

:code:`show_execution_time`
---------------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the output of the execution time.

:code:`show_percentage`
-----------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the output of the percentage of each status.

:code:`simple`
--------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the simple output mode.

.. note::
    If this index is set to :code:`True`, the system will only return the result inf format: :code:`tested.element STATUS`.

:code:`split`
-------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / disable the split of the results files.

.. note::
    Understand with "results files" the mirror of what is shown on screen.

:code:`syntax`
--------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the syntax (only) testing.

.. warning::
    If this index is set to :code:`True`, we **ONLY** check for syntax, not availability.

:code:`travis`
--------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the Travis CI autosaving system.

.. warning::
    Do not activate this index unless you are using PyFunceble under Travis CI.

:code:`travis_autosave_commit`
------------------------------

    **Type:** :code:`string`

    **Default value:** :code:`"PyFunceble - AutoSave"`

    **Description:** Set the default commit message we want to use when have to commit (save) but our tests are not yet completed.

:code:`travis_autosave_final_commit`
------------------------------------

    **Type:** :code:`string`

    **Default value:** :code:`"PyFunceble - Results"`

    **Description:** Set the default final commit message we want to use when we all tests are finished.

:code:`travis_autosave_minutes`
-------------------------------

    **Type:** :code:`integer`

    **Default value:** :code:`15`

    **Description:** Set the minimum of minutes we have to run before to automatically save our test results.

.. note::
    As many services are setting a rate limit per IP, it's a good idea to set this value between :code:`1` and :code:`15` minutes.

:code:`travis_branch`
---------------------

    **Type:** :code:`string`

    **Default value:** :code:`master`

    **Description:** Set the git branch where we are going to push our results.

:code:`unified`
---------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the generation of the unified results.

.. note::
    This index has no effect if :code:`split` is set to :code:`True`.

:code:`user_agent`
------------------

    **Type:** :code:`string`

    **Default value:** :code:`"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"`

    **Description:** Set the User-Agent to use every time we are requesting something from a web server other than our API.

:code:`verify_ssl_certificate`
------------------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the verification of the SSL/TLS certificate when testing for URL.

.. warning::
    If you set this index to :code:`True`, you may get **false positive** result.

    Indeed if the certificate is not registered to the CA or is simply invalid and the domain is still alive, you will always get :code:`INACTIVE` as output.


:code:`whois_database`
----------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the usage of the whois database to avoid/bypass whois server requests rate limit.
