:code:`http_codes`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the HTTP status code and
    the way PyFunceble handles them.

:code:`http_codes[self_managed]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`bool`

    **Default value:** :code:`False`

    **Description:** Informs PyFunceble that the status code list should not be
    managed automatically.

:code:`http_codes[list]`
""""""""""""""""""""""""

    **Type:** :code:`dict`

    **Description:** Categorizes the HTTP status codes.

:code:`http_codes[list][up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:**

        .. code-block:: yaml

            - 100
            - 101
            - 102
            - 200
            - 201
            - 202
            - 203
            - 204
            - 205
            - 206
            - 207
            - 208
            - 226


    **Description:** List the HTTP status codes which are considered as
    :code:`ACTIVE`.

:code:`http_codes[list][potentially_down]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:**

        .. code-block:: yaml

            - 400
            - 402
            - 404
            - 409
            - 410
            - 412
            - 414
            - 415
            - 416
            - 451

    **Description:** List the HTTP status code which are considered
    as :code:`INACTIVE` or :code:`POTENTIALLY_INACTIVE`.


:code:`http_codes[list][potentially_up]`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **Type:** :code:`list`

    **Default value:**

        .. code-block:: yaml

            - 000
            - 300
            - 301
            - 302
            - 303
            - 304
            - 305
            - 307
            - 308
            - 403
            - 405
            - 406
            - 407
            - 408
            - 411
            - 413
            - 417
            - 418
            - 421
            - 422
            - 423
            - 424
            - 426
            - 428
            - 429
            - 431
            - 500
            - 501
            - 502
            - 503
            - 504
            - 505
            - 506
            - 507
            - 508
            - 510
            - 511

    **Description:** List the HTTP status code which are considered as
    :code:`ACTIVE` or :code:`POTENTIALLY_ACTIVE`.
