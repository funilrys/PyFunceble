Configuration
=============
This page will try to detail each configuration available into :code:`.PyFunceble.yaml` along with the location of where we are looking for the configuration file.

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

    This means that under most Windows versions, we consider :code:`%APPDATA%\PyFunceble` - also know as :code:`C:\Users\userName\AppData\PyFunceble`- as the configuration location.
    But if the :code:`%APPDATA%` directory does not exist, we fallback to current directory as the configuration location.

Custom location
"""""""""""""""

Sometimes, you may find yourself in a position where you absolutly do not want PyFunceble to use its default configuration location. 

For that reason, if you set your desired configuration location along with the :code:`PYFUNCEBLE_OUTPUT_DIR` environment variable, we take that location as the (default) configuration location.

Auto configuration
------------------

Sometimes, you may find yourself in a position that you do not or you can't answer the question which ask you if you would like to install the default configuration file. 

For that reason, if you set :code:`PYFUNCEBLE_AUTO_CONFIGURATION` as environnement variable with what you want as assignement, we do not ask that question. We simply do what we have to do whithout asking anything.

-----------------------------------

:code:`adblock`
---------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / disable the adblock format decoding.

.. note::

    If this index is set to :code:`True`, everytime we read a given file, we try to extract the elements that are present.
    
    We basically only decode the adblock format.

.. note::

    If this index is set to :code:`False`, everytime we read a given file, we will consider one line as an element to test.

:code:`auto_continue`
---------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`Trus`
    
    **Description:** Enable / disable the auto continue system.

:code:`command_before_end`
--------------------------

    **Type:** :code:`string`
    
    **Default value:** :code:`""`
    
    **Description:** Set the command to run before the final commit.

.. note::
    The parsed command is called only if :code:`auto_continue` and :code:`travis` are set to :code:`True`.

.. note::
    Understand by final commit the commit which will deliver the last element we have to test.

:code:`custom_ip`
-----------------

    **Type:** :code:`string`
    
    **Default value:** :code:`"0.0.0.0"`
    
    **Description:** Set the custom IP to use when we generate a line in the hosts file format.

.. note::
    This index has no effect if :code:`generate_hosts` is set to :code:`False`.

:code:`days_between_db_retest`
------------------------------

    **Type:** :code:`integer`
    
    **Default value:** :code:`1`
    
    **Description:** Set the number of day(s) between each retest of the :code:`INACTIVE` and :code:`INVALID` elements which are present into :code:`inactive_db.json`.

.. note::
    This index has no effect if :code:`inactive_database` is set to :code:`False`.

:code:`debug`
-------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / disable the generation of debug file(s).

.. note::
    This index has not effect if :code:`logs` is set to :code:`False`

.. warning::
    Do not touch this index unless you a have good reason to.

.. warning::
    Do not touch this index unless you have been invited to.

:code:`filter`
--------------

    **Type:** :code:`string`
    
    **Default value:** :code:`""`
    
    **Description:** Set the element to filter.

.. note::
    This index should be initiated with a regular expression.

:code:`generate_hosts`
----------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / disable the generation of the hosts file(s).

:code:`generate_json`
---------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / disable the generation of the JSON file(s).

:code:`header_printed`
----------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Say to the system if the header has been already printed or not.

.. warning::
    Do not touch this index unless you have a good reason to.

:code:`hierarchical_sorting`
----------------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Say to the system if we have to sort the list and the outputs in a hierarchical order.

:code:`iana_whois_server`
-------------------------

    **Type:** :code:`string`
    
    **Default value:** :code:`whois.iana.org`
    
    **Description:** Set the server to call to get the :code:`whois` referer of a given element.

.. note::
    This index is only used when generating the :code:`iana-domains-db.json` file.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`idna_conversion`
-----------------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Tell the system to convert all domains to IDNA before testing.

.. note::
    We use `domain2idna`_ for the conversion.

.. warning:
    This feature is not supported for the URL testing.

.. _domain2idna: https://github.com/funilrys/domain2idna

:code:`inactive_database`
-------------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / Disable the usage of a database to store the :code:`INACTIVE` and :code:`INVALID` element to retest overtime.

:code:`less`
------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / Disable the output of every information of screen.

:code:`local`
-------------

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Enable / Disable the execution of the test(s) in a local or private network.

:code:`logs`
------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / Disable the output of all logs.

:code:`mining`
--------------

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Enable / Disable the mining subsystem.

:code:`no_files`
----------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / Disable the generation of any file(s).

:code:`no_whois`
----------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / Disable the usage of :code:`whois` in the tests.

:code:`plain_list_domain`
-------------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / Disable the generation of the plain list of elements sorted by statuses.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`quiet`
-------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / Disable the generation of output on screen.

:code:`referer`
---------------

    **Type:** :code:`string`
    
    **Default value:** :code:`""`
    
    **Description:** Set the referer of the element that is currently under tested.

.. warning::
    Do not touch this index unless you a have good reason to.

:code:`seconds_before_http_timeout`
-----------------------------------

    **Type:** :code:`integer`
    
    **Default value:** :code:`3`
    
    **Description:** Set the timeout to apply to every HTTP status code request.

.. note::
    This index must be a multiple of :code:`3`.

:code:`share_logs`
------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / disable the logs sharing.


.. note::
    This index has no effect if :code:`logs` is set to :code:`False`.

:code:`show_execution_time`
---------------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / disable the output of the execution time.

:code:`show_percentage`
-----------------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / disable the output of the percentage of each statuses.

:code:`simple`
--------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / disable the simple output mode.

.. note::
    If this index is set to :code:`True`, the system will only return the result inf format: :code:`tested.element STATUS`. 

:code:`split`
-------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`True`
    
    **Description:** Enable / disable the split of the results files.

.. note::
    Understand with "results files" the mirror of what is shown on screen.

:code:`travis`
--------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / disable the Travis CI autosave system.

.. warning::
    Do not activate this index unless you are using PyFunceble under Travis CI.

:code:`travis_autosave_commit`
------------------------------

    **Type:** :code:`string`
    
    **Default value:** :code:`"PyFunceble - AutoSave"`
    
    **Description:** Set the default commit message we want to use when have to commit (save) but our tests are not yet completed.

:code:`travis_autosave_final_commit`
------------------------------------

    **Type:** :code:`string`
    
    **Default value:** :code:`"PyFunceble - Results"`
    
    **Description:** Set the default final commit message we have to use when have to save and all tests are finished.

:code:`travis_autosave_minutes`
-------------------------------

    **Type:** :code:`integer`
    
    **Default value:** :code:`15`
    
    **Description:** Set the minimum of minutes we have to run before to automatically save our test results.

.. note::
    As many services are setting a rate limit per IP, it's a good idea to set this value between :code:`1` and :code:`15` minutes. 

:code:`travis_branch`
---------------------

    **Type:** :code:`string`
    
    **Default value:** :code:`master`
    
    **Description:** Set the git branch where we are going to push our results.

:code:`unified`
---------------

    **Type:** :code:`boolean`
    
    **Default value:** :code:`False`
    
    **Description:** Enable / Disable the generation of the unified results.

.. note::
    This index has no effect if :code:`split` is set to :code:`True`.

:code:`user_agent`
------------------

    **Type:** :code:`string`
    
    **Default value:** :code:`"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"`
    
    **Description:** Set the User-Agent to use everytime we are requesting something from a web server other than our API.

:code:`outputs`
---------------

    **Type:** :code:`dict`
    
    **Description:** Set the needed output tree/names.

.. warning::
    If you choose to change anything please consider deleting our :code:`output/` directory and the :code:`dir_structure*.json` files.

:code:`outputs[default_files]`
""""""""""""""""""""""""""""""
    
    **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files.

:code:`outputs[default_files][dir_structure]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`dir_structure.json`
    
    **Description:** Set the default filename of the file which have the structure to re-construct.

.. note::
    This index has no influence with :code:`dir_structure_production.json`

:code:`outputs[default_files][iana]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`iana-domains-db.json`
    
    **Description:** Set the default filename of the file which has the formatted copy of the IANA root zone database.

:code:`outputs[default_files][inactive_db]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`inactive_db.json`
    
    **Description:** Set the default filename of the file which will save the list of elements to retest overtime.


:code:`outputs[default_files][results]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`results.txt`
    
    **Description:** Set the default filename of the file which will save the formatted copy of the public suffix database.

:code:`outputs[default_files][public_suffix]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`public-suffix.json`
    
    **Description:** Set the default filename of the file which will save the mirror of what is shown on screen.

:code:`outputs[domains]`
""""""""""""""""""""""""
    
    **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files related to the :code:`plain_list_domain` index.

:code:`outputs[domains][directory]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`domains/`
    
    **Description:** Set the default directory where we have to save the plain list of elements for each status.

:code:`outputs[domains][filename]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`list`
    
    **Description:** Set the default filename of the file which will save the plain list of elements.

:code:`outputs[hosts]`
""""""""""""""""""""""
    
     **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files related to the :code:`generate_hosts` index.

