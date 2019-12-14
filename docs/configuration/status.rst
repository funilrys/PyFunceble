:code:`status`
^^^^^^^^^^^^^^

    **Type:** :code:`dict`
    
    **Description:** Set the needed, accepted and status name.


:code:`status[list]`
""""""""""""""""""""

    **Type:** :code:`dict`
    
    **Description:** Set the needed and accepted status name.

.. warning::
    All status should be in lowercase.

:code:`status[list][valid]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["valid","syntax_valid","valid_syntax"]`
    
    **Description:** Set the accepted :code:`VALID` status.

.. note::
    This status is only shown if the :code:`syntax` index is activated.

:code:`status[list][up]`
~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["up","active"]`
    
    **Description:** Set the accepted :code:`ACTIVE` status.

:code:`status[list][generic]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["generic"]`
    
    **Description:** Set the accepted :code:`generic` status.

.. note::
    This status is the one used to say the system that we have to print the complete information on the screen.

:code:`status[list][http_active]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["http_active"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][up]` index.


:code:`status[list][down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["down","inactive", "error"]`
    
    **Description:** Set the accepted status :code:`INACTIVE` index.


:code:`status[list][invalid]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["ouch","invalid"]`
    
    **Description:** Set the accepted status :code:`INVALID` index.

:code:`status[list][potentially_down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["potentially_down", "potentially_inactive"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][potentially_down]` index.

:code:`status[list][potentially_up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["potentially_up", "potentially_active"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][potentially_up]` index.

:code:`status[list][suspicious]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:** :code:`["strange", "hum", "suspicious"]`
    
    **Description:** Set the accepted status for the :code:`outputs[analytic][filenames][suspicious]` index.

:code:`status[official]`
""""""""""""""""""""""""

    **Type:** :code:`dict`
    
    **Description:** Set the official status name.

.. note::
    Those status are the ones that are printed on the screen.

.. warning::
    After any changes here please delete :code:`dir_structure.json` and the :code:`output/` directory.

:code:`status[official][up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`ACTIVE`
    
    **Description:** Set the returned status for the :code:`ACTIVE` case.

:code:`status[official][down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`INACTIVE`
    
    **Description:** Set the returned status for the :code:`INACTIVE` case.

:code:`status[official][invalid]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`INVALID`
    
    **Description:** Set the returned status for the :code:`INVALID` case.

:code:`status[official][valid]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`string`

    **Default value:** :code:`VALID`
    
    **Description:** Set the returned status for the :code:`VALID` case.

.. note::
    This status is only shown if the :code:`syntax` index is activated.