:code:`cli_decoding`
^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures everything related to the decoding of the given
    input sources.

:code:`cli_decoding[adblock]`
"""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the adblock decoding.

.. note::
    If this index is set to :code:`True`, every time we read a given file, we
    try to extract the elements that are present.

    We basically only decode the adblock format.

.. note::
    If this index is set to :code:`False`, every time we read a given file, we
    will consider one line as an element to test.

:code:`cli_decoding[aggressive]`
""""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables disable some aggressive settings
    related to the adblock decoding.

.. warning::
    This option is available but please keep in mind that the underlying source
    code is still experimental.

:code:`cli_decoding[rpz]`
"""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the decoding of RPZ policies
    from each given input files.

:code:`cli_decoding[wildcard]`
""""""""""""""""""""""""""""""

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the decoding of wildcards for each
    given input files.
