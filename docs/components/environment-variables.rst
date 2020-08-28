Environment variables
---------------------

Dotenv files
^^^^^^^^^^^^

Since PyFunceble :code:`2.0.0` (equivalent of PyFunceble-dev :code:`>=1.18.0`), we load (thanks to `python-dotenv`_) the content of
the following files into the (local) list of environment variables.

1. :code:`.env` (current directory)
2. :code:`.pyfunceble-env` (current directory)
3. :code:`.env` (configuration directory)
4. :code:`.pyfunceble-env` (configuration directory)

To quote the `python-dotenv`_ documentation, a :code:`.env` should look like the following:

::

    # a comment and that will be ignored.
    REDIS_ADDRESS=localhost:6379
    MEANING_OF_LIFE=42
    MULTILINE_VAR="hello\nworld"

.. _python-dotenv: https://github.com/theskumar/python-dotenv

What do we use and why ?
^^^^^^^^^^^^^^^^^^^^^^^^

Here is the list of environment variables we use and how we use them if they are set.

+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| **Environment Variable**              | **How do we use it?**                                                                                                |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`DEBUG_PYFUNCEBLE`              | Same as :code:`PYFUNCEBLE_DEBUG` it's just present for retro-compatibility.                                          |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`DEBUG_PYFUNCEBLE_ON_SCREEN`    | Same as :code:`PYFUNCEBLE_DEBUG_ON_SCREEN` it's just present for retro-compatibility.                                |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_AUTO_CONFIGURATION` | Tell us if we have to install/update the configuration file automatically.                                           |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_CHARSET`         | Tell us the MySQL charset to use.                                                                                    |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_HOST`            | Tell us the host or the Unix socket (absolute file path) of the MySQL database.                                      |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_NAME`            | Tell us the name of the MySQL database to use.                                                                       |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_PASSWORD`        | Tell us the MySQL user password to use.                                                                              |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_PORT`            | Tell us the MySQL connection port to use.                                                                            |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_USERNAME`        | Tell us the MySQL user-name to use.                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DEBUG`              | Tell us to log everything into the :code:`output/logs/*.log` files.                                                  |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DEBUG_ON_SCREEN`    | Tell us to log everything to :code:`stdout`                                                                          |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_CONFIG_DIR`         | Tell us the location of the directory to use as the configuration directory.                                         |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_OUTPUT_DIR`         | Same as :code:`PYFUNCEBLE_CONFIG_DIR` it's just present for retro-compatibility.                                     |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_OUTPUT_LOCATION`    | Tell us where we should generate the :code:`output/` directory.                                                      |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`APPDATA`                       | Used under Windows to construct/get the configuration directory if :code:`PYFUNCEBLE_CONFIG_DIR` is not found.       |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GH_TOKEN`                      | Tell us the GitHub token to set into the repository configuration when using PyFunceble under Travis CI.             |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GL_TOKEN`                      | Tell us the GitLab token to set into the repository configuration when using PyFunceble under GitLab CI/CD.          |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GIT_EMAIL`                     | Tell us the :code:`git.email` configuration to set when using PyFunceble under any supported CI environment.         |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GIT_NAME`                      | Tell us the :code:`git.name` configuration to set when using PyFunceble under any supported CI environment.          |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`TRAVIS_BUILD_DIR`              | Used to confirm that we are running under a Travis CI container.                                                     |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GITLAB_CI`                     | Used to confirm that we are running under a GitLab CI/CD environment.                                                |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GITLAB_USER_ID`                | Used to confirm that we are running under a GitLab CI/CD environment.                                                |
+---------------------------------------+----------------------------------------------------------------------------------------------------------------------+