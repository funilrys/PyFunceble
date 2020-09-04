:code:`outputs`
^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Set the needed output tree/names.

.. warning::
    If you choose to change anything please consider deleting our :code:`output/` directory and the :code:`dir_structure*.json` files.

:code:`outputs[default_files]`
""""""""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Set the default name of some important files.

:code:`outputs[default_files][dir_structure]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`dir_structure.json`

    **Description:** Set the default filename of the file which has the structure to re-construct.

.. note::
    This index has no influence with :code:`dir_structure_production.json`

:code:`outputs[default_files][iana]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`iana-domains-db.json`

    **Description:** Set the default filename of the file which has the formatted copy of the IANA root zone database.

:code:`outputs[default_files][inactive_db]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`inactive_db.json`

    **Description:** Set the default filename of the file which will save the list of elements to retest overtime.


:code:`outputs[default_files][results]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`results.txt`

    **Description:** Set the default filename of the file which will save the formatted copy of the public suffix database.

:code:`outputs[default_files][public_suffix]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`public-suffix.json`

    **Description:** Set the default filename of the file which will save the mirror of what is shown on screen.

:code:`outputs[default_files][mining]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`mining.json`

    **Description:** Set the default filename of the file which will save the temporary list of mined subject to test.


:code:`outputs[default_files][whois_db]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`whois_db.json`

    **Description:** Set the default filename of the file which will save the whois information for caching.

:code:`outputs[domains]`
""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Set the default name of some important files related to the :code:`plain_list_domain` index.

:code:`outputs[domains][directory]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`domains/`

    **Description:** Set the default directory where we have to save the plain list of elements for each status.

:code:`outputs[domains][filename]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`list`

    **Description:** Set the default filename of the file which will save the plain list of elements.

:code:`outputs[hosts]`
""""""""""""""""""""""

     **Type:** :code:`dict`

    **Description:** Set the default name of some important files related to the :code:`generate_hosts` index.

:code:`outputs[hosts][directory]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`hosts/`

    **Description:** Set the default directory where we have to save the hosts files of the elements for each status.

:code:`outputs[hosts][filename]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`hosts`

    **Description:** Set the default filename of the file which will save the hosts files of the elements.

:code:`outputs[json]`
"""""""""""""""""""""

     **Type:** :code:`dict`

    **Description:** Set the default name of some important files related to the :code:`generate_json` index.

:code:`outputs[json][directory]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`json`

    **Description:** Set the default directory where we have to save the JSON files of the elements for each status.

:code:`outputs[json][filename]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`dump.json`

    **Description:** Set the default filename of the file which will save the JSON files of the elements.

:code:`outputs[complements]`
""""""""""""""""""""""""""""

     **Type:** :code:`dict`

    **Description:** Set the default name of some important files/directories related to the :code:`generate_complements` index.


:code:`outputs[complements][directory]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`complements`

    **Description:** Set the default directory where we have to save the complements related files sorted by status.

:code:`outputs[analytic]`
"""""""""""""""""""""""""

     **Type:** :code:`dict`

    **Description:** Set the default name of some important files and directories related to the :code:`generate_hosts` index.

:code:`outputs[analytic][directories]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`dict`

    **Description:** Set the default name of some important directories related to the :code:`http_codes[active]` index.

:code:`outputs[analytic][directories][parent]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`Analytic/`

    **Description:** Set the default directory where we are going to put everything related to the HTTP analytic.

:code:`outputs[analytic][directories][potentially_down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`POTENTIALLY_INACTIVE/`

    **Description:** Set the default directory where we are going to put all potentially inactive data.


:code:`outputs[analytic][directories][potentially_up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`POTENTIALLY_INACTIVE/`

    **Description:** Set the default directory where we are going to put all potentially active data.

:code:`outputs[analytic][directories][up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`POTENTIALLY_INACTIVE/`

    **Description:** Set the default directory where we are going to put all active data.

:code:`outputs[analytic][directories][suspicious]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`SUSPICIOUS/`

    **Description:** Set the default directory where we are going to put all suspicious data.


:code:`outputs[analytic][filenames]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`dict`

    **Description:** Set the default name of some important files related to the :code:`http_codes[active]` index and the HTTP analytic subsystem.

:code:`outputs[analytic][filenames][potentially_down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`down_or_potentially_down`

    **Description:** Set the default filename where we are going to put all potentially inactive data.


:code:`outputs[analytic][filenames][potentially_up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`potentially_up`

    **Description:** Set the default filename where we are going to put all potentially active data.

:code:`outputs[analytic][filenames][up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`active_and_merged_in_results`

    **Description:** Set the default filename where we are going to put all active data.

:code:`outputs[analytic][filenames][suspicious]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`suspicious_and_merged_in_results`

    **Description:** Set the default filename where we are going to put all suspicious data.


:code:`outputs[logs]`
"""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Set the default name of some important files and directories related to the :code:`logs` index.


:code:`outputs[logs][directories]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

     **Type:** :code:`dict`

    **Description:** Set the default name of some important directories related to the :code:`logs` index.


:code:`outputs[logs][directories][date_format]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`date_format/`

    **Description:** Set the default directory where we are going to put everything related to the data when the dates are in the wrong format.

:code:`outputs[logs][directories][no_referer]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`no_referer/`

    **Description:** Set the default directory where we are going to put everything related to the data when no referer is found.

:code:`outputs[logs][directories][parent]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`no_referer/`

    **Description:** Set the default directory where we are going to put everything related to the data when no referer is found.

:code:`outputs[logs][directories][percentage]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`percentage/`

    **Description:** Set the default directory where we are going to put everything related to percentages.

:code:`outputs[logs][directories][whois]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`whois/`

    **Description:** Set the default directory where we are going to put everything related to whois data.

.. note::
    This is the location of all files when the :code:`debug` index is set to :code:`True`.

:code:`outputs[logs][filenames]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`dict`

    **Description:** Set the default filenames of some important files related to the :code:`logs` index.

:code:`outputs[logs][filenames][auto_continue]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`continue.json`

    **Description:** Set the default filename where we are going to put the data related to the auto continue subsystem.

.. note::
    This file is allocated if the :code:`auto_continue` is set to :code:`True`.

:code:`outputs[logs][filenames][execution_time]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`execution.log`

    **Description:** Set the default filename where we are going to put the data related to the execution time.

.. note::
    This file is allocated if the :code:`show_execution_time` is set to :code:`True`.

:code:`outputs[logs][filenames][percentage]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    **Description:** Set the directory name of the parent directory which will contain all previously nouned directories.


:code:`outputs[splited]`
""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Set the default name of some important files and directory related to the :code:`split` index.

:code:`outputs[splited][directory]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`splited/`

    **Description:** Set the default directory name where we are going to put the split data.
