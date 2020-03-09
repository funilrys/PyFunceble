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

    This argument take 1 or more values.

    As example:

    ::

        $ PyFunceble -d example.org example.net

:code:`-url "something"` | :code:`--url "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""

    Test one or more full URL, separated by spaces.

.. note::
    When we test the availability of a URL, we (only) check the HTTP status code of the given URL.

.. note::
    This argument take 1 or more values.

    As example:

    ::

        $ PyFunceble -u https://example.org https://example.com

:code:`-f "something"` | :code:`--file "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""

    Read a local or remote (RAW link) file and test all domains inside it.
    If remote (RAW link) file is given, PyFunceble will download it,
    and test the content of the given RAW link as if it was a locally stored file.

.. note::
   The system understand the following format:

    - plain list of subjects.
    - hosts file format.

:code:`-uf "something"` | :code:`--url-file "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Read a local or remote (RAW link) file and test all (full) URLs inside it.
    If remote (RAW link) file is given, PyFunceble will download it,
    and test the content of the given RAW link as if it was a locally stored file.

.. note::
    We consider one line as one URL to test.

.. note::
    This argument test if a URL which is inside the given file is available.
    It ONLY test full URLs.

    As example:

    ::

        $ PyFunceble -uf `https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.travis/lists/url`

    will download the given URL and test for it's content assuming that each line represent a URL to test.

.. warning::
    A test with this argument consist of the comparison of the status code.
    No WHOIS record will be request nor DNS Lookup will be done.

Source filtering, decoding, conversion and expansion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:code:`-ad` | :code:`--adblock`
"""""""""""""""""""""""""""""""

    Switch the decoding of the adblock format.

    **Default value:** :code:`False`

If this argument is activated the system will extract all domains or IP from the given adblock file.

:code:`--complements`
"""""""""""""""""""""

    Switch the value of the generation and test of the complements.
    A complement is for example :code:`example.org` if :code:`www.example.org` is given and vice-versa.

    **Default value:** :code:`False`

:code:`--filter "something"`
""""""""""""""""""""""""""""

    Domain to filter (regex).

Want to test all :code:`blogspot` from your list? This argument allows you to do that!

.. note::
    This argument should be a regex expression.

:code:`--idna`
""""""""""""""

    Switch the value of the IDNA conversion.

    **Default value:** :code:`False`

This argument allows the conversion of the domains using `domain2idna`_

.. _domain2idna: https://github.com/PyFunceble/domain2idna

:code:`--mining`
""""""""""""""""

    Switch the value of the mining subsystem usage.

    **Default value:** :code:`False`

Want to find domain or URL linked to a domain in your list? This argument will exactly do that.

Test control
^^^^^^^^^^^^

:code:`-c` | :code:`--auto-continue` | :code:`--continue`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Switch the value of the auto continue mode.

    **Default value:** :code:`True`

This argument activates or deactivates the auto-continue subsystem.
Indeed, as we can automatically continue if the script has been stopped,
this switch allows us to disable or enable the usage of that specific subsystem.

:code:`--cooldown-time`
"""""""""""""""""""""""

    Switch the value of the cooldown time to apply between each test.

    **Default value:** :code:`None`

This argument apply a number of seconds to sleep before/between each test.

:code:`--http`
""""""""""""""

    Switch the value of the usage of HTTP code.

    **Default value:** :code:`True`

You don't want to take the result of the HTTP code execution in consideration? This argument allows you to disable that!

.. note::
    If activated the subsystem will bypass the HTTP status code extraction logic-representation.rst

:code:`--local`
"""""""""""""""

    Switch the value of the local network testing.

    **Default value:** :code:`False`

Want to run a test over a local or private network? This argument will disable the limitation which does not apply to private networks.

:code:`-ns` | :code:`--no-special`
""""""""""""""""""""""""""""""""""

    Switch the value of the usage of the SPECIAL rules.

    **Default value:** :code:`False`

Don't want to use/apply the SPECIAL rules - which are explaines in the source column section ? This argument disable them all.


:code:`-nw` | :code:`--no-whois`
""""""""""""""""""""""""""""""""

    Switch the value the usage of whois to test domain's status.

    **Default value:** :code:`False`

Don't want to use or take in consideration the results from :code:`whois`? This argument allows you to disable it!

:code:`--syntax`
""""""""""""""""

    Switch the value of the syntax test mode.

    **Default value:** :code:`False`

.. warning::
    This will disable all other form of test,
    will validate the syntax of a given test subject,
    and output its results in plain format into :code:`output/domains/{VALID,INVALID}/list`

:code:`-t "something"` | :code:`--timeout "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Switch the value of the timeout.

    **Default value:** :code:`5`

