From a terminal
---------------

:code:`--help`
^^^^^^^^^^^^^^

    Show the help message and exit.

:code:`-v` | :code:`--version`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Show the version of PyFunceble and exit.

Source
^^^^^^

:code:`-d "something"` | :code:`--domain "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""""

    Test one or more domains, separated by spaces.

.. note::

    This argument takes one or more values.

    As example:

    ::

        $ PyFunceble -d example.org example.net

.. note::
    When this option is used, no output files are generated.

:code:`-url "something"` | :code:`--url "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""

    Test one or more full URL, separated by spaces.

.. note::
    When we test the availability of a URL, we (only) check the HTTP status
    code of the given URL.

.. note::
    This argument takes one or more values.

    As example:

    ::

        $ PyFunceble -u https://example.org https://example.com

:code:`-f "something"` | :code:`--file "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""

    Read a local or remote (RAW link) file and test all domains inside it.
    If remote (RAW link) file is given, PyFunceble will download it,
    and test the content of the given RAW link as if it was a locally stored
    file.

    Multiple space separated files can be given.

.. note::
    This argument takes one or more values.

    As example:

    ::

        $ PyFunceble -f test_this test_that



:code:`-uf "something"` | :code:`--url-file "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Read a local or remote (RAW link) file and test all (full) URLs inside it.
    If remote (RAW link) file is given, PyFunceble will download it,
    and test the content of the given RAW link as if it was a locally stored
    file.

.. note::
    This argument takes one or more values.

    As example:

    ::

        $ PyFunceble -uf test_this test_tha

.. note::
    We consider one line as one URL to test.

.. note::
    This argument test if a URL which is inside the given file is available.
    It ONLY tests full URLs.

    As example:

    ::

        $ PyFunceble -uf `https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.travis/lists/url`

    will download the given URL and test for its content assuming that each
    line represents a URL to test.

.. warning::
    A test with this argument consists of the comparison of the status code.
    No WHOIS record will be requested nor DNS Lookup will be done.


Source filtering, decoding, conversion and expansion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:code:`--adblock`
"""""""""""""""""

    Activates or disables the decoding of the adblock format.

    **Default value:** :code:`False`

.. note::
    If this argument is activated the system will extract all domains or
    IP from the given adblock file.

:code:`--complements`
"""""""""""""""""""""

    Activates or disables the generation and test of the complements.
    A complement is for example :code:`example.org` if :code:`www.example.org`
    is given and vice-versa.

    **Default value:** :code:`False`

:code:`--filter "something"`
""""""""""""""""""""""""""""

    Regex to match in order to test a given line.

    **Default value:** :code:`None`

Want to test all :code:`blogspot` from your list? This argument allows you to
do that!

.. note::
    This argument should be a regex expression.

:code:`--mining`
""""""""""""""""

    Activates or disables the mining subsystem usage.

    **Default value:** :code:`False`

Want to find domain or URL linked to a domain in your list? This argument will
exactly do that.

:code:`--rpz`
"""""""""""""

    Activates or disables the decoding of RPZ policies
    from each given input files.

    **Default value:** :code:`False`

:code:`--wildcard`
""""""""""""""""""

    Activates or disables the decoding of wildcards for each given input files.

    **Default value:** :code:`False`

Test control
^^^^^^^^^^^^

:code:`-c` | :code:`--auto-continue` | :code:`--continue`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Activates or disables the autocontinue subsystem.

    **Default value:** :code:`True`

This argument activates or deactivates the auto-continue subsystem.
Indeed, as we can automatically continue if the script has been stopped,
this switch allows us to disable or enable the usage of that specific
subsystem.

:code:`--cooldown-time`
"""""""""""""""""""""""

    Sets the cooldown time (in second) to apply between each test.

    **Default value:** :code:`0.0`

This argument applies a number of seconds to sleep before/between each test.

:code:`--local`
"""""""""""""""

    Activates or disables the consideration of the test(s) in
    or for a local or private network context.

    **Default value:** :code:`False`

Want to run a test over a local or private network? This argument will disable
the limitation which does not apply to private networks.

:code:`--dns-lookup`
""""""""""""""""""""

    Activates or disables the usage of the DNS lookup whether
    possible.

    **Default value:** :code:`True`

Don't want to perform some DNS lookup ? This argument is for you.


:code:`--http-status-code-lookup` | :code:`--http`
""""""""""""""""""""""""""""""""""""""""""""""""""

    Activates or disables the usage of the HTTP status code
    whether possible.

    **Default value:** :code:`True`

