Location
--------

Problematics
^^^^^^^^^^^^

* How can we create a more efficient way to work with configuration?
* How can we make the configuration file(s) available globally so that PyFunceble can be run everywhere in the user workspace?

To answer those problematics, we moved the configuration location elsewhere in the place where most users expect to have their configuration file(s).

Repository clone
^^^^^^^^^^^^^^^^

If you cloned the repository and you're trying to test from a cloned directory (the one with for example :code:`CONTRIBUTING.md`) we consider the configuration directory as the current one.

.. note::
    This behavior allows us to not modify the way we develop PyFunceble.

Travis CI
^^^^^^^^^

Under `Travis CI`_, we search or initiate the configuration at the directory we are currently located.

.. warning::
    We don't care about the distribution, as long as the :code:`TRAVIS_BUILD_DIR` environment variable is set, we search or initiate the configuration in the current directory.

.. note::
    If you want to force the directory where we should work, you can initiate the :code:`PYFUNCEBLE_CONFIG_DIR` environment variable with the path where we should work.

.. _Travis CI: https://travis-ci.org/

GitLab CI/CD
^^^^^^^^^^^^

Under `GitLab CI/CD`_, we search or initiate the configuration at the directory we are currently located.

.. warning::
    We don't care about the distribution, as long as the :code:`PROJECT_CI` and :code:`GITLAB_CI` environment variables are set,
    we search or initiate the configuration in the current directory.

.. note::
    If you want to force the directory where we should work, you can initiate the :code:`PYFUNCEBLE_CONFIG_DIR` environment variable with the path where we should work.

.. _GitLab CI/CD: https://docs.gitlab.com/ee/ci/

Linux and MacOS (Darwin Kernel)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Under Linux and MacOS, we look for the following directories in their order. If any configuration directory is found, the system proposes you to install them automatically on the first configuration file.

1. :code:`~/.config/PyFunceble`
2. :code:`~/.PyFunceble`
3. :code:`${PWD}`

.. note::
    If the parent directory does not exist, we move to the next possible location in the given order.

    This means that under most Linux distributions and MacOS versions, we consider :code:`~/.config/PyFunceble` as the configuration location.
    But if the :code:`~/.config` directory does not exist, we fallback to :code:`~/.PyFunceble` as the configuration location.

Windows
^^^^^^^

As mentioned by `Pat Altimore's`_ Blog, we used the :code:`Per user configuration files synchronized across domain joined machines via Active Directory Roaming` section in order to understand what we should do to find our configuration directory.

Under Windows, we look for the following directories in their order. If any configuration directory is found, the system proposes you to install them automatically on the first configuration file.

1. :code:`%APPDATA%\PyFunceble` (environnement variable)
2. :code:`%CD%`

.. note::
    :code:`%CD%` is explained by the set command (:code:`set /?`):

        :code:`%CD% - expands to the current directory string.`

.. _Pat Altimore's: https://blogs.msdn.microsoft.com/patricka/2010/03/18/where-should-i-store-my-data-and-configuration-files-if-i-target-multiple-os-versions/

.. note::
    If the parent directory does not exist, we move to the next possible location in the given order.

    This means that under most Windows versions, we consider :code:`%APPDATA%\PyFunceble` - also know as :code:`C:\Users\userName\AppData\Roaming\PyFunceble`- as the configuration location.
    But if the :code:`%APPDATA%` directory does not exist, we fall back to the current directory as the configuration location.

Custom location
^^^^^^^^^^^^^^^

Sometimes, you may find yourself in a position where you absolutely do not want PyFunceble to use its default configuration location.

For that reason, if you set your desired configuration location along with the :code:`PYFUNCEBLE_CONFIG_DIR` environment variable, we take that location as the (default) configuration location.