This argument will set the default timeout to apply everywhere it is possible to set a timeout.

:code:`--reputation`
""""""""""""""""""""

    Switch the value of the reputation test mode.

    **Default value:** :code:`False`

.. warning::
    This will disable all other form of test,
    will checks against AlienVault's reputation data
    and output its result into :code:`output/*/{MALICIOUS,SANE}/*`.

:code:`--use-reputation-data`
"""""""""""""""""""""""""""""

    Switch teh value of the reputation data usage.

    **Default value:** :code:`False`

.. warning::
    This only have an effect when used along with the availability test.

:code:`-ua "something"` | :code:`--user-agent "something"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Set the user-agent to use and set every time we interact with everything which is not the logs sharing system.

:code:`-vsc` | :code:`--verify-ssl-certificate`
"""""""""""""""""""""""""""""""""""""""""""""""

    Switch the value of the verification of the SSL/TLS certificate when testing for URL.

    **Default value:** :code:`False`

    .. warning::
        If you activate the verification of the SSL/TLS certificate, you may get **false positive** results.

        Indeed if the certificate is not registered to the CA or is simply invalid and the domain is still alive, you will always get :code:`INACTIVE` as output.


DNS (resolver) control
^^^^^^^^^^^^^^^^^^^^^^

:code:`--dns`
"""""""""""""

    Set one or more specific DNS servers to use during the test, separated by spacees.


    **Default value:** :code:`Follow OS DNS` ==> :code:`None`

.. warning::
    We expect a DNS server(s). If no DNS server(s) is given. You'll almost for certain get all
    results as :code:`INACTIVE`

    This could happens in case you use :code:`--dns -f`

.. note::
    You can specify a port number to use to the DNS server if needed.

    As example:

    ::

        - 127.0.1.53:5353

:code:`--dns-lookup-over-tcp`
"""""""""""""""""""""""""""""

    Make all DNS query through TCP instead of UDP.

    **Default value:** :code:`False`


Databases
^^^^^^^^^

:code:`-db` | :code:`--database`
""""""""""""""""""""""""""""""""

    Switch the value of the usage of a database to store inactive domains of the currently tested list.

    **Default value:** :code:`True`

This argument will disable or enable the usage of a database which saves all `INACTIVE` and `INVALID` domain of the given file over time.

.. note::
    The database is retested every x day(s), where x is the number set in :code:`-dbr "something"`.

:code:`--database-type`
"""""""""""""""""""""""

    Tell us the type of database to use.
    You can choose between the following: :code:`json`, :code:`mariadb`, :code:`mysql`.

    **Default value:** :code:`json`

This argument let us use different types of database.

.. note::
    This feature is applied to the following subsystems:

    * Autocontinue physically located (JSON) at :code:`output/continue.json`.
    * InactiveDB physically located (JSON) at :code:`[config_dir]/inactive_db.json`.
    * Mining physically located (JSON) at :code:`[config_dir]/mining.json`.
    * WhoisDB physically located (JSON) at :code:`[config_dir]/whois.json`.

:code:`-dbr "something"` | :code:`--days-between-db-retest "something"`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    Set the numbers of days between each retest of domains present into the database of `INACTIVE` and `INVALID` domains.

    **Default value:** :code:`1`

.. note::
    This argument is only used if :code:`-db` or :code:`inactive_database : true` (under :code:`.PyFunceble.yaml`) are activated.

:code:`-wdb` | :code:`--whois-database`
"""""""""""""""""""""""""""""""""""""""

    Switch the value of the usage of a database to store whois data in order to avoid whois servers rate limit.

    **Default value:** :code:`True`

Output control
^^^^^^^^^^^^^^

:code:`-a` | :code:`--all`
""""""""""""""""""""""""""

    Output all available information on the screen.

    **Default value:** :code:`False`

**When activated:**

::


    Domain                                                                                               Status      Expiration Date   Source     HTTP Code
    ---------------------------------------------------------------------------------------------------- ----------- ----------------- ---------- ----------
    pyfunceble.readthedocs.io                                                                            ACTIVE      Unknown           NSLOOKUP   302

**When deactivated:**

::

    Domain                                                                                               Status      HTTP Code
    ---------------------------------------------------------------------------------------------------- ----------- ----------
    pyfunceble.readthedocs.io                                                                            ACTIVE      302

:code:`-ex` | :code:`--execution`
"""""""""""""""""""""""""""""""""

    Switch the default value of the execution time showing.

    **Default value:** :code:`False`

