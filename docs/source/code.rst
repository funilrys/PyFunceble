Documentation of the Code
##########################

.. automodule:: PyFunceble
   :members: test, command_line

Auto-continue
=============

This subsystem is written so that if the system break, we can continue from where we stopped.

Code documentation
------------------

.. automodule::PyFunceble.auto_continue
   :members: 

.. autoclass:: PyFunceble.auto_continue.AutoContinue
    :members:

Autosave
========

This subsystem provide several logic around the autosaving. 
Actually only Travis CI is supported 


Travis CI problematic
---------------------

Indeed, as Travis CI have a default timeout of 45 minutes, we bypass that by autosaving.
On the next session, the auto-continue subsystem restore the last session so we can continue line nothing happend.

Code documentation
------------------

.. automodule::PyFunceble.auto_save
   :members: 

.. autoclass:: PyFunceble.auto_save.AutoSave
    :members:

Cleaning
========

Problematic
-----------

Indeed, as we do not want to have collision between older and new file, we choosed to create a logic which clean the output directory automatically.


Code documentation
------------------

.. automodule::PyFunceble.clean
   :members: 

.. autoclass:: PyFunceble.clean.Clean
    :members:
    :exclude-members: all, file_to_delete

Configuration
=============

Problematic
-----------
As I did not want to relay on a `tool.py` to update the code configuration, I introduction :code:`.PyFunceble.yaml` which contain every configuration needed by every sub- system.

Code documentation
------------------

.. automodule::PyFunceble.config
   :members: 

:code:`Load()`
^^^^^^^^^^^^^^

.. autoclass:: PyFunceble.config.Load
    :members:

:code:`Version()`
^^^^^^^^^^^^^^^^^

.. autoclass:: PyFunceble.config.Version
    :members:

Core
====


Code documentation
------------------

.. automodule::PyFunceble.core
   :members: 

.. autoclass:: PyFunceble.core.Core
    :members:

Database
========

Problematic
-----------

Before the introduction of this class/system, we were testing domains and that's it!
Which this class we allow the continuous testing of INACTIVE domains.

Indeed, we save all :code:`INACTIVE` and :code:`INVALID` into a file called :code:`inactive-db.json` and if the current test is > 24h from the last test, we retest all :code:`INACTIVE` and :code:`INVALID`.

Code documentation
------------------

.. automodule::PyFunceble.database
   :members: 

.. autoclass:: PyFunceble.database.Database
    :members:

Directory Structure
===================

Problematic
-----------

How can we give make the output directory less **annoying** ? 

Why **annoying**? Because before the introduction of this subsystem, the user had to always create the output directory. And if I update the structure, they local structure were broken because it was incompatible with the new update.

Code documentation
------------------

.. automodule::PyFunceble.directory_structure
   :members: 

.. autoclass:: PyFunceble.directory_structure.DirectoryStructure
    :members: