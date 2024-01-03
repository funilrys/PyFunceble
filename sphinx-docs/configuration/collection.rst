:code:`collection`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the interaction with the
    collection API.

:code:`collection[url_base]`
""""""""""""""""""""""""""""

    **Type:** :code:`str`

    **Default value:** :code:`http://localhost:8080`

    **Description:** Sets the base URL of the collection API.

:code:`collection[push]`
""""""""""""""""""""""""

    **Type:** :code:`bool`

    **Default value:** :code:`False`

    **Description:** Activates or disables the push of the test datasets to the
    collection API.


    .. warning::

        This argument is useless if the :code:`PYFUNCEBLE_COLLECTION_API`
        environment variable is not defined.

:code:`collection[preferred_status_origin]`
"""""""""""""""""""""""""""""""""""""""""""

    **Type:** :code:`str`

    **Default value:** :code:`frequent`

    **Available values:** :code:`frequent`, :code:`latest` , :code:`recommended`

    **Description:** Sets the preferred status origin when fetching data from
    the collection
