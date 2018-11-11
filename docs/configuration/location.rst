Location
--------

Problematics
""""""""""""

* How can we create a more efficient way to work with configuration ?
* How can we make the configuration file(s) available globally so that PyFunceble can be run everywhere in the user workspace ?

To answer those problematics, we moved the configuration location elsewhere in the place where most users expect to have their configuration file(s).

Clone
"""""

If you cloned the repository and you're trying to test from cloned directory (the one with for example :code:`CONTRIBUTING.md`) we consider the configuration directory as the current one.

.. note::
    This behavior allow us to not modify the way we develop PyFunceble.

Travis CI
""""""""""

Under `Travis CI`_, we search or initiate the configuration at the directory we are currently located.

.. warning::
    We don't care about the distribution, as long as the :code:`TRAVIS_BUILD_DIR` environment variable is set, we search or initiate the configuration in the current directory.

.. note::
    If you want to force the directory where we should work, you can initiate the :code:`PYFUNCEBLE_OUTPUT_DIR` environment variable with the path where we should work.

.. _Travis CI: https://travis-ci.org/

Linux
"""""

Under Linux we look for the following directories in their order. If any configuration directory is found, the system proposes you to install them automatically on the first configuration file.

1. :code:`~/.config/PyFunceble`
2. :code:`~/.PyFunceble`
3. :code:`${PWD}`

.. note::
    If the parent directory does not exist, we move to the next possible location in the given order. 

    This means that under most distributions, we consider :code:`~/.config/PyFunceble` as the configuration location. 
    But if  the :code:`~/.config` directory does not exist, we fallback to :code:`~/.PyFunceble` as the configuration location.

Mac (Darwin Kernel)
""""""""""""""""""""

As mentioned by the `Mac Application Environment`_ documentation:

    The Application Support directory is where your app stores any type of file that supports the app but is not required for the app to run, such as document templates or configuration files. 
    The files should be app-specific but should never store user data. This directory is located inside the Library directory.

This means that we follow that direction for our application configuration files. 

.. note::
    The reason we do not use the :code:`Library directory` is because of the mention:

        In OS X v10.7 and later, the Finder hides the Library directory in the user’s home folder by default. Therefore, you should never store files in this directory that you want the user to access. 

    But as we except the user to modify the configuration files as they want, we fallback to the following.

Under MacOS we look for the following directories in their order. If any configuration directory is found, the system proposes you to install them automatically on the first configuration file.

1. :code:`~/Library/Application Support/PyFunceble`
2. :code:`${PWD}`

.. _Mac Application Environment: https://developer.apple.com/library/archive/documentation/General/Conceptual/MOSXAppProgrammingGuide/AppRuntime/AppRuntime.html

.. note::
    If the parent directory does not exist, we move to the next possible location in the given order. 

    This means that under most MacOS, we consider :code:`~/Library/Application Support/PyFunceble` as the configuration location. 
    But if  the :code:`~/Library/Application Support` directory does not exist, we fallback to current directory as the configuration location.

Windows
"""""""

As mentioned by `Pat Altimore's`_ Blog, we used the :code:`Per user configuration files synchronized across domain joined machines via Active Directory Roaming` section in order to understand what we should do to find our configuration directory.

Under Windows we look for the following directories in their order. If any configuration directory is found, the system proposes you to install them automatically on the first configuration file.

1. :code:`%APPDATA%\PyFunceble` (environnement variable)
2. :code:`%CD%`

.. note::
    :code:`%CD%` is explained by the set command (:code:`set /?`):

        :code:`%CD% - expands to the current directory string.`

.. _Pat Altimore's: https://blogs.msdn.microsoft.com/patricka/2010/03/18/where-should-i-store-my-data-and-configuration-files-if-i-target-multiple-os-versions/

.. note::
    If the parent directory does not exist, we move to the next possible location in the given order.

    This means that under most Windows versions, we consider :code:`%APPDATA%\PyFunceble` - also know as :code:`C:\Users\userName\AppData\Roaming\PyFunceble`- as the configuration location.
    But if the :code:`%APPDATA%` directory does not exist, we fallback to current directory as the configuration location.

Custom location
"""""""""""""""

Sometimes, you may find yourself in a position where you absolutely do not want PyFunceble to use its default configuration location. 

For that reason, if you set your desired configuration location along with the :code:`PYFUNCEBLE_OUTPUT_DIR` environment variable, we take that location as the (default) configuration location.

Auto configuration
------------------

Sometimes, you may find yourself in a position that you do not or you can't answer the question which ask you if you would like to install the default configuration file. 

For that reason, if you set :code:`PYFUNCEBLE_AUTO_CONFIGURATION` as environnement variable with what you want as assignment, we do not ask that question. We simply do what we have to do without asking anything.