Want to know the execution time of your test? Well, this argument will let you know!

:code:`--hierarchical`
""""""""""""""""""""""

    Switch the value of the hierarchical sorting of the tested file.

    **Default value:** :code:`True`

This argument will output the result listed in a hierarchical order.

:code:`-h` | :code:`--host`
"""""""""""""""""""""""""""

    Switch the value of the generation of hosts file.

    **Default value:** :code:`True`

This argument will let the system know if it has to generate the hosts file version of each status.

:code:`-ip "something"`
"""""""""""""""""""""""

    Change the IP to print with the hosts files.

    **Default value:** :code:`0.0.0.0`

:code:`--json`
""""""""""""""

    Switch the value of the generation of the JSON formatted list of domains.

    **Default value:** :code:`False`

:code:`--less`
""""""""""""""

**When activated:**

::

    Domain                                                                                               Status      HTTP Code
    ---------------------------------------------------------------------------------------------------- ----------- ----------
    pyfunceble.readthedocs.io                                                                            ACTIVE      302

**When deactivated:**

::


    Domain                                                                                               Status      Expiration Date   Source     HTTP Code
    ---------------------------------------------------------------------------------------------------- ----------- ----------------- ---------- ----------
    pyfunceble.readthedocs.io                                                                            ACTIVE      Unknown           NSLOOKUP   302

:code:`-nf` | :code:`--no-files`
""""""""""""""""""""""""""""""""

    Switch the value the production of output files.

    **Default value:** :code:`False`

Want to disable the production of the outputted files? This argument is for you!

:code:`-nl` | :code:`--no-logs`
"""""""""""""""""""""""""""""""

    Switch the value of the production of logs files in the case we encounter some errors.

    **Default value:** :code:`False`

Don't want any logs to go out of PyFunceble? This argument disables every logs subsystem.

:code:`-nu` | :code:`--no-unified`
""""""""""""""""""""""""""""""""""

    Switch the value of the production unified logs under the output directory.

    **Default value:** :code:`True`

This argument disables the generation of `result.txt`.

:code:`--percentage`
""""""""""""""""""""

    Switch the value of the percentage output mode.

    **Default value:** :code:`True`

This argument will disable or enable the generation of the percentage of each status.

:code:`--plain`
"""""""""""""""

    Switch the value of the generation of the plain list of domains.

    **Default value:** :code:`False:`

Want to get a list with all domain for each status? The activation of this argument does the work while testing!

:code:`-q` | :code:`--quiet`
""""""""""""""""""""""""""""

    Run the script in quiet mode.

    **Default value:** :code:`False`

You prefer to run a program silently? This argument is for you!

:code:`--share-logs`
""""""""""""""""""""

    Switch the value of the sharing of logs.

    **Default value:** :code:`False`

Want to make PyFunceble a better tool? Share your logs with our API which collect all logs!

:code:`-s` | :code:`--simple`
"""""""""""""""""""""""""""""

    Switch the value of the simple output mode.

    **Default value:** :code:`False`

Want as less as possible data on screen? This argument returns as less as possible on screen!

:code:`--split`
"""""""""""""""

    Switch the value of the split of the generated output

    **Default value:** :code:`True`

Want to get the logs (copy of what you see on screen) on different files? This argument is suited to you!

Multiprocessing
^^^^^^^^^^^^^^^

:code:`-m` | :code:`--multiprocess`
"""""""""""""""""""""""""""""""""""

    Switch the value of the usage of multiple process.

    **Default value:** :code:`False`

Want to speed up the test time? This argument will allow the usage of multiple processes for testing.

:code:`--multiprocess-merging-mode`
"""""""""""""""""""""""""""""""""""

    Sets the multiprocess merging mode. You can choose between the following `live|ends`.

    **Default value:** :code:`end`

.. note::
    With the :code:`end` value, the merging of cross process data is made at the very end of the current instance.

