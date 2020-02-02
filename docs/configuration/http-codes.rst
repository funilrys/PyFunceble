:code:`http_codes`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Handle the interpretation of each status codes when we do and generate our analytic data.

:code:`http_codes[active]`
""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`
    
    **Description:** Enable / Disable the usage of the HTTP status code extraction.

:code:`http_codes[list]`
""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Categorize the http status code as mentioned in the documentation related to the :code:`HTTP Code` column.

:code:`http_codes[list][up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:**
        ::

            - 100
            - 101
            - 200
            - 201
            - 202
            - 203
            - 204
            - 205
            - 206

    **Description:** List the HTTP status codes which are considered as :code:`ACTIVE`.

:code:`http_codes[list][potentially_down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:**
        ::

            - 400
            - 402
            - 403
            - 404
            - 409
            - 410
            - 412
            - 414
            - 415
            - 416

    **Description:** List the HTTP status code which are considered as :code:`INACTIVE` or :code:`POTENTIALLY_INACTIVE`.


:code:`http_codes[list][potentially_up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:**
        ::

            - 000
            - 300
            - 301
            - 302
            - 303
            - 304
            - 305
            - 307
            - 403
            - 405
            - 406
            - 407
            - 408
            - 411
            - 413
            - 417
            - 500
            - 501
            - 502
            - 503
            - 504
            - 505

    **Description:** List the HTTP status code which are considered as :code:`ACTIVE` or :code:`POTENTIALLY_ACTIVE`.
