# `cli_testing`

This is where you can configure everything related to the testing through the CLI.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
cli_testing:
  # Provides everything directly related to the testing through the CLI.

  # Set the IP to prefix each hosts file lines with.
  #
  # CLI Argument: -ip | --hosts-ip
  hosts_ip: "0.0.0.0"

  # Set the amount of maximal workers to use to perform tests.
  #
  # NOTE:
  #     If set to `null`, the value is implicitly CPU * Cores - 2
  #
  # CLI Argument: -w | --max-workers
  max_workers: null

  # Enable/Disable the autocontinue datasets.
  #
  # The autocontinue datasets/database is a database that temporarily store the
  # result of the tested subject in the hope to continue as soon as possible
  # after a break or shortage.
  #
  # CLI Argument: -c | --auto-continue | --continue
  autocontinue: no

  # Enable/Disable the inactive datasets.
  #
  # The inactive datasets/database is used to store the INACTIVE and INVALID
  # subjects to purposely retest then at a later time.
  #
  # This mechanism let you cleanup your source file while being sure that
  # pyfunceble will retest the old entries of your source file. After retesting,
  # pyfunceble will throw the newly ACTIVE subject from the database and put
  # it into your ACTIVE output files so that you can reintroduce them into
  # your list.
  #
  # CLI Argument:  --inactive-db
  inactive_db: yes

  # Enable/Disable the whois storage of whois records.
  #
  # This mechanism let us avoid spaming the WHOIS servers by storing the
  # expiration dates from the whois record into a local datasets/database.
  # Later on, PyFunceble will query the local database first.
  #
  # CLI Argument: -wdb | --whois-database
  whois_db: yes

  # Enable/Disable the testing and generation of complements.
  #
  # A complement is `www.example.org` when `example.org` is given and vice-versa.
  #
  # CLI Argument: --complements
  complements: no

  # Enable/Disable the expension and testing of single addresses of a CIDR.
  #
  # CLI Argument: --cidr
  cidr_expand: no

  # Set the cooldown time to apply between each tests.
  #
  # This is essential to avoid spaming remote resources - especially WHOIS servers.
  #
  # WARNING:
  #     This must be a value >= 0.0
  #
  # CLI Argument: --cooldown-time
  cooldown_time: 0.0

  # Sets the Database Connector type to use.
  # Available: csv | mariadb | mysql | postgresql
  #
  # Set the type of database to use or generate to store long term information-s.
  #
  # When set to `mariadb`, `mysql` or `postgesql` the following environment
  # variables are required.
  #
  #     PYFUNCEBLE_DB_HOST - The host or unix socket path of the database server.
  #     PYFUNCEBLE_DB_PORT - The port to use to reach the database server.
  #     PYFUNCEBLE_DB_USERNAME - The username to use to connect to the database server - when applicable.
  #     PYFUNCEBLE_DB_PASSWORD - The password to use to connect to the database server - when applicable.
  #     PYFUNCEBLE_DB_NAME - The name of the database to work with.
  #     PYFUNCEBLE_DB_CHARSET - The charset to use - when applicable.
  #
  # Available Values: csv | mariadb | mysql | postgresql
  #
  # CLI Argument: --database-type
  db_type: csv

  # Set the filter to apply while reading inputs.
  #
  # In other words, a global filter to apply to select the subject to tests.
  # Meaning that if you give `\.info$` (for example), we will only test the
  # subjects that ends with `.info`.
  #
  # CLI Argument: --filter
  file_filter: null

  # Enable/Disable the mining of subjects.
  #
  # When enabled, PyFunceble will follow the HTTP redirects and put all redirected
  # subjects into the testing queue and outputs.
  #
  # CLI Argument: --mining
  mining: no

  # Acknowledge/Dismiss that we are testing for subjects that are only on the
  # local network.
  #
  # NOTE:
  #     When enabled, no syntax checking will be processed when performing
  #     availability and reputation tests.
  #
  # CLI Argument: --local
  local_network: no

  # Enable/Disable the preloading of the given input file(s).
  #
  # When enabled, we take the time to pre-load subjects by decoding inputs files
  # and storing the informatino in the chosen datasets/database format.
  # The hope is to optimise some of our process by only focusing on testing.
  #
  # WARNING:
  #     While this is helpful for long running tasks, this might not be a good
  #     idea if you are testing a URL directly. This process is not optimizied
  #     for sources that are constantly updated (checksums).
  #
  # CLI Argument: --preload
  preload_file: no

  # Enable/Disable a chancy testing mode that unleashes and bypass the safety
  # workflow-s in place in hope of speed.
  #
  # DANGER / WARNING:
  #     You have been warned. This mode is for the chancy and lucky one.
  #
  #     You shouldn't use this unless you fele really, really, really lucky and
  #     trust your machine.
  #
  #     Enabling this mode makes thinks look 'fast', but it may produce some
  #     rather ... unexpected behavior and results - IF N+1 process simultaneously
  #     write the same output file.
  #
  #     This mode also makes the CLI terminal output unparsable - either.
  #
  #     **MAY THE FORCE BE WITH YOU!**
  #
  # CLI Argument: --chancy
  chancy_tester: no

  ci:
    # Provides everything related to the testing within a Continuous integration
    # engine.

    # Enable/Disable the CI/CD mode.
    #
    # When enabled, PyFunceble will assume that it works with a git repository.
    # Therefore, you have to declare the following environment variables to
    # configure git for pushing - which is normally not available withing a
    # CI engine.
    #
    #       GIT_NAME - The `git.name` to setup and use.
    #       GIT_EMAIL - The `git.email` to setup and use.
    #       GIT_BRANCH - (optional) - The git branch to use to distribute results betwen sessions.
    #       GIT_DISTRIBUTION_BRANCH - (optional) - The git branch to use to distribute the final results.
    #       GITHUB_TOKEN - The token to use to authenticate ourselves against GitHub. Read when under a GitHub Action or Jenkins CI worker.
    #       GL_TOKEN - The token to use to authenticate ourselves againt GitLab. Read when under a GitLab Runner.
    #       GH_TOKEN - The token to ue to authenticate ourselves against GitHub. Read when under a Travis CI instance.
    #
    # CLI Argument: --ci
    active: no

    # Set the commit message to apply to all results commit except the final one.
    #
    # CLI Argument: --ci-commit-message
    commit_message: "PyFunceble - AutoSave"

    # Set the commit message to apply to the very last and final result commit.
    #
    # CLI Argument: --ci-end-commit-message
    end_commit_message: "PyFunceble - Results"

    # Set the number of minutes to wait before to start saving and stopping a session.
    #
    # This parameter can be understood as the running time of PyFunceble under a
    # CI Engine.
    #
    # CLI Argument: --ci-max-minutes
    max_exec_minutes: 15

    # Set the branch to use to distribute results between multiple CI/CD sessions.
    #
    # Environment Variable: GIT_BRANCH
    # CLI Argument: --ci-branch
    branch: master

    # Set the branch to use to distribute the final results of multiple CI/CD session.
    #
    # Environment Variable: GIT_DISTRIBUTION_BRANCH
    # CLI Argument: --ci-distribution-branch
    distribution_branch: master

    # Set the command to execute before each (except last) result commit.
    #
    # CLI Argument: --ci-command
    command: null

    # Set the command to execute before the very last result commit.
    #
    # CLI Argument: --ci-end-command
    end_command: null

  display_mode:
    # Provides everything related to the display/OUTPUT of PyFunceble.

    # Enable/Disable the printing of dots.
    #
    # Dots !? Why Dots ? WTH ?!
    #   Yes, you read correctly dots. Those dots are crutial under CI/CD engines
    #   that assumes that no-output within a few minutes is an error. To avoid
    #   such situation when the CI/CD engines just kill the job, we print dots,
    #   when we perform some tasks that may not output anything for a few minutes.
    #
    #   An example is when you are on the second session of testing and PyFunceble
    #   is going through the list of subjects but it sees that the subject has been
    #   already tested.
    #
    # NOTE:
    #   This argument is automatically switched to `yes` when under a CI/CD engine
    #   (aka cli_testing.ci set to yes).
    #
    # CLI Argument: --dots
    dots: no

    # Enable/Disable the printing of the execution time at the end of a test session.
    #
    # CLI Argument: -ex | --execution
    execution_time: no

    # Enable/Disable the printing of the percentage stats per status at the end
    # of a test session.
    #
    # CLI Argument: --percentage
    percentage: yes

    # Enable/Disable the printing of the registrar stats per subjects at the end
    # of a test session.
    #
    # CLI Argument: --registrar
    registrar: no

    # Enable/Disable the printing of any outputs.
    #
    # CLI Argument: -q | --quiet
    quiet: no

    # Enable/Disable the printing of minimal tabular information when testing.
    less: yes

    # Enable/Disable the printing of most tabular information when testing.
    #
    # CLI Argument: -a | --all
    all: no

    # Enable/Disable the printing of an extreme simple and minimalistic information
    # when testing.
    #
    # CLI Argument: -s | --simple
    simple: no

    # Enable/Disable the printing of colored tabular information.
    #
    # CLI Argument: --colour | --color
    colour: yes

    # Set the status to display to STDOUT.
    #
    # WARNING:
    #   When this parameter is not set to `ALL`, only the subjects matching the
    #   selected status will be printed to STDOUT. Howerver, this doesn't have
    #   any effect on the generated files.
    #
    # CLI Argument: --display-status
    status: all

    # Set the maximal number of registrar to display when we have to print the
    # registrar stats per subject.
    #
    # NOTE:
    #   This doesn't have any effect on the generated files.
    #
    # CLI Argument: --max-registrar
    max_registrar: 15

  testing_mode:
    # Provides and select the testing mode.
    #
    # NOTE:
    #   Only one can be active at a time.

    # Enable/Disable the availability test mode.
    availability: yes

    # Enable/Disable the syntax test mode.
    #
    # CLI Argument: --syntax
    syntax: no

    # Enable/Disable the reputation test mode.
    #
    # CLI Argument: --reputation
    reputation: no

  days_between:
    # Provides everything which is x days periodic.

    # NOT IMPLEMENTED (Anticipation for future usage).
    db_clean: 28

    # Set the minimal number of days between the retest of subject which were
    # stored into the inactive datasets/database.
    #
    # CLI Argument: -dbr | --days-between-db-retest
    db_retest: 1

  sorting_mode:
    # Provides everything related to the output sorting.
    #
    # NOTE:
    #   Only one can be active at a time.
    #
    # WARNING:
    #   The parameters below only applies to the generated files. NOT STDOUT.

    # Enable/Disable the hierarchical sorting.
    #
    # CLI Argument: --hierarchical
    hierarchical: no

    # Enable/Disable the standard sorting.
    standard: yes

  file_generation:
    # Provides everything related to the generation of files.

    # Enable/Disable the generation of files.
    #
    # CLI Argument: --no-files
    no_file: no

    # Enable/Disable the generation of hosts formatted files.
    #
    # CLI Argument: -h | --hosts
    hosts: no

    # Enable/Disable the generation of plain/raw formatted files.
    #
    # CLI Argument: --plain
    plain: yes

    # Enable/Disable the generation of analytic files.
    #
    # Analytic ?! WTH !?
    #   Yes, analytic! While PyFunceble is really good for a lot of things, sometime
    #   it takes some decision without being really sure about it or without
    #   wanting to be biased. Therefore, it generates files inside the analytic folder.
    #   The files inside the analytic folder are there for human to analyse or
    #   to invite the community to influence PyFunceble.
    #
    #   If you are sure that the behavior of PyFunceble should be adopted for sure,
    #   fill an issue and let's evolve it together :-)
    #
    analytic: yes

    # Enable/Disable the generation of unified results files.
    #
    # WARNING:
    #   This parameter simply generate a unified copy of the STDOUT instead of 1
    #   file per status.
    #
    # CLI Argument: --unified-results
    unified_results: no

    # Enable/Disable the merging of the results of all inputted files into one
    # single output directory.
    #
    # Normally, PyFunceble generated a dedicated output folder for each inputted
    # files. However, if you want the results to be merged inside a single
    # folder, just switch this parameter.
    #
    # CLI Argument: --merge-output
    merge_output_dirs: no
```