Don't want to take the result of the HTTP code execution into consideration?
This argument allows you to disable that!

:code:`--netinfo-lookup`
""""""""""""""""""""""""

    Activates or disables the usage of the network information
    (or network socket) whether possible.

    **Default value:** :code:`True`

Don't want to perform some netinfo lookup ? This argument is for you.

:code:`--special-lookup`
""""""""""""""""""""""""

    Activates or disables the usage of our SPECIAL and extra
    rules whether possible.

    **Default value:** :code:`True`

Don't want to use/apply the SPECIAL rules - which are explained in the source
column section? This argument disables them all.


:code:`--whois-lookup`
""""""""""""""""""""""

   Activates or disables the usage of the WHOIS record
   (or better said the expiration date in it) whether possible.

    **Default value:** :code:`True`

Don't want to use or take into consideration the results from :code:`whois`?
This argument allows you to disable it!

:code:`--reputation-lookup`
"""""""""""""""""""""""""""

   Activates or disables the usage of the reputation dataset
   whether possible.

    **Default value:** :code:`False`

Want to take the reputation data into consideration?
This argument is for you.

:code:`--reputation`
""""""""""""""""""""

    Activates or disables the reputation checker.

    **Default value:** :code:`False`

:code:`--syntax`
""""""""""""""""

    Activates or disables the syntax checker.

    **Default value:** :code:`False`

:code:`-t "something"` | :code:`--timeout "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the default timeout to apply to each lookup utilities
    everytime it is possible to define a timeout.

    **Default value:** :code:`5`

:code:`-ua "something"` | :code:`--user-agent "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the user agent to use.

.. warning::
    If not given, we try to get the latest (automatically) for you

:code:`-vsc` | :code:`--verify-ssl-certificate`
"""""""""""""""""""""""""""""""""""""""""""""""

    Activates or disables the verification of the SSL/TLS certificate when
    testing for URL.

    **Default value:** :code:`False`

    .. warning::
        If you activate the verification of the SSL/TLS certificate, you may get
        **false-positive** results.

        Indeed if the certificate is not registered to the CA or is simply
        invalid and the domain is still alive, you will always get
        :code:`INACTIVE` as output.

DNS control
^^^^^^^^^^^

:code:`--dns`
"""""""""""""

    Sets one or more DNS server(s) to use during testing.
    Separated by spaces.


    **Default value:** :code:`Follow OS DNS` ==> :code:`None`

.. warning::
    We expect a DNS server(s). If no DNS server(s) is given. You'll almost for
    certain get all results as :code:`INACTIVE`

    This could happen in case you use :code:`--dns -f`

.. note::
    You can specify a port number to use to the DNS server if needed.

    As example:

    ::

        - 127.0.1.53:5353

:code:`--dns-protocol`
""""""""""""""""""""""

    Sets the protocol to use for the DNS queries.

    **Default value:** :code:`False`

    **Available values:** :code:`UDP`, :code:`TCP`, :code:`HTTPS`, :code:`TLS`.


Databases
^^^^^^^^^

:code:`--inactive-database`
"""""""""""""""""""""""""""

    Switch the value of the usage of a database to store inactive domains of
    the currently tested list.

    **Default value:** :code:`True`

This argument will disable or enable the usage of a database which saves all
:code:`INACTIVE` and :code:`INVALID` domain of the given file over time.

:code:`--database-type`
"""""""""""""""""""""""

    Sets the database engine to use.

    **Default value:** :code:`csv`

    **Available values:** :code:`csv`, :code:`mariadb`, :code:`mysql`.

:code:`-dbr "something"` | :code:`--days-between-db-retest "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the numbers of days since the introduction of a
    subject into the inactive dataset before it gets retested.

    **Default value:** :code:`1`

.. note::
    This argument is only used if :code:`-db` or
    :code:`inactive_database : true` (under :code:`.PyFunceble.yaml`) are
    activated.

:code:`-wdb` | :code:`--whois-database`
"""""""""""""""""""""""""""""""""""""""

    Activates or disables the uage of a "database" to store
    the expiration date of all domains with a valid expiration date.

    **Default value:** :code:`True`

Output control
^^^^^^^^^^^^^^

