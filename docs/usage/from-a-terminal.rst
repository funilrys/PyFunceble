From a terminal
---------------

Detailed
""""""""

.. note::
    :code:`False` stand for deactivated when :code:`True` stand for activated.

:code:`-ad` | :code:`--adblock`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the decoding of the adblock format.
        Default value: :code:`False`

If this argument is activated the system will extract all domains or IP from the given adblock file.

:code:`-a` | :code:`--all`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    Output all available informations on screen.
        Default value: :code:`False`

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


:code:`--cmd-before-end "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Pass a command before the results (final) commit under the travis mode.
        Default value: :code:`''`

In this example, :code:`something` should be a script or a program which have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--travis` or :code:`travis : true`  (under :code:`.PyFunceble.yaml`) are used.

:code:`-c` | :code:`--auto-continue` | :code:`--continue`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the auto continue mode.
        Default value: :code:`True`

This argument activate or deactivated the auto-continue subsystem. 
Indeed, as we can automatically continue if the script has been stopped, this switch allows us to disable or enable the usage of that specific subsystem.

:code:`--clean`
^^^^^^^^^^^^^^^

    Clean all files under output.

As it is sometime needed to clean our :code:`output/` directory, this argument do the job automatically.

.. warning::
    This argument delete everything which are :code:`.keep` or :code:`.gitignore`


:code:`--commit-autosave-message "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Replace the default autosave commit message.
        Default value: :code:`PyFunceble - AutoSave`

This argument allow us to set a custom commit message which is going to be used as commit message when saving.

.. note::
    This argument is only used if :code:`--travis` or :code:`travis : true`  (under :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we have to split the work in multiple process because a list is too long or the timeout is reached.

.. warning::
    Please avoid the usage of :code:`[ci skip]` here.

:code:`--commit-results-message "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Replace the default results (final) commit message.
        Default value: :code:`PyFunceble - Results`

