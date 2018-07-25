Usage
=====

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

:code:`-ip "something"`
^^^^^^^^^^^^^^^^^^^^^^^

    Change the IP to print with the hosts files.
        Default value: :code:`0.0.0.0`

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

:code:`-n` | :code:`--no-files`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Switch the value the production of output files.
        Default value: :code:`False`

Want to disable the production of the outputed files? This argument is for you!

:code:`--link "something"`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    Download and test the given file.

Want to test a raw link ? This argument will download and test the given raw link.

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

    usage: pyfunceble [-ad] [-a] [--cmd-before-end CMD_BEFORE_END] [-c]
                    [--autosave-minutes AUTOSAVE_MINUTES] [--clean]
                    [--commit-autosave-message COMMIT_AUTOSAVE_MESSAGE]
                    [--commit-results-message COMMIT_RESULTS_MESSAGE]
                    [-d DOMAIN] [-db] [-dbr DAYS_BETWEEN_DB_RETEST] [--debug]
                    [--directory-structure] [-f FILE] [--filter FILTER] [-ex]
                    [--help] [-h] [--http] [--iana] [-ip IP] [--less] [-n]
                    [--link LINK] [-nl] [-nu] [-nw] [-p] [--plain]
                    [--production] [-psl] [-q] [--share-logs] [-s] [--split]
                    [-t TIMEOUT] [--travis] [--travis-branch TRAVIS_BRANCH]
                    [-u URL] [-uf URL_FILE] [-v]

    The tool to check domain or IP availability.

    optional arguments:
    -ad, --adblock        Switch the decoding of the adblock format.
                            Installed value: False
    -a, --all             Output all available informations on screen.
                            Installed value: False
    --cmd-before-end CMD_BEFORE_END
                            Pass a command before the results (final) commit of
                            travis mode. Installed value: ''
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
                            Analyze the given domain.
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
    -f FILE, --file FILE  Test a file with a list of domains. If a URL is given
                            we download and test the content of the given URL.
    --filter FILTER       Domain to filter (regex).
    -ex, --execution      Switch the dafault value of the execution time
                            showing. Installed value: False
    --help                Show this help message and exit.
    -h, --host            Switch the value of the generation of hosts file.
                            Installed value: True
    --http                Switch the value of the usage of HTTP code.
                            Installed value: True
    --iana                Update/Generate `iana-domains-db.json`.
    -ip IP                Change the ip to print in host file.
                            Installed value: '0.0.0.0'
    --less                Output less informations on screen. Installed
                            value: True
    -n, --no-files        Switch the value the production of output files.
                            Installed value: False
    --link LINK           Download and test the given file.
    -nl, --no-logs        Switch the value of the production of logs files in
                            the case we encounter some errors. Installed
                            value: True
    -nu, --no-unified     Switch the value of the production unified logs under
                            the output directory. Installed value:
                            False
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
    --split               Switch the valur of the split of the generated output
                            files. Installed value: True
    -t TIMEOUT, --timeout TIMEOUT
                            Switch the value of the timeout. Installed
                            value: 3
    --travis              Activate the travis mode. Installed value:
                            False
    --travis-branch TRAVIS_BRANCH
                            Switch the branch name where we are going to push.
                            Installed value: 'master'
    -u URL, --url URL     Analyze the given url.
    -uf URL_FILE, --url-file URL_FILE
                            Test a file with a list of URL. If a URL is given we
                            download and test the content of the given URL.
    -ua USER_AGENT, --user-agent USER_AGENT
                            Set the user-agent to use and set everytime we
                            interact with everything which is not our logs sharing
                            system.
    -v, --version         show program's version number and exit

    Crafted with ♥ by Nissar Chababy (Funilrys) with the
    help of https://git.io/vND4m && https://git.io/vND4a

From a Python script or module
------------------------------

Before continuing reading this part, You should know that I consider that you can speak in Python. If it's not the case, well, it's the time to `learn Python`_!

As **PyFunceble** is written in Python, it can be easily imported and used inside a script. This part will represent a basic example of usage.

Basic example
"""""""""""""

::


    """
    This is a basic example which prints one of the official output of PyFunceble.

    Note:
    * Official output: ACTIVE, INACTIVE, INVALID
    """
    from PyFunceble import test as PyFunceble

    print(PyFunceble(domain='google.com'))

.. _learn Python: http://www.learnpython.org/

Loop example
""""""""""""

This part is unnecessary but we wanted to document it!!

::

    """
    This is a loop example which tests a list of domain and processes some action
        according to one of the official output of PyFunceble.

    Note:
    * Official output: ACTIVE, INACTIVE, INVALID
    * You should always use PyFunceble().test() as it's the method which is specially
        suited for `__name__ != '__main__'` usage.
    """
    from PyFunceble import test as PyFunceble

    DOMAINS = [
        'twitter.com',
        'google.com',
        'github.com',
        'github.comcomcom',
        'funilrys.co']


    def domain_status(domain_or_ip):
        """
        Check the status of the given domain name or IP.

        :param domain_or_ip: A string, the domain or IPv4 address to test.
        """
        return PyFunceble(domain_or_ip)


    for domain in DOMAINS:
        print('%s is %s' % (domain, domain_status(domain)))