:code:`-a` | :code:`--all`
""""""""""""""""""""""""""

    Activates or disables the disply of the all information in the table we
    print to stdout.

    **Default value:** :code:`False`

    **When activated:**

        ::


            Domain                        Status      Expiration Date   Source     HTTP Code  Checker
            ----------------------------- ----------- ----------------- ---------- ---------- -------------
            pyfunceble.readthedocs.io     ACTIVE      Unknown           NSLOOKUP   302        AVAILABILITY



    **When deactivated:**


        ::

            Domain                        Status      Source
            ----------------------------- ----------- ----------
            pyfunceble.readthedocs.io     ACTIVE      SYNTAX

:code:`-ex` | :code:`--execution`
"""""""""""""""""""""""""""""""""

    Activates or disables the display of the execution time.

    **Default value:** :code:`False`

Want to know the execution time of your test? Well, this argument will let
you know!

:code:`--color` | :code:`--colour`
""""""""""""""""""""""""""""""""""

    Activates or disables the coloration to STDOUT.

    **Default value:** :code:`True`

Don't want any colour ? This argument is for you!

:code:`--display-status`
""""""""""""""""""""""""

    Sets the status that we are allowed to print to STDOUT.
    Multiple space separated statuses can be given.

    **Default value:** :code:`all`

    **Available values:** :code:`all`, :code:`ACTIVE`, :code:`INACTIVE`,
    :code:`INVALID`, :code:`VALID`, :code:`SANE`, :code:`MALICIOUS`

:code:`--hierarchical`
""""""""""""""""""""""

    Activates or disables the sorting of the files content (output) in a
    hierarchical order.

    **Default value:** :code:`True`

This argument will output the result listed in a hierarchical order.

:code:`-h` | :code:`--host`
"""""""""""""""""""""""""""

    Activates or disables the generation of the hosts file(s).

    **Default value:** :code:`True`

This argument will let the system know if it has to generate the hosts file
version of each status.

:code:`-ip "something"` | --hosts-ip "something"
""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the IP to prefix each lines of the hosts file.

    **Default value:** :code:`0.0.0.0`

:code:`--no-files`
""""""""""""""""""

    Activates or disables the generation of any non-logs file(s).

    **Default value:** :code:`False`

Want to disable the production of the outputted files? This argument is for
you!

:code:`--unified-results`
"""""""""""""""""""""""""

    Activates or disables the generation of the unified results
    file instead of the splitted one.

    **Default value:** :code:`True`

This argument disables the generation of the :code:`result.txt` file.

:code:`--percentage`
""""""""""""""""""""

    Activates or disables the display and generation of the
    percentage - file - of each status.

    **Default value:** :code:`True`

This argument will disable or enable the generation of the percentage of each
status.

:code:`--plain`
"""""""""""""""

    Activates or disables the generation of the RAW file(s).
    What is meant is a list with only a list of subject (one per line).

    **Default value:** :code:`False:`

Want to get a list with all domains for each status? The activation of this
argument does the work while testing!

:code:`--dots`
""""""""""""""

    Activate or disables the display of dots or other characters when we skip
    the test of a subjec.

    **Default value:** :code:`False`

:code:`-q` | :code:`--quiet`
""""""""""""""""""""""""""""

    Activates or disables the display of output to the terminal.

    **Default value:** :code:`False`

You prefer to run a program silently? This argument is for you!

:code:`--share-logs`
""""""""""""""""""""

    Switch the value of the sharing of logs.

    **Default value:** :code:`False`

Want to make PyFunceble a better tool? Share your logs with our API which
collect all logs!

:code:`-s` | :code:`--simple`
"""""""""""""""""""""""""""""

    Activates or disables the simple output mode.

    **Default value:** :code:`False`

Want as less as possible data on screen? This argument returns as less as
possible on screen!

Multithreading
^^^^^^^^^^^^^^

:code:`-w` | :code:`--max-workers`
""""""""""""""""""""""""""""""""""

    Sets the number of maximal worker to use.

    **Default value:** :code:`False`

.. note::
    If omitted, the number of available CPU cores multiplied by 5 will be used
    instead.


CI / CD
^^^^^^^

:code:`--ci-max-minutes`
""""""""""""""""""""""""

    Sets the number of minutes to wait before starting to stop a CI session.

    **Default value:** :code:`15`

:code:`--ci`
""""""""""""

    Activates or disables the Continuous Integration mechanism.

    **Default value:** :code:`False`

.. note::
    If you combine this argument with the :code:`--quiet` argument, the test
    will output a dotted line, where each dot (:code:`.`) represent one test
    result or input which was skipped because it was previously tested.