.. note::
    This argument is only used if :code:`--travis` or :code:`travis : true`  (under :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we reached the end of the list we are or have to test.

:code:`-d "something"` | :code:`--domain "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Set and test the given domain.

This argument will test and give the results of the tests of the given domain.

.. note::
    For this argument (and only for this argument9, we are converting the given string to lowercase.


:code:`-db` | :code:`--database`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the usage of a database to store inactive domains of the currently tested list.
        Default value: :code:`True`   

This argument will disable or enable the usage of a database which save all `INACTIVE` and `INVALID` domain of the given file over time.

.. note::
    The database is retested every x day(s), where x is the number set in :code:`-dbr "something"`.

:code:`-dbr "something"`
^^^^^^^^^^^^^^^^^^^^^^^^

    Set the numbers of day(s) between each retest of domains present into the database of `INACTIVE` and `INVALID` domains.
        Default value: :code:`1`

.. note::
    This argument is only used if :code:`-db` or :code:`inactive_database : true` (under :code:`.PyFunceble.yaml`) are activated.


:code:`--debug`
^^^^^^^^^^^^^^^

    Switch the value of the debug mode.
        Default value: :code:`False`

This argument activate the debug mode. Under the debug mode, everything catched by the whois subsystem is saved.

.. warning::
    Do not use this argument unless you has been told to.

:code:`--directory-structure`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Generate the directory and files that are needed and which does not exist in the current directory.

Want to start without anything ? This argument generate the output directory automatically for you!

.. note::
    In case of a file or directory not found issue, it's recommended to remove the :code:`dir_structure.json` along with the `output/` directory before using this argument.

:code:`-ex` | :code:`--execution`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the dafault value of the execution time showing.
        Default value: :code:`False`

Want to know the execution time of your test ? Well, this argument will let you know!

:code:`-f "something"` | :code:`--file "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Read the given file and test all domains inside it. If a URL is given we download and test the content of the given URL.

.. note::
    We consider one line as one domain or one commented line. Line can be commented at the end.

.. note::
    You can give a raw link and the system will download and test its content.


:code:`--filter "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Domain to filter (regex).

Want to test all :code:`blogspot` from your list ? This argument allow you to do that!

.. note::
    This argument should be a regex expression.

:code:`--help`
^^^^^^^^^^^^^^

    Show the help message and exit.

:code:`-h` | :code:`--host`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the generation of hosts file.
        Default value: :code:`True`

This argument will let the system know if it have to generate the hosts file version of each status.

:code:`--hierarchical`
^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the hierarchical sorting of tested file.
        Default value: :code:`True`

This argument will let the system know if we have to sort the list and our output in hierarchical order.


:code:`--http`
^^^^^^^^^^^^^^

    Switch the value of the usage of HTTP code.
        Default value: :code:`True`

You don't want to take the result of the HTTP code execution in consideration ? This argument allows you to disable that!

.. note:.
    If activated the subsystem will bypass the HTTP status code extraction logic-representation.rst

:code:`--iana`
^^^^^^^^^^^^^^

    Update/Generate `iana-domains-db.json`.

This argument generate or update `iana-domains-db.json`.

:code:`--idna`
^^^^^^^^^^^^^^

    Switch the value of the IDNA conversion.
        Default value: :code:`False`

This argument allow the conversion of the domains using `domain2idna`_

.. warning::
    This feature is not supported yet for the URL testing.

.. _domain2idna: https://github.com/funilrys/domain2idna

:code:`-ip "something"`
^^^^^^^^^^^^^^^^^^^^^^^

    Change the IP to print with the hosts files.
        Default value: :code:`0.0.0.0`

:code:`--json`
^^^^^^^^^^^^^^

    Switch the value of the generation of the json list of domain.
        Default value: :code:`False`

:code:`--less`
^^^^^^^^^^^^^^

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

:code:`--local`
^^^^^^^^^^^^^^^

    Switch the value of the local network testing.
        Default value: :code:`False`

Want to run a test over a local or private network ? This argument will disable the limitation which do not apply to private networks.

:code:`--link "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    Download and test the given file.

Want to test a raw link ? This argument will download and test the given raw link.

:code:`-m` | :code:`--mining`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the mining subsystem usage.
        Default value: :code:`False`

Want to find domain or URL linked to a domain in your list ? This argument will exactly do that.

:code:`-n` | :code:`--no-files`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value the production of output files.
        Default value: :code:`False`

Want to disable the production of the outputed files? This argument is for you!

:code:`-nl` | :code:`--no-logs`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the production of logs files in the case we encounter some errors.
        Default value: :code:`False`

Don't want any logs to go out of PyFunceble ? This arguments disable every logs subsystems.

:code:`-nu` | :code:`--no-unified`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the production unified logs under the output directory.
        Default value: :code:`True`

This argument disable the generation of `result.txt`.

:code:`-nw` | :code:`--no-whois`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value the usage of whois to test domain's status.
        Default value: :code:`False`

Don't want to use or take in consideration the results from :code:`whois` ? This argument allows you to disable it!

:code:`-p` | :code:`--percentage`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the percentage output mode.
        Default value: :code:`True`

This argument will disable or enable the generation of the percentage of each status.

:code:`--plain`
^^^^^^^^^^^^^^^

    Switch the value of the generation of the plain list of domain.
        Default value: :code:`False:`

Want to get a list with all domain for each status ? The activation of this argument do the work while testing!

:code:`--production`
^^^^^^^^^^^^^^^^^^^^

    Prepare the repository for production.

.. warning::
    Do not use this argument unless you has been told to, you prepare a Pull Request or you want to distribute your modified version of PyFunceble.

:code:`-psl` | :code:`--public-suffix`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Update/Generate `public-suffix.json`.

This argument will generate or update `public-suffix.json`.

:code:`-q` | :code:`--quiet`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Run the script in quiet mode.
        Default value: :code:`False`

You prefer to run a program silently ? This argument is for you!

:code:`--share-logs`

    Switch the value of the sharing of logs.
        Default value: :code:`True`

Want to make PyFunceble a better tool? Share your logs with our API which collect all logs!

:code:`-s` | :code:`--simple`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the simple output mode.
        Default value: :code:`False`

Want as less as possible data on screen ? This argument return as less informations as possible on screen!

:code:`--split`
^^^^^^^^^^^^^^^
    
    Switch the value of the split of the generated output
        Default value: :code:`True`

Want to get the logs (copy of what you see on screen) on different files? This argument is suited for you!

:code:`-t "something"` | :code:`--timeout "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value of the timeout.
        Default value: :code:`3`
    
This argument will set the default timeout to apply everywhere it is possible to set a timeout.

:code:`--travis`
^^^^^^^^^^^^^^^^

    Switch the value of the travis mode.
        Defautl value: :code:`False`

Want to use PyFunceble under Travis CI? This argument is suited for your need!

:code:`-url "something"` | :code:`--url "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Analyze the given URL.

Want to test the availability or an URL ? Enjoy this argument!

.. note::
    When we test the availability of an URL, we check the HTTP status code of the given URL.

:code:`-uf "something"` | :code:`--url-file "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Read and test the list of URL of the given file.  If a URL is given we download and test the content of the given URL.

.. note::
    We consider one line as one URL to test.

.. note::
    You can give a raw link and the system will download and test its content.

:code:`-ua "something"` | :code:`--user-agent "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Set the user-agent to use and set everytime we interact with everything which is not our logs sharing system.

:code:`-v` | :code:`--version`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Show the version of PyFunceble and exit.


Global overview
"""""""""""""""

::

    usage: PyFunceble [-ad] [-a] [--cmd-before-end CMD_BEFORE_END] [-c]
                  [--autosave-minutes AUTOSAVE_MINUTES] [--clean]
                  [--commit-autosave-message COMMIT_AUTOSAVE_MESSAGE]
                  [--commit-results-message COMMIT_RESULTS_MESSAGE]
                  [-d DOMAIN] [-db] [-dbr DAYS_BETWEEN_DB_RETEST] [--debug]
                  [--directory-structure] [-ex] [-f FILE] [--filter FILTER]
                  [--help] [--hierarchical] [-h] [--http] [--iana] [--idna]
                  [-ip IP] [--json] [--less] [--local] [--link LINK] [-m] [-n]
                  [-nl] [-nu] [-nw] [-p] [--plain] [--production] [-psl] [-q]
                  [--share-logs] [-s] [--split] [-t TIMEOUT] [--travis]
                  [--travis-branch TRAVIS_BRANCH] [-u URL] [-uf URL_FILE]
                  [-ua USER_AGENT] [-v]

    The tool to check domain or IP availability.

    optional arguments:
        -ad, --adblock        Switch the decoding of the adblock format.
                                Installed value: False
        -a, --all             Output all available informations on screen.
                                Installed value: True
        --cmd-before-end CMD_BEFORE_END
                                Pass a command before the results (final) commit under
                                the travis mode. Installed value: ''
        -c, --auto-continue, --continue
                                Switch the value of the auto continue mode.
                                Installed value: True
        --autosave-minutes AUTOSAVE_MINUTES
                                Update the minimum of minutes before we start
                                committing to upstream under Travis CI.
                                Installed value: 15
        --clean               Clean all files under output.
        --commit-autosave-message COMMIT_AUTOSAVE_MESSAGE
                                Replace the default autosave commit message.
                                Installed value: 'PyFunceble -
                                AutoSave'
        --commit-results-message COMMIT_RESULTS_MESSAGE
                                Replace the default results (final) commit message.
                                Installed value: 'PyFunceble -
                                Results'
        -d DOMAIN, --domain DOMAIN
                                Set and test the given domain.
        -db, --database       Switch the value of the usage of a database to store
                                inactive domains of the currently tested list.
                                Installed value: True
        -dbr DAYS_BETWEEN_DB_RETEST, --days-between-db-retest DAYS_BETWEEN_DB_RETEST
                                Set the numbers of day(s) between each retest of
                                domains present into inactive-db.json.
                                Installed value: 1
        --debug               Switch the value of the debug mode. Installed
                                value: False
        --directory-structure
                                Generate the directory and files that are needed and
                                which does not exist in the current directory.
        -ex, --execution      Switch the dafault value of the execution time
                                showing. Installed value: False
        -f FILE, --file FILE  Read the given file and test all domains inside it. If
                                a URL is given we download and test the content of the
                                given URL.
        --filter FILTER       Domain to filter (regex).
        --help                Show this help message and exit.
        --hierarchical        Switch the value of the hierarchical sorting of tested
                                file. Installed value: True
        -h, --host            Switch the value of the generation of hosts file.
                                Installed value: True
        --http                Switch the value of the usage of HTTP code.
                                Installed value: True
        --iana                Update/Generate `iana-domains-db.json`.
        --idna                Switch the value of the IDNA conversion.
                                Installed value: False
        -ip IP                Change the ip to print in the hosts files.
                                Installed value: '0.0.0.0'
        --json                Switch the value of the generation of the json list of
                                domain. Installed value: False
        --less                Output less informations on screen. Installed
                                value: False
        --local               Switch the value of the local network testing.
                                Installed value: True
        --link LINK           Download and test the given file.
        -m, --mining          Switch the value of the mining subsystem usage.
                                Installed value: False
        -n, --no-files        Switch the value the production of output files.
                                Installed value: False
        -nl, --no-logs        Switch the value of the production of logs files in
                                the case we encounter some errors. Installed
                                value: False
        -nu, --no-unified     Switch the value of the production unified logs under
                                the output directory. Installed value:
                                True
        -nw, --no-whois       Switch the value the usage of whois to test domain's
                                status. Installed value: False
        -p, --percentage      Switch the value of the percentage output mode.
                                Installed value: True
        --plain               Switch the value of the generation of the plain list
                                of domain. Installed value: False
        --production          Prepare the repository for production.
        -psl, --public-suffix
                                Update/Generate `public-suffix.json`.
        -q, --quiet           Run the script in quiet mode. Installed
                                value: False
        --share-logs          Switch the value of the sharing of logs.
                                Installed value: True
        -s, --simple          Switch the value of the simple output mode.
                                Installed value: False
        --split               Switch the value of the split of the generated output
                                files. Installed value: True
        -t TIMEOUT, --timeout TIMEOUT
                                Switch the value of the timeout. Installed
                                value: 3
        --travis              Switch the value of the travis mode.
                                Installed value: False
        --travis-branch TRAVIS_BRANCH
                                Switch the branch name where we are going to push.
                                Installed value: 'master'
        -u URL, --url URL     Analyze the given URL.
        -uf URL_FILE, --url-file URL_FILE
                                Read and test the list of URL of the given file. If a
                                URL is given we download and test the content of the
                                given URL.
        -ua USER_AGENT, --user-agent USER_AGENT
                                Set the user-agent to use and set everytime we
                                interact with everything which is not our logs sharing
                                system.
        -v, --version         Show the version of PyFunceble and exit.

    Crafted with ♥ by Nissar Chababy (Funilrys) with the
    help of https://pyfunceble.rtfd.io/en/dev/contributors.html &&
    https://pyfunceble.rtfd.io/en/dev/special-thanks.html