:code:`outputs[hosts][directory]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`hosts/`
    
    **Description:** Set the default directory where we have to save the hosts files of the elements for each status.

:code:`outputs[hosts][filename]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`hosts`
    
    **Description:** Set the default filename of the file which will save the hosts files of the elements.

:code:`outputs[json]`
"""""""""""""""""""""
    
     **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files related to the :code:`generate_json` index.

:code:`outputs[json][directory]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`json/`
    
    **Description:** Set the default directory where we have to save the JSON files of the elements for each status.

:code:`outputs[json][filename]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`dump.json`
    
    **Description:** Set the default filename of the file which will save the JSON files of the elements.

:code:`outputs[analytic]`
"""""""""""""""""""""""""
    
     **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files and directories related to the :code:`generate_hosts` index.

:code:`outputs[analytic][directories]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`
    
    **Description:** Set the default name of some important directories related to the :code:`http_codes[active]` index.

:code:`outputs[analytic][directories][parent]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`Analytic/`
    
    **Description:** Set the default directory where we are going to put everything related to the http analytic.

:code:`outputs[analytic][directories][potentially_down]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`POTENTIALLY_INACTIVE/`
    
    **Description:** Set the default directory where we are going to put all potentially inactive data.


:code:`outputs[analytic][directories][potentially_up]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`POTENTIALLY_INACTIVE/`
    
    **Description:** Set the default directory where we are going to put all potentially active data.

:code:`outputs[analytic][directories][up]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`POTENTIALLY_INACTIVE/`
    
    **Description:** Set the default directory where we are going to put all active data.

:code:`outputs[analytic][directories][suspicious]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`SUSPICIOUS/`
    
    **Description:** Set the default directory where we are going to put all suspicious data.


:code:`outputs[analytic][filenames]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files related to the :code:`http_codes[active]` index and the http analytic subsystem.

:code:`outputs[analytic][filenames][potentially_down]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`down_or_potentially_down`
    
    **Description:** Set the default filename where we are going to put all potentially inactive data.


:code:`outputs[analytic][filenames][potentially_up]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`potentially_up`
    
    **Description:** Set the default filename where we are going to put all potentially active data.

:code:`outputs[analytic][filenames][up]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`active_and_merged_in_results`
    
    **Description:** Set the default filename where we are going to put all active data.

:code:`outputs[analytic][filenames][suspicious]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`suspicious_and_merged_in_results`
    
    **Description:** Set the default filename where we are going to put all suspicious data.


:code:`outputs[logs]`
"""""""""""""""""""""
    
    **Type:** :code:`dict`
    
    **Description:** Set the default name of some important files and directories related to the :code:`logs` index.


