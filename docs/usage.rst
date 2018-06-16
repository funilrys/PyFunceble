Usage
=====

From a terminal
---------------

::

    usage: PyFunceble [-ad] [-a] [--cmd-before-end CMD_BEFORE_END] [-c]
                    [--autosave-minutes AUTOSAVE_MINUTES] [--clean]
                    [--commit-autosave-message COMMIT_AUTOSAVE_MESSAGE]
                    [--commit-results-message COMMIT_RESULTS_MESSAGE]
                    [-d DOMAIN] [-db] [-dbr DAYS_BETWEEN_DB_RETEST] [--debug]
                    [--directory-structure] [-f FILE] [--filter FILTER] [-ex]
                    [--help] [-h] [--http] [--iana] [-ip IP] [--less] [-n]
                    [--link LINK] [-nl] [-nu] [-nw] [-p] [--plain]
                    [--production] [-q] [--share-logs] [-s] [--split]
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
                            commiting to upstream under Travis CI.
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
                            case we encounter some errors. Installed
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

This part is unnecessary but I wanted to document it!!

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