.. note::
    With the :code:`live` value, the merging of cross process data is made after the processing of the maximal number of process.

    Which means that if you allow 5 processes, we will run 5 tests, merge, run 5 tests, merge and so on until the end.

:code:`-p` | :code:`--processes`
""""""""""""""""""""""""""""""""

    Set the number of simultaneous processes to use while using multiple processes.

    **Default value:** :code:`25`

.. warning::
    DO not try to exceed your number of CPU if you want to keep your machine
    somehow alive and healthy!!


CI / CD
^^^^^^^

:code:`--autosave-minutes`
""""""""""""""""""""""""""

    Update the minimum of munutes before we start committing to upstream under the CI mode.

    **Default value:** :code:`15`

:code:`--ci`
""""""""""""

    Switch the value of the CI mode.

    **Default value:** :code:`False`

.. note::
    If you combine this argument with the :code:`--quiet` argument, the test will
    output a dotted line, were each dot (:code:`.`) represent one test result
    or an input which was skiped because it was previously tested.

Want to use PyFunceble under a supporter CI infrastructure/network? This argument is suited for your need!

:code:`--ci-branch`
"""""""""""""""""""

    Switch the branch name where we are going to push.

    **Default value:** :code:`master`

:code:`--ci-distribution-branch`
""""""""""""""""""""""""""""""""""""

    Switch the branch name where we are going to push the final results.

    **Default value:** :code:`master`

.. note::
    The difference between this and :code:`--ci-branch` is the fact
    that this branch will get the (final) result only when the test is finished
    under the given :code:`--ci-branch`.

    As example, this allow us to have 2 branches:

    - :code:`proceessing` (CI branch), for the tests with PyFunceble.
    - :code:`master` (CI distribution branch), for the distribution of the results of PyFunceble.

:code:`--cmd` "something"
"""""""""""""""""""""""""

    Pass a command before each commit (except the final one).

    **Default value:** :code:`''`

.. note::
    In this example, :code:`something` should be a script or a program which have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under :code:`.PyFunceble.yaml`) are activated.

:code:`--cmd-before-end "something"`
""""""""""""""""""""""""""""""""""""

    Pass a command before the results (final) commit under the CI mode.

    **Default value:** :code:`''`

.. note::
    In this example, :code:`something` should be a script or a program which have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under :code:`.PyFunceble.yaml`) are activated.

:code:`--commit-autosave-message "something"`
"""""""""""""""""""""""""""""""""""""""""""""

    Replace the default autosave commit message.

    **Default value:** :code:`PyFunceble - AutoSave`

This argument allows us to set a custom commit message which is going to be used as commit message when saving.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we have to split the work into multiple processes because a list is too long or the timeout is reached.

.. warning::
    Please avoid the usage of :code:`[ci skip]` here.

:code:`--commit-results-message "something"`
""""""""""""""""""""""""""""""""""""""""""""

    Replace the default results (final) commit message.

    **Default value:** :code:`PyFunceble - Results`

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we reached the end of the list we are or have to test.


Unique actions
^^^^^^^^^^^^^^

:code:`--clean`
"""""""""""""""

    Clean all files under the output directory.

As it is sometimes needed to clean our :code:`output/` directory, this argument does the job automatically.

.. warning::
    This argument delete everything which are :code:`.keep` or :code:`.gitignore`

:code:`--clean-all`
"""""""""""""""""""

    Clean all files under the output directory along with all file generated by PyFunceble.

.. warning::
    This really deletes almost everything we generated without any warning.

.. note::
    We don't delete the whois database file/table because they are (almost) static data which
    are shared accross launches in your environment.

.. warning::
    If you plan to clean manually do not delete the whois database file or table as it will
    make your test finish under a much longer time as usual for you.

.. warning::
    If you don't combine this argument alongside with the :code:`--database-type` argument or its configurable equivalent,
    this argument will only clean the JSON formatted databases.