Want to use PyFunceble under a supported CI infrastructure/network? This
argument is suited for your needs!

:code:`--ci-branch`
"""""""""""""""""""

    Sets our git working branch. This is the branch from where
    we are supposed to store the tests (excepts the final results).

    **Default value:** :code:`master`

.. note::
    Currently the branch need to exist, but there are being worked on a path
    to have PyFunceble to create the sub-branch and finally merge it into the
    :code:`--ci-distribution-branch`

:code:`--ci-distribution-branch`
""""""""""""""""""""""""""""""""

    Sets our git distributions branch. This is the branch from where we are
    supposed to store and push the final results.

    **Default value:** :code:`master`

.. note::
    The difference between this and :code:`--ci-branch` is the fact
    that this branch will get the (final) result only when the test is finished
    under the given :code:`--ci-branch`.

    As an example, this allows us to have 2 branches:

    - :code:`proceessing` (CI branch), for the tests with PyFunceble.
    - :code:`master` (CI distribution branch), for the distribution of the
      results of PyFunceble.

:code:`--ci-command "something"` | :code:`--cmd "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the command to execute before each commit (except the final one).

    **Default value:** :code:`''`

.. note::
    In this example, :code:`something` should be a script or a program which
    have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are activated.

:code:`--ci-end-command "something"` | :code:`--cmd-before-end "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the command to execute before the final commit.

    **Default value:** :code:`''`

.. note::
    In this example, :code:`something` should be a script or a program which
    have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are activated.

:code:`--ci-commit-message "something"` | :code:`--commit-autosave-message "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the commit message to apply everytime we have to apply a commit except
    for the really last one.

    **Default value:** :code:`PyFunceble - AutoSave`

This argument allows us to set a custom commit message which is going to be
used as a commit message when saving.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we have to split the work into multiple
    processes because a list is too long or the timeout is reached.

.. warning::
    Please avoid the usage of :code:`[ci skip]` here.

:code:`--ci-end-commit-message "something"` | :code:`--commit-results-message "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Sets the commit message to apply at the really end.

    **Default value:** :code:`PyFunceble - Results`

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we reached the end of the list we are or
    have to test.

Global overview
^^^^^^^^^^^^^^^