:code:`outputs[logs][directories]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
     **Type:** :code:`dict`
    
    **Description:** Set the default name of some important directories related to the :code:`logs` index.


:code:`outputs[logs][directories][date_format]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`date_format/`
    
    **Description:** Set the default directory where we are going to put everything related to the data when the dates are in wrong format.

:code:`outputs[logs][directories][no_referer]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`no_referer/`
    
    **Description:** Set the default directory where we are going to put everything related to the data when no referer is found.

:code:`outputs[logs][directories][parent]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`no_referer/`
    
    **Description:** Set the default directory where we are going to put everything related to the data when no referer is found.

:code:`outputs[logs][directories][percentage]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`percentage/`
    
    **Description:** Set the default directory where we are going to put everything related to percentages.

:code:`outputs[logs][directories][whois]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`whois/`
    
    **Description:** Set the default directory where we are going to put everything related to whois data.

.. note::
    This is the location of all files when the :code:`debug` index is set to :code:`True`.

:code:`outputs[logs][filenames]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    **Type:** :code:`dict`
    
    **Description:** Set the default filenames of some important files related to the :code:`logs` index.

:code:`outputs[logs][filenames][auto_continue]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`continue.json`
    
    **Description:** Set the default filename where we are going to put the data related to the auto continue subsystem.