From Travis CI
---------------

As we offer an argument named :code:`--travis` to activate the usage of PyFunceble in a Travis CI instance, we document here what you need to know!

Configuration
"""""""""""""

.. note::
   This part only present a commented :code:`.travis.yml` so that you can understand where to start. 
   
   If you need more practical examples, feel free to report to one of `Dead-Hosts`_ repositories which use PyFunceble with Travis CI.

.. _Dead-Hosts: https://github.com/dead-hosts


::

    env:
        global:
            # The following is your encrypted GitHub API key.
            # Indeed as we are going to push to the repository, this is needed.
            - secure: QQdKFquFFojFT9XJ1XZp4EMoDTVoXFgqZq8XU+sCVf+pJQR6d/oKBp8rnSTCnZizWOQXUjGXUUxUpSG/dYGyBLjo3rH3rsn9ciZHVfubxbwK860w4sqibl4DvhCv2rdsFtvzXnhm4P9OL3i+krKdewh9fxpNyUU58qOgfnS7mK9FcFhb8z5ak2sxU2XRZedwm6Ro0oyVKs8kFkL4YaADfNyAHlGTfr9rVmE52WXQXQENktb9gFgR2A8ZnmLy0BCMZGkPDShJnjRDWD4DErtasLmLQvWpzOBwdbVJTY6U9KDRXVNdC9lp5E5Ba/dc0y36q6vjfgJR+QchetOtHgNbKYbLB8c26Di90OZCFJsxMNcl1Wct4qFPXkFGvjXrISW6pbdPL5Plto0Ig3iLiulhYOPVArysMIk9ymtSXP+WE7VWX01LQ1fEkIoSfeVZ2caTnCmTsoHVGRRe978CojKaT7yU45kb15hcyDrzptQ8EP2hfxeh5F7KtueQ6Rsb9LFDZMkMDKflZn6a+bRhESlmWWmYB9stzGzTurQA1E1bcSACJ8A8hG5nHBzZYJ2S+OY0PE7UdyOJ0JK0qe/67d+F9ocQdIoFpDDTdgIjHerQnD2wRg1aKPzLDb4jJTpqgr5ssPrqUAKl3st7gyaAZzCEADPDnIBDjOJS+mFWbx9DKgc=
            # This is the Git name we have to set. (git config user.name)
            - GIT_NAME: Travis CI
            # This is the Git Email we have to set. (git config user.email)
            - GIT_EMAIL: dead-hosts@funilrys.com
            # This is the full slug of the repository we are working with.
            - TRAVIS_REPO_SLUG: dead-hosts/repository-structure
            # This is the branch we have to checkout and push to.
            - GIT_BRANCH: master

    # This is the language we use.
    language: python

    # This is the python version we are going to use for the tests.
    # Note: you can add any 3.x version to the list.
    python:
    - "3.6"

    # The following will tell to Travis CI to ends as fast as possible.
    matrix:
        fast_finish: true

    # Here we are setting what Travis CI have to cache.
    cache:
        # We are caching pip3 as we use it to install PyFunceble
        - pip3

    install:
        # We install the development version of PyFunceble. If you prefer the stable version replace `pyfunceble-dev` with `pyfunceble`.
        - pip3 install pyfunceble-dev

    # Our tests start here.
    script:
        # Let's say we want our results and our PyFunceble infrastructure to be saved in a directory called `PyFunceble-tests`

        # We move inside it.
        - cd PyFunceble-tests
        # We test the file `my_awesome_list` which is located inside the current directory.
        # Note: we precise the `--travis` argument here,
        #     but you work without it if you set `travis: true` inside your `.PyFunceble.yaml`
        - PyFunceble --travis -f my_awesome_list --plain

    # The following set the email notification logic.
    notifications:
        # As we want to get a mail on failure and on status change, we set the following.
        on_success:   change
        on_failure:   always

Getting a GitHub token
""""""""""""""""""""""

For the :code:`secure` index of the :code:`.travis.yml` file, you have to generate a `new GitHub token`_.

After you got your token, please write it or save it in a safe place as you're going to need it everytime you're going to interact with Travis CI.

.. note::
    The scope to set is :code:`public_repo` but you can also set others depending on your needs.

.. _new GitHub token: https://github.com/settings/tokens/new

Encrypting the token for Travis CI usage
""""""""""""""""""""""""""""""""""""""""

To encrypt the token simply replace and execute the following according to your personal case.

::

    $ travis encrypt 'GH_TOKEN=theGeneratedToken' -r 'The content of TRAVIS_REPO_SLUG' --add

.. warning::
    Please do not execute the following explicitly without replacing :code:`theGeneratedToken` with your previously generated GitHub token and :code:`The content of TRAVIS_REPO_SLUG` with your repository slug.

.. note::
    The usage of :code:`--add` ensure that the :code:`travis` program automatically add the :code:`secure` index to the :code:`.travis.yml` file.