::

    usage: pyfunceble [-d DOMAINS [DOMAINS ...]] [-u URLS [URLS ...]]
                    [-f FILES [FILES ...]] [-uf URL_FILES [URL_FILES ...]]
                    [--adblock] [--complements]
                    [--filter CLI_TESTING__FILE_FILTER] [--mining] [--rpz]
                    [--wildcard] [-c]
                    [--cooldown-time CLI_TESTING__COOLDOWN_TIME] [--local]
                    [--dns-lookup] [--http] [--netinfo-lookup]
                    [--special-lookup] [--whois-lookup] [--reputation-lookup]
                    [--reputation] [--syntax] [-t LOOKUP__TIMEOUT]
                    [-ua USER_AGENT__CUSTOM] [-vsc]
                    [--dns DNS__SERVER [DNS__SERVER ...]]
                    [--dns-protocol {UDP,TCP,HTTPS,TLS}] [--inactive-db]
                    [--database-type {csv,mariadb,mysql}]
                    [-dbr CLI_TESTING__DAYS_BETWEEN__DB_RETEST]
                    [-wdb CLI_TESTING__WHOIS_DB] [-a] [-ex] [--colour]
                    [--display-status {all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} [{all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} ...]]
                    [--hierarchical] [-h] [-ip CLI_TESTING__HOSTS_IP]
                    [--no-files] [--unified-results] [--percentage] [--plain]
                    [--dots] [-q] [-s] [-w CLI_TESTING__MAX_WORKERS]
                    [--ci-max-minutes CLI_TESTING__CI__MAX_EXEC_MINUTES] [--ci]
                    [--ci-branch CLI_TESTING__CI__BRANCH]
                    [--ci-distribution-branch CLI_TESTING__CI__DISTRIBUTION_BRANCH]
                    [--cmd CLI_TESTING__CI__COMMAND]
                    [--cmd-before-end CLI_TESTING__CI__END_COMMAND]
                    [--ci-commit-message CLI_TESTING__CI__COMMIT_MESSAGE]
                    [--ci-end-commit-message CLI_TESTING__CI__END_COMMIT_MESSAGE]
                    [--help] [-v]

    PyFunceble - The tool to check the availability or syntax of domain, IP or URL.

    optional arguments:
        --help                Show this help message and exit.
        -v, --version         Show the version of PyFunceble and exit.

    Source:
        -d DOMAINS [DOMAINS ...], --domain DOMAINS [DOMAINS ...]
                                Test one or more domains, separated by spaces.

                                When this option is used, no output files are generated.
        -u URLS [URLS ...], --url URLS [URLS ...]
                                Test one or more full URL, separated by spaces.
        -f FILES [FILES ...], --file FILES [FILES ...]
                                Read a local or remote (RAW link) file and test all domains inside it.
                                If remote (RAW link) file is given, PyFunceble will download it,
                                and test the content of the given RAW link as if it was a locally stored file.
        -uf URL_FILES [URL_FILES ...], --url-file URL_FILES [URL_FILES ...]
                                Read a local or remote (RAW link) file and test all (full) URLs inside it.
                                If remote (RAW link) file is given, PyFunceble will download it,
                                and test the content of the given RAW link as if it was a locally stored file.

                                This argument test if an URL is available. It ONLY test full URLs.

    Source filtering, decoding, conversion and expansion:
        --adblock             Activates or deactivates the decoding of the adblock format.
                                Configured value: False
        --complements         Activates or disables the generation and test of the
                                complements.
                                A complement is for example `example.org` if 'www.example.org'
                                is given and vice-versa.
                                Configured value: False
        --filter CLI_TESTING__FILE_FILTER
                                Regex to match in order to test a given line.
                                Configured value: None
        --mining              Activates or disables the mining subsystem.
                                Configured value: False
        --rpz                 Activates or disables the decoding of RPZ policies
                                from each given input files.
                                Configured value: False
        --wildcard            Activates or disables the decoding of wildcards for
                                each given input files.
                                Configured value: False

    Test control:
        -c, --auto-continue, --continue
                                Activates or disables the autocontinue subsystem.
                                Configured value: True
        --cooldown-time CLI_TESTING__COOLDOWN_TIME
                                Sets the cooldown time (in second) to apply between
                                each test.
                                Configured value: 0.0
        --local               Activates or disables the consideration of the test(s)
                                in or for a local or private network context.
                                Configured value: False
        --dns-lookup          Activates or disables the usage of the DNS lookup
                                whether possible.
                                Configured value: True
        --http, --http-status-code-lookup
                                Switch the value of the usage of HTTP code.
                                Configured value: True
        --netinfo-lookup      Activates or disables the usage of the network
                                information (or network socket) whether possible.
                                Configured value: True
        --special-lookup      Activates or disables the usage of our SPECIAL and
                                extra rules whether possible.
                                Configured value: True
        --whois-lookup        Activates or disables the usage of the WHOIS record
                                (or better said the expiration date in it) whether possible.
                                Configured value: True
        --reputation-lookup   Activates or disables the usage of the reputation
                                dataset whether possible.
                                Configured value: False
        --reputation          Activates or disables the reputation checker.
                                Configured value: False
        --syntax              Activates or disables the syntax checker.
                                Configured value: False
        -t LOOKUP__TIMEOUT, --timeout LOOKUP__TIMEOUT
                                Sets the default timeout to apply to each lookup
                                utilities everytime it is possible to define a timeout.
                                Configured value: 5
        -ua USER_AGENT__CUSTOM, --user-agent USER_AGENT__CUSTOM
                                Sets the user agent to use.

                                If not given, we try to get the lastest (automatically) for you.
        -vsc, --verify-ssl-certificate
                                Activates or disables the verification of the SSL/TLS
                                certificate when testing for URL.
                                Configured value: False

    DNS control:
        --dns DNS__SERVER [DNS__SERVER ...]
                                Sets one or more (space separated) DNS server(s) to use during testing.

                                To specify a port number for the DNS server you append
                                it as :port [ip:port].

                                If no port is specified, the default DNS port (53) is used.
                                Configured value: None
        --dns-protocol {UDP,TCP,HTTPS,TLS}
                                Sets the protocol to use for the DNS queries.
                                Configured value: 'UDP'

        Databases:
        --inactive-db         Activates or disables the usage of a 'database' to
                                store all 'INACTIVE' and 'INVALID'  subject for continuous retest.
                                Configured value: True
        --database-type {csv,mariadb,mysql}
                                Sets the database engine to use.
                                You can choose between the following: `csv | mariadb | mysql`
                                Configured value: 'csv'
        -dbr CLI_TESTING__DAYS_BETWEEN__DB_RETEST, --days-between-db-retest CLI_TESTING__DAYS_BETWEEN__DB_RETEST
                                Sets the numbers of days since the introduction of
                                subject into the inactive dataset before it gets retested.
                                Configured value: 1
        -wdb CLI_TESTING__WHOIS_DB, --whois-database CLI_TESTING__WHOIS_DB
                                Activates or disables the usage of a 'database' to
                                store the expiration date of all domains with a valid
                                expiration date.
                                Configured value: True

    Output control:
        -a, --all             Activates or disables the display of the all
                                information in the table we print to stdout.
                                Configured value: False
        -ex, --execution      Activates or disables the display of the execution time.
                                Configured value: False
        --colour, --color     Activates or disables the coloration to STDOUT.
                                Configured value: True
        --display-status {all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} [{all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} ...]
                                Sets the status that we are allowed to print to STDOUT.

                                Multiple space separated statuses can be given.
                                Configured value: 'all'
        --hierarchical        Activates or disables the sorting of the files
                                content (output) in a hierarchical order.
                                Configured value: False
        -h, --host            Activates or disables the generation of the
                                hosts file(s).
                                Configured value: True
        -ip CLI_TESTING__HOSTS_IP, --hosts-ip CLI_TESTING__HOSTS_IP
                                Sets the IP to prefix each lines of the hosts file.
                                Configured value: '0.0.0.0'
        --no-files            Activates or disables the generation of any non-logs
                                file(s).
                                Configured value: False
        --unified-results     Activates or disables the generation of the unified
                                results file instead of the splitted one.
                                Configured value: False
        --percentage          Activates or disables the display and generation
                                of the percentage - file - of each status.
                                Configured value: True
        --plain               Activates or disables the generation of the
                                RAW file(s). What is meant is a list with only a list of
                                subject (one per line).
                                Configured value: True
        --dots                Activate or disables the display of dots or other
                                characters when we skip the test of a subject.
                                Configured value: False
        -q, --quiet           Activates or disables the display of output to the
                                terminal.
                                Configured value: False
        -s, --simple          Activates or disables the simple output mode.
                                Configured value: False

    Multithreading:
        -w CLI_TESTING__MAX_WORKERS, --max-workers CLI_TESTING__MAX_WORKERS
                                Sets the number of maximal workers to use.
                                If not given, 40 (based on the current machine) will be applied.
                                Configured value: None

    CI / CD:
        --ci-max-minutes CLI_TESTING__CI__MAX_EXEC_MINUTES, --autosave-minutes CLI_TESTING__CI__MAX_EXEC_MINUTES
                                Sets the number of minutes to wait before starting
                                to stop a CI session.
                                Configured value: 15
        --ci                  Activates or disables the Continuous Integration
                                mechanism.
                                Configured value: False
        --ci-branch CLI_TESTING__CI__BRANCH
                                Sets our git working branch. This is the branch
                                from where we are supposed to store the tests
                                (excepts the final results).
                                Configured value: 'master'
        --ci-distribution-branch CLI_TESTING__CI__DISTRIBUTION_BRANCH
                                Sets our git distributions branch. This is the
                                branch from where we are supposed to store and push
                                the final results.
                                Configured value: 'master'
        --cmd CLI_TESTING__CI__COMMAND, --ci-command CLI_TESTING__CI__COMMAND
                                Sets the command to execute before each commit
                                (except the final one).
                                Configured value: None
        --cmd-before-end CLI_TESTING__CI__END_COMMAND, --ci-end-command CLI_TESTING__CI__END_COMMAND
                                Sets the command to execute before the final commit.
                                Configured value: None
        --ci-commit-message CLI_TESTING__CI__COMMIT_MESSAGE, --commit-autosave-message CLI_TESTING__CI__COMMIT_MESSAGE
                                Sets the commit message to apply everytime we have
                                to apply a commit except for the really last one.
                                Configured value: 'PyFunceble - AutoSave'
        --ci-end-commit-message CLI_TESTING__CI__END_COMMIT_MESSAGE, --commit-results-message CLI_TESTING__CI__END_COMMIT_MESSAGE
                                Sets the commit message to apply at the really end.
                                Configured value: 'PyFunceble - Results'

    For an in-depth usage, explanation and examples of the arguments,
    you should read the documentation at https://pyfunceble.readthedocs.io/en/dev/

    Crafted with ♥ by Nissar Chababy (@funilrys) with the help of
    https://git.io/JkUPS && https://git.io/JkUPF
