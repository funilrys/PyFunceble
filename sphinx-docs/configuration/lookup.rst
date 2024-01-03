:code:`lookup`
^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the lookup tools
    to use while testing a given subject.

:code:`lookup[dns]`
"""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of the DNS lookup whether
    possible.

:code:`lookup[http_status_code]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of the HTTP status code
    whether possible.

:code:`lookup[netinfo]`
"""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of the network information
    (or network socket) whether possible.

:code:`lookup[special]`
"""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of our SPECIAL and extra
    rules whether possible.

:code:`lookup[whois]`
"""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of the WHOIS record
    (or better said the expiration date in it) whether possible.

:code:`lookup[reputation]`
""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of the reputation dataset
    whether possible.

:code:`lookup[timeout]`
"""""""""""""""""""""""

    **Type:** :code:`integer`

    **Default value:** :code:`5`

    **Description:** Sets the default timeout to apply to each lookup utilities
    everytime it is possible to define a timeout.

:code:`lookup[collection]`
""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`True`

    **Description:** Activates or disables the usage of the collection dataset
    whether possible.
