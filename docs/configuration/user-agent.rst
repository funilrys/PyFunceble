:code:`user_agent`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`dict`

    **Description:** Configures the user agent.

:code:`user_agent[browser]`
"""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`chrome`

    **Description:** Sets the browser to get the get the latest user agent from.
    Available values: :code:`chrome`, :code:`edge`, :code:`firefox`, :code:`ie`, :code:`opera`, :code:`safari`

.. warning::
    This option is not taken in consideration if :code:`user_agent[custom]` is
    not set to :code:`null`.

:code:`user_agent[platform]`
""""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`linux`

    **Description:** Sets the platform to get the get the latest user agent for.
    Available values: :code:`linux`, :code:`macosx`, :code:`win10`

.. warning::
    This option is not taken in consideration if :code:`user_agent[custom]` is
    not set to :code:`null`.

:code:`user_agent[custom]`
""""""""""""""""""""""""""

    **Type:** :code:`string`

    **Default value:** :code:`null`

    **Description:** Sets the user agent to use.

.. warning::
    Setting this index will overwrite the choices made into
    :code:`user_agent[platform]` and :code:`user_agent[browser]`.
