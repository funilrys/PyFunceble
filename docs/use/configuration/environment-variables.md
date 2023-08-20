# Environment Variables

PyFunceble provides some environment variables to control some of its internal
states or logic before it actually loads any configuration files.

In this page you will find all environment variables grouped by "features".

## Configuration Management

| Environment Variable          | Description                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| PYFUNCEBLE_CONFIG_DIR         | If set, PyFunceble will assume its value as the location of the configuration files. |
| PYFUNCEBLE_AUTO_CONFIGURATION | If defined with any value, PyFunceble will accept upstream configuration changes.    |

## Output Management

| Environment Variable       | Description                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------ |
| PYFUNCEBLE_OUTPUT_LOCATION | Defines the folder where PyFunceble will generate the `output/` folder and datasets. |

## Git / CI Management

| Environment Variable    | Description                                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| GIT_NAME                | Defines the `git.name` to setup and use.                                                                                                 |
| GIT_EMAIL               | Defines the `git.email` to setup and use.                                                                                                |
| GIT_BRANCH              | Defines the branch to use to store results between multiple CI/CD sessions. **WARNING:** This doesn't apply to the final results         |
| GIT_DISTRIBUTION_BRANCH | Defines the branch to use to distribute the final results of multiple CI/CD sessions.                                                    |
| GITHUB_TOKEN            | Under a GitHub Action worker or Jenkins CI worker, defines the token to use to authenticate ourselves against the GitHub infrastructure. |
| GL_TOKEN                | Under a GitLab CI/CD runner, defines the token to use to authenticate ourselves against the GitLab infrastructure.                       |
| GH_TOKEN                | Under a Travis CI instance, defines the token to use to authenticate ourselves against the GitHub infrastructure.                        |

## Database Management

The environment variables listed below are used to share your database credentials
with PyFunceble.

| Environment Variable   | Description                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| PYFUNCEBLE_DB_CHARSET  | The charset PyFunceble has to use while writing into the database.                                 |
| PYFUNCEBLE_DB_HOST     | The location of the database. It can be an IP, hostname or an absolute path of a unix socket file. |
| PYFUNCEBLE_DB_PORT     | When `PYFUNCEBLE_DB_HOST` is not a socket file, the port to reach the database through             |
| PYFUNCEBLE_DB_USERNAME | The username to use to authenticate ourselves.                                                     |
| PYFUNCEBLE_DB_PASSWORD | The password to use to authenticate ourselves.                                                     |
| PYFUNCEBLE_DB_NAME     | The name of the database to work with.                                                             |

## Debugging

The environment variables listed below can be used to control the extended outputs of PyFunceble.

!!! danger "Beware!!!"

    Using the debug mode will help you understand what's going one under the hood, but
    may also leak private information inside the `{output-dir}/logs` folder.

    **Never share the debug output unsecurely.**

| Environment Variable       | Description                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| PYFUNCEBLE_DEBUG           | Activates the debug mode.                                                                   |
| PYFUNCEBLE_DEBUG_LVL       | The logging level. Can be any of `NONE`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` or `DEBUG`. |
| PYFUNCEBLE_LOGGING_LVL     | Alias of `PYFUNCEBLE_DEBUG_LVL`.                                                            |
| PYFUNCEBLE_DEBUG_ON_SCREEN | Activates the output of debug logs to STDOUT. Should be `true` or `false`.                  |

## Internal Environment Variables

The environment variables shouldn't be set by yourself, but PyFunceble somehow still
read and use them. #MayTheForceBeWithYou :star:

| Environment Variable | Description                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------- |
| APPDATA              | Used under Windows to build or get the configuration folder, when `PYFUNCEBLE_CONFIG_DIR` is not found. |
| GITHUB_ACTIONS       | Used to detect whether we are running under a GitHub Action worker                                      |
| GITLAB_CI            | Used to detect whether we are running under a GitLab CI/CD runner.                                      |
| GITLAB_USER_ID       | Used to detect whether we are running under a GitLab CI/CD runner.                                      |
| TRAVIS_BUILD_DIR     | Used to detect whether we are running under a Travis CI instance.                                       |
| JENKINS_URL          | Used to detect whether we are running under a Jenkins CI worker.                                        |
| JENKINS_HOME         | Used to detect whether we are running under a Jenkins CI worker.                                        |


## Beta Features
!!! danger "Beware!!!"

    This section is documented, but most of the features below them are not open to everyone - yet.

The environment variables listed below, are strictely reserved to selected or power users.

| Environment Variable            | Description                                                         |
| ------------------------------- | ------------------------------------------------------------------- |
| PYFUNCEBLE_COLLECTION_API_TOKEN | Set the API token to use when pushing data into the collection API. |