:code:`--directory-structure`
"""""""""""""""""""""""""""""

    Generate the directory and files that are needed and which does not exist in the current directory.

Want to start without anything? This argument generates the output directory automatically for you!

.. note::
    In case of a file or directory not found issue, it's recommended to remove the :code:`dir_structure.json` along with the `output/` directory before using this argument.

Global overview
^^^^^^^^^^^^^^^

::

    usage: PyFunceble [-d DOMAIN [DOMAIN ...]] [-u URL [URL ...]] [-f FILE]
                    [-uf URL_FILE] [-ad] [--complements] [--filter FILTER]
                    [--idna] [--mining] [-c] [--cooldown-time COOLDOWN_TIME]
                    [--http] [--local] [-ns] [-nw] [--syntax] [-t TIMEOUT]
                    [--reputation] [--use-reputation-data] [-ua USER_AGENT]
                    [-vsc] [--dns DNS [DNS ...]] [--dns-lookup-over-tcp] [-db]
                    [--database-type DATABASE_TYPE]
                    [-dbr DAYS_BETWEEN_DB_RETEST] [-wdb] [-a] [-ex]
                    [--hierarchical] [-h] [-ip IP] [--json] [--less] [-nf] [-nl]
                    [-nu] [--percentage] [--plain] [-q] [--share-logs] [-s]
                    [--split] [-m]
                    [--multiprocess-merging-mode MULTIPROCESS_MERGING_MODE]
                    [-p PROCESSES] [--autosave-minutes AUTOSAVE_MINUTES] [--ci]
                    [--ci-branch CI_BRANCH]
                    [--ci-distribution-branch CI_DISTRIBUTION_BRANCH]
                    [--cmd CMD] [--cmd-before-end CMD_BEFORE_END]
                    [--commit-autosave-message COMMIT_AUTOSAVE_MESSAGE]
                    [--commit-results-message COMMIT_RESULTS_MESSAGE] [--clean]
                    [--clean-all] [--directory-structure] [--help] [-v]

    PyFunceble - The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

    optional arguments:
        --help                Show this help message and exit.
        -v, --version         Show the version of PyFunceble and exit.

    Source:
        -d DOMAIN [DOMAIN ...], --domain DOMAIN [DOMAIN ...]
                                Test one or more domains, separated by spaces.
        -u URL [URL ...], --url URL [URL ...]
                                Test one or more full URL, separated by spaces.
        -f FILE, --file FILE  Read a local or remote (RAW link) file and test all domains inside it.
                                If remote (RAW link) file is given, PyFunceble will download it, and test the content of the given RAW link as if it was a locally stored file.
        -uf URL_FILE, --url-file URL_FILE
                                Read a local or remote (RAW link) file and test all (full) URLs inside it.
                                If remote (RAW link) file is given, PyFunceble will download it, and test the content of the given RAW link as if it was a locally stored file.

                                This argument test if an URL is available. It ONLY test full URLs.

    Source filtering, decoding, conversion and expansion:
        -ad, --adblock        Switch the decoding of the adblock format.
                                Configured value: False
        --complements         Switch the value of the generation and test of the complements.
                                A complement is for example `example.org` if `www.example.org` is given and vice-versa.
                                Configured value: False
        --filter FILTER       Domain to filter (regex).
        --idna                Switch the value of the IDNA conversion.
                                Configured value: False
        --mining              Switch the value of the mining subsystem usage.
                                Configured value: False

    Test control:
        -c, --auto-continue, --continue
                                Switch the value of the auto continue mode.
                                Configured value: True
        --cooldown-time COOLDOWN_TIME
                                Switch the value of the cooldown time to apply between each test.
                                Configured value: None
        --http                Switch the value of the usage of HTTP code.
                                Configured value: True
        --local               Switch the value of the local network testing.
                                Configured value: True
        -ns, --no-special     Switch the value of the usage of the SPECIAL rules.
                                Configured value: False
        -nw, --no-whois       Switch the value the usage of whois to test domain's status.
                                Configured value: False
        --syntax              Switch the value of the syntax test mode.
                                Configured value: False
        -t TIMEOUT, --timeout TIMEOUT
                                Switch the value of the timeout.
                                Configured value: 5
        --reputation          Switch the value of the reputation test mode.
                                Configured value: False
        --use-reputation-data
                                Switch the value of the reputation data usage.
                                Configured value: False
        -ua USER_AGENT, --user-agent USER_AGENT
                                Set the user-agent to use and set every time we interact with everything which is not the logs sharing system.
        -vsc, --verify-ssl-certificate
                                Switch the value of the verification of the SSL/TLS certificate when testing for URL.
                                Configured value: False

    DNS (resolver) control:
        --dns DNS [DNS ...]   Set one or more specific DNS servers to use during the test, separated by spaces.

                                You can give the port along with the DNS server if needed. But, if omitted, the default port (53) will be used.
                                Configured value: OS (declared) DNS server
        --dns-lookup-over-tcp
                                Make all DNS query with TCP.
                                Configured value: False

    Databases:
        -db, --database       Switch the value of the usage of a database to store inactive domains of the currently tested list.
                                Configured value: True
        --database-type DATABASE_TYPE
                                Tell us the type of database to use.
                                You can choose between the following: `json | mariadb | mysql`
                                Configured value: 'json'
        -dbr DAYS_BETWEEN_DB_RETEST, --days-between-db-retest DAYS_BETWEEN_DB_RETEST
                                Set the numbers of days between each retest of domains present into inactive-db.json.
                                Configured value: 1
        -wdb, --whois-database
                                Switch the value of the usage of a database to store whois data in order to avoid whois servers rate limit.
                                Configured value: True

    Output control:
        -a, --all             Output all available information on the screen.
                                Configured value: True
        -ex, --execution      Switch the default value of the execution time showing.
                                Configured value: False
        --hierarchical        Switch the value of the hierarchical sorting of the tested file.
                                Configured value: False
        -h, --host            Switch the value of the generation of hosts file.
                                Configured value: True
        -ip IP                Change the IP to print in the hosts files with the given one.
                                Configured value: '0.0.0.0'
        --json                Switch the value of the generation of the JSON formatted list of domains.
                                Configured value: False
        --less                Output less informations on screen.
                                Configured value: False
        -nf, --no-files       Switch the value of the production of output files.
                                Configured value: False
        -nl, --no-logs        Switch the value of the production of logs files in the case we encounter some errors.
                                Configured value: False
        -nu, --no-unified     Switch the value of the production unified logs under the output directory.
                                Configured value: False
        --percentage          Switch the value of the percentage output mode.
                                Configured value: True
        --plain               Switch the value of the generation of the plain list of domains.
                                Configured value: False
        -q, --quiet           Run the script in quiet mode.
                                Configured value: False
        --share-logs          Switch the value of the sharing of logs.
                                Configured value: False
        -s, --simple          Switch the value of the simple output mode.
                                Configured value: False
        --split               Switch the value of the split of the generated output files.
                                Configured value: True

    Multiprocessing:
        -m, --multiprocess    Switch the value of the usage of multiple process.
                                Configured value: False
        --multiprocess-merging-mode MULTIPROCESS_MERGING_MODE
                                Sets the multiprocess merging mode.
                                You can choose between the following: `live|ends`.
                                Configured value: 'end'
        -p PROCESSES, --processes PROCESSES
                                Set the number of simultaneous processes to use while using multiple processes.
                                Configured value: 25

    CI / CD:
        --autosave-minutes AUTOSAVE_MINUTES
                                Update the minimum of minutes before we start committing to upstream under the CI mode.
                                Configured value: 15
        --ci                  Switch the value of the CI mode.
                                Configured value: False
        --ci-branch CI_BRANCH
                                Switch the branch name where we are going to push.
                                Configured value: 'master'
        --ci-distribution-branch CI_DISTRIBUTION_BRANCH
                                Switch the branch name where we are going to push the final results.
                                Configured value: 'master'
        --cmd CMD             Pass a command to run before each commit (except the final one) under the CI mode.
                                Configured value: ''
        --cmd-before-end CMD_BEFORE_END
                                Pass a command to run before the results (final) commit under the CI mode.
                                Configured value: ''
        --commit-autosave-message COMMIT_AUTOSAVE_MESSAGE
                                Replace the default autosave commit message.
                                Configured value: None
        --commit-results-message COMMIT_RESULTS_MESSAGE
                                Replace the default results (final) commit message.
                                Configured value: None

    Unique actions:
        --clean               Clean all files under the output directory.
        --clean-all           Clean all files under the output directory along with all file generated by PyFunceble.
        --directory-structure
                                Generate the directory and files that are needed and which does not exist in the current directory.

    For an in depth usage, examplation and examples of the arguments, you should read the documentation at https://pyfunceble.readthedocs.io//en/dev/

    Crafted with ♥ by Nissar Chababy (@funilrys) with the help of https://pyfunceble.github.io/contributors.html && https://pyfunceble.github.io/special-thanks.html
