Code documentation
==================

.. automodule:: PyFunceble
   :members: test

Helpers
-------

Problematic
^^^^^^^^^^^

How can we avoid writing the same thing every time ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.helpers
   :members: 

:code:`Download()`
""""""""""""""""""

.. autoclass:: PyFunceble.helpers.Download
    :members:

:code:`Command()`
"""""""""""""""""

.. autoclass:: PyFunceble.helpers.Command
    :members:

:code:`Regex()`
"""""""""""""""

.. autoclass:: PyFunceble.helpers.Regex
    :members:

:code:`Dict()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.Dict
    :members:

:code:`List()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.List
    :members:

:code:`Directory()`
"""""""""""""""""""

.. autoclass:: PyFunceble.helpers.Directory
    :members:

:code:`File()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.File
    :members:

:code:`Hash()`
""""""""""""""

.. autoclass:: PyFunceble.helpers.Hash
    :members:


Auto-continue
-------------

How can we continue the test after exectutable stop ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.auto_continue
   :members: 

.. autoclass:: PyFunceble.auto_continue.AutoContinue
    :members:

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

.. autoclass:: PyFunceble.auto_save.AutoSave
    :members:

Cleaning
--------

Problematic
^^^^^^^^^^^

How can we clean the :code:`output/` directory so we do not have collision between old and new files ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.clean
   :members: 

.. autoclass:: PyFunceble.clean.Clean
    :members:
    :exclude-members: all, file_to_delete

Configuration
-------------

Problematic
^^^^^^^^^^^

How can we avoid the usage of :code:`tool.py` ?
How can we make personalisation more simple ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.config
   :members: 

:code:`Load()`
""""""""""""""

.. autoclass:: PyFunceble.config.Load
    :members:

:code:`Version()`
"""""""""""""""""

.. autoclass:: PyFunceble.config.Version
    :members:

Core
----


Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.core
   :members: 

.. autoclass:: PyFunceble.core.Core
    :members:

Database
--------

Problematic
^^^^^^^^^^^

How can we continuously test :code:`INACTIVE` and :code:`INVALID` domains or IP ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.database
   :members: 

.. autoclass:: PyFunceble.database.Database
    :members:

Directory Structure
-------------------

Problematic
^^^^^^^^^^^

How can we give make the output directory less **annoying** after update ? 

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.directory_structure
   :members: 

.. autoclass:: PyFunceble.directory_structure.DirectoryStructure
    :members:

Execution Time
--------------

Problematic
^^^^^^^^^^^

How to monitor the execution time of the session ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.execution_time
   :members: 

.. autoclass:: PyFunceble.execution_time.ExecutionTime
    :members:

Expiration Date
---------------

Problematic
^^^^^^^^^^^

How can we get the expiration date of a given domain ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.expiration_date
   :members: 

.. autoclass:: PyFunceble.expiration_date.ExpirationDate
    :members:

Generation
----------

Problematic
^^^^^^^^^^^

How can we generate file which reflects the results of PyFunceble ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.generate
   :members: 

.. autoclass:: PyFunceble.generate.Generate
    :members:

HTTP Code
---------

Problematic
^^^^^^^^^^^

How can we get the HTTP status code of the given domain or IP ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.http_code
   :members: 

.. autoclass:: PyFunceble.http_code.HTTPCode
    :members:

IANA
----

Problematic
^^^^^^^^^^^

How can we get information from IANA ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.iana
   :members: 

.. autoclass:: PyFunceble.iana.IANA
    :members:

Lookup
------

Problematic
^^^^^^^^^^^

How can we get information from WHOIS records ?
How can we check if a domain or IP have a valid pointer (nslookup)?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.lookup
   :members: 

.. autoclass:: PyFunceble.lookup.Lookup
    :members:

Percentage
----------

Problematic
^^^^^^^^^^^

How can we calculate the percentage of each status ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.percentage
   :members: 

.. autoclass:: PyFunceble.percentage.Percentage
    :members:

Prints
------

Problematic
^^^^^^^^^^^

How can we print information on screen and on file in a table format ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.prints
   :members: 

.. autoclass:: PyFunceble.prints.Prints
    :members:

Production
----------

Problematic
^^^^^^^^^^^

How can we efficiently prepare the repository for push/production ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.production
   :members: 

.. autoclass:: PyFunceble.production.Production
    :members:

Referer
-------

Problematic
^^^^^^^^^^^

How can we efficiently get the whois server to call for whois record request ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.referer
   :members: 

.. autoclass:: PyFunceble.referer.Referer
    :members:

Status
------

Problematic
^^^^^^^^^^^

How can we efficiently manage the statuses in function of the test type ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.status
   :members: 

Normal testing
""""""""""""""

.. autoclass:: PyFunceble.status.Status
    :members:

URL testing
"""""""""""

.. autoclass:: PyFunceble.status.URLStatus
    :members:

URL Testing
-----------

Problematic
^^^^^^^^^^^

How can we test full URL ?

Code documentation
^^^^^^^^^^^^^^^^^^

.. automodule::PyFunceble.url
   :members: 

.. autoclass:: PyFunceble.url.URL
    :members:
