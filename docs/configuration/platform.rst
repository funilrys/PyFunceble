:code:`platform`
^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the interaction with the
    Platform API.

:code:`platform[push]`
""""""""""""""""""""""""

    **Type:** :code:`bool`

    **Default value:** :code:`False`

    **Description:** Activates or disables the push of the test datasets to the
    Platform API.


    .. warning::

        This argument is useless if the :code:`PYFUNCEBLE_PLATFORM_API`
        environment variable is not defined.

:code:`platform[preferred_status_origin]`
"""""""""""""""""""""""""""""""""""""""""""

    **Type:** :code:`str`

    **Default value:** :code:`frequent`

    **Available values:** :code:`frequent`, :code:`latest` , :code:`recommended`

    **Description:** Sets the preferred status origin when fetching data from
    the Platform API.