.. note::
    This file is allocated if the :code:`auto_continue` is set to :code:`True`.

:code:`outputs[logs][filenames][execution_time]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`execution.log`
    
    **Description:** Set the default filename where we are going to put the data related to the execution time.

.. note::
    This file is allocated if the :code:`show_execution_time` is set to :code:`True`.

:code:`outputs[logs][filenames][percentage]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`percentage.txt`
    
    **Description:** Set the default filename where we are going to put the data related to the percentage.

.. note::
    This file is allocated if the :code:`show_percentage` is set to :code:`True`.

:code:`outputs[main]`
"""""""""""""""""""""
    
    **Type:** :code:`string`

    **Default value:** :code:`""`
    
    **Description:** Set the default location where we have to generate the :code:`parent_directory` directory and its dependencies.

:code:`outputs[parent_directory]`
"""""""""""""""""""""""""""""""""
    
    **Type:** :code:`string`

    **Default value:** :code:`output/`
    
    **Description:** Set the directory name of the parent directory which will contains all previously nouned directories.


:code:`outputs[splited]`
""""""""""""""""""""""""
    
    **Type:** :code:`dict`

    **Description:** Set the default name of some important files and directory related to the :code:`split` index.

:code:`outputs[splited][directory]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`
    
    **Default value:** :code:`splited/`
    
    **Description:** Set the default directory name where we are going to put the splited data.

:code:`status`
---------------

    **Type:** :code:`dict`
    
    **Description:** Set the needed, accepted and status name.


:code:`status[list]`
""""""""""""""""""""

    **Type:** :code:`dict`
    
    **Description:** Set the needed and accepted status name.

.. warning::
    All status should be in lowercase.

:code:`status[list][up]`
^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["up","active", "valid"]`
    
    **Description:** Set the accepted :code:`ACTIVE` status.

:code:`status[list][generic]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["generic"]`
    
    **Description:** Set the accepted :code:`generic` status.

.. note::
    This status is the one used to say the system that we have to print the complete information on screen.

:code:`status[list][http_active]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["http_active"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][up]` index.


:code:`status[list][down]`
^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["down","inactive", "error"]`
    
    **Description:** Set the accepted status :code:`INACTIVE` index.


:code:`status[list][invalid]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["ouch","invalid"]`
    
    **Description:** Set the accepted status :code:`INVALID` index.

:code:`status[list][potentially_down]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["potentially_down", "potentially_inactive"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][potentially_down]` index.

:code:`status[list][potentially_up]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["potentially_up", "potentially_active"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][potentially_up]` index.

:code:`status[list][suspicious]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`list`

    **Default value:** :code:`["strange", "hum", "suspicious"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][suspicious]` index.

:code:`status[official]`
""""""""""""""""""""""""

    **Type:** :code:`dict`
    
    **Description:** Set the official status name.

.. note::
    Those status are the ones that are printed on screen.

.. warning::
    After any changes here please delete :code:`dir_structure.json` and the :code:`output/` directory.

:code:`status[official][up]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`ACTIVE`
    
    **Description:** Set the returned status for the :code:`ACTIVE` case.

:code:`status[official][down]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`INACTIVE`
    
    **Description:** Set the returned status for the :code:`INACTIVE` case.

:code:`status[official][invalid]`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`string`

    **Default value:** :code:`INVALID`
    
    **Description:** Set the returned status for the :code:`INVALID` case.


.. todo::
    Complete the documentation...
