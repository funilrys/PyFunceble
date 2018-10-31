Code documentation
==================

.. note::
    This section will documents every parts (except the API section) of our code base.

Helpers
-------

Problematic
^^^^^^^^^^^

How can we avoid writing the same thing every time ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule:: PyFunceble.helpers
   :members:
   :private-members:

:code:`Download()`
""""""""""""""""""

.. autoclass:: PyFunceble.helpers.Download
    :members:
    :private-members:

:code:`Command()`
"""""""""""""""""

.. autoclass:: PyFunceble.helpers.Command
    :members:
    :private-members:

:code:`Regex()`
"""""""""""""""

.. autoclass:: PyFunceble.helpers.Regex
    :members:
    :private-members:

:code:`Dict()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.Dict
    :members:
    :private-members:

:code:`List()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.List
    :members:
    :private-members:

:code:`Directory()`
"""""""""""""""""""

.. autoclass:: PyFunceble.helpers.Directory
    :members:
    :private-members:

:code:`File()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.File
    :members:
    :private-members:

:code:`Hash()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.Hash
    :members:
    :private-members:

Auto-continue
-------------

How can we continue the test after exectutable stop ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.auto_continue
   :members:
   :private-members:

.. autoclass:: PyFunceble.auto_continue.AutoContinue
    :members:
    :private-members:

Autosave
--------

This subsystem provide several logic around the autosaving. 
Actually only Travis CI is supported 


Travis CI problematic
^^^^^^^^^^^^^^^^^^^^^

How can we bypass the default Travis CI timeout of 45 minutes ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.auto_save
   :members:
   :private-members:

.. autoclass:: PyFunceble.auto_save.AutoSave
    :members:
    :private-members:

Check
-----

Problematic
^^^^^^^^^^^

How can we efficiently check the format of IP, domains and URL.

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.check
   :members:
   :private-members:

.. autoclass:: PyFunceble.check.Check
    :members:
    :private-members:


Cleaning
--------

Problematic
^^^^^^^^^^^

How can we clean the :code:`output/` directory so we do not have collision between old and new files ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.clean
   :members:
   :private-members:

.. autoclass:: PyFunceble.clean.Clean
    :members:
    :exclude-members: almost_everything, file_to_delete, databases_to_delete

Configuration
-------------

Problematics
^^^^^^^^^^^^

* How can we avoid the usage of :code:`tool.py` ?
* How can we make personalisation more simple ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.config
   :members:
   :private-members:

:code:`Load()`
""""""""""""""

.. autoclass:: PyFunceble.config.Load
    :members:
    :private-members:

:code:`Version()`
"""""""""""""""""

.. autoclass:: PyFunceble.config.Version
    :members:
    :private-members:

Core
----


Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.core
   :members:
   :private-members:

.. autoclass:: PyFunceble.core.Core
    :members:
    :private-members:

Database
--------

Problematics
^^^^^^^^^^^^

* How can we continuously test :code:`INACTIVE` and :code:`INVALID` domains or IP ?
* How can we reduce the number of whois requests over time ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.database
   :members:
   :private-members:

.. autoclass:: PyFunceble.database.Inactive
    :members:
    :private-members:

.. autoclass:: PyFunceble.database.Whois
    :members:
    :private-members:

Directory Structure
-------------------

Problematic
^^^^^^^^^^^

How can we give make the output directory less **annoying** after update ? 

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.directory_structure
   :members:
   :private-members:

.. autoclass:: PyFunceble.directory_structure.DirectoryStructure
    :members:
    :private-members:

Execution Time
--------------

Problematic
^^^^^^^^^^^

How to monitor the execution time of the session ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.execution_time
   :members:
   :private-members:

.. autoclass:: PyFunceble.execution_time.ExecutionTime
    :members:
    :private-members:

Expiration Date
---------------

Problematic
^^^^^^^^^^^

How can we get the expiration date of a given domain ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.expiration_date
   :members:
   :private-members:

.. autoclass:: PyFunceble.expiration_date.ExpirationDate
    :members:
    :private-members:

Generation
----------

Problematic
^^^^^^^^^^^

How can we generate file which reflects the results of PyFunceble ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.generate
   :members:
   :private-members:

.. autoclass:: PyFunceble.generate.Generate
    :members:
    :private-members:

HTTP Code
---------

Problematic
^^^^^^^^^^^

How can we get the HTTP status code of the given domain or IP ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.http_code
   :members:
   :private-members:

.. autoclass:: PyFunceble.http_code.HTTPCode
    :members:
    :private-members:

IANA
----

Problematic
^^^^^^^^^^^

How can we get information from IANA ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.iana
   :members:
   :private-members:

.. autoclass:: PyFunceble.iana.IANA
    :members:
    :private-members:

Lookup
------

Problematics
^^^^^^^^^^^^

* How can we get information from WHOIS records ?
* How can we check if a domain or IP have a valid pointer (nslookup)?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.lookup
   :members:
   :private-members:

.. autoclass:: PyFunceble.lookup.Lookup
    :members:
    :private-members:

Mining
------

Problematic
^^^^^^^^^^^

How can we get the list of domain or URL which link to the desired domain, IPv4 or URL ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.mining
    :members:
    :private-members:

.. autoclass:: PyFunceble.mining.Mining
    :members:
    :private-members:

Percentage
----------

Problematic
^^^^^^^^^^^

How can we calculate the percentage of each status ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.percentage
   :members:
   :private-members:

.. autoclass:: PyFunceble.percentage.Percentage
    :members:
    :private-members:

Prints
------

Problematic
^^^^^^^^^^^

How can we print information on screen and on file in a table format ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.prints
   :members:
   :private-members:

.. autoclass:: PyFunceble.prints.Prints
    :members:
    :private-members:

Production
----------

Problematic
^^^^^^^^^^^

How can we efficiently prepare the repository for push/production ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.production
   :members:
   :private-members:

.. autoclass:: PyFunceble.production.Production
    :members:

Public Suffix
-------------

Problematic
^^^^^^^^^^^

How can we get the list of all possible or at least most used domain suffix ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.publicsuffix
   :members:
   :private-members:

.. autoclass:: PyFunceble.publicsuffix.PublicSuffix
    :members:
    :private-members:

Referer
-------

Problematic
^^^^^^^^^^^

How can we efficiently get the whois server to call for whois record request ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.referer
   :members:
   :private-members:

.. autoclass:: PyFunceble.referer.Referer
    :members:
    :private-members:

Sort
----

Problematic
^^^^^^^^^^^

How can we format the list to test (and the outputed informations) in format other than the alphabetical format ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.sort
   :members:
   :private-members:

.. autoclass:: PyFunceble.sort.Sort
    :members:
    :private-members:

Status
------

Problematic
^^^^^^^^^^^

How can we efficiently manage the statuses in function of the test type ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.status
   :members:
   :private-members:

Normal testing
""""""""""""""

.. autoclass:: PyFunceble.status.Status
    :members:
    :private-members:

URL testing
"""""""""""

.. autoclass:: PyFunceble.status.URLStatus
    :members:
    :private-members:

URL Testing
-----------

Problematic
^^^^^^^^^^^

How can we test full URL ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.url
   :members:
   :private-members:

.. autoclass:: PyFunceble.url.URL
    :members:
    :private-members:

