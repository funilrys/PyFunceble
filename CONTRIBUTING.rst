Coding conventions
==================

Format
------

1. We should format our code with `Black`_, *The uncompromising Python code formatter*.
2. We should write **docstrings** for every public method, function and class.
   It does not have to be elaborate. Just explain what it simply does!

::

    $ black PyFunceble && black tests

Linting
-------

Our code should pass a :code:`pylint` check without any issue (exit 0).

::

    $ pylint PyFunceble && pylint tests

Coverage
--------

Our code should have at least 60% of coverage.

.. note::
    Coverage unrelevant code/files can be muted.

::

    $ coverage run setup.py test && coverage report -m

Distribution
------------

Our code should be shipped (after each commit) with a new version and a new :code:`version.yaml` file.
That file should **ALWAYS** be generated with the following.

.. note::
    An exception is granted for detached branch (not :code:`dev` nor :code:`master`)
    and no code changes.

::

    $ # Prepare our files, :code:`version.yaml` and code for production/dev usage.
    $ PyFunceble --production

Commit
------

All your commits should be - when possible - be signed with **PGP**. (More information can be found on `GitHub documentation`_)
Please note the usage of :code:`-S` into the commit command which means that we sign the commit.

The commit message may be formatted like follow:

.. note::
    An exception is granted for no code changes.

::
    Short explanation (max 79 char).

    Paragraphs with some details/context (if needed).

Git Hook
--------

If one may want to automate the process.

Here is a git hook (as proposition) to be set into :code:`.git/hooks/pre-commit`.

::

    #!/usr/bin/env bash

    # We print what's going on.
    set -x
    # We stop on error.
    set -e

    # We get top level path.
    rootDirectory="$(git rev-parse --show-toplevel)"
    # We construct our list of directories.
    ourDirectories="${rootDirectory}/PyFunceble ${rootDirectory}/tests"

    if [[ ! -z "$(git status --porcelain | awk '{ if ($NF > 0 && substr($1,1,1) != "?" && $2 ~ '/\.py/' ) print $2}')" ]]
    then
            hash find
            hash isort
            hash black
            hash pylint
            hash coverage

            for directory in $(echo ${ourDirectories})
            do
                    # We sort the imports.
                    find "${directory}" -name "*.py" -exec isort {} \;
                    # We format the code.
                    black "${directory}"
                    # We lint the code.
                    pylint "${directory}"
            done

            cd "${rootDirectory}"
            coverage run setup.py test
    fi

    set +e
    set +x
    exit 0

.. _GitHub documentation: https://github.com/blog/2144-gpg-signature-verification
.. _Black: https://github.com/ambv/black