# Coding conventions

## Format

1.  We should format our code with
    [Black](https://github.com/ambv/black), *The uncompromising Python
    code formatter*.
2.  We should write **docstrings** for every public method, function and
    class. It does not have to be elaborate. Just explain what it simply
    does!

```shell
black PyFunceble tests
```

## Linting

Our code should pass a `pylint` check without any issue (exit 0).

```shell
pylint PyFunceble && pylint tests
```

## Coverage

Our code should have at least 60% of coverage.

**Note:** Coverage unrelevant code/files can be muted.

```shell
coverage run setup.py test && coverage report -m
```

## Distribution

Our code should be shipped (before package) with a new version and a
new `version.yaml` file. That file should **ALWAYS** be generated with
the following.

**Note:** An exception is granted for detached branch (not `dev` nor `master`) and
no code changes.


```shell
# Prepare our files, :code:`version.yaml` and code for production/dev usage.
production-pyfunceble [dev|master]
```

## Commit

All your commits should be - when possible - be signed with **PGP**.
Please note the usage of `-S` into the commit command which means that
we sign the commit.

(More information can be found on [GitHub
documentation](https://github.com/blog/2144-gpg-signature-verification))

The commit message may be formatted like follow:

**Note:** An exception is granted for no code changes.

```git
Short explanation (max 79 char).

Paragraphs with some details/context (if needed).
```

## Git Hook

If one may want to automate the process.

Here is a git hook (as proposition) to be set into `.git/hooks/pre-commit`.

```shell
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
```