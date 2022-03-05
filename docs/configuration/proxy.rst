:code:`proxy`
^^^^^^^^^^^^^

    .. versionadded:: 4.1.0b12.dev

    **Type:** :code:`dict`

    **Description:** Configures everything related to the proxy settings.

:code:`proxy[global]`
"""""""""""""""""""""

    .. versionadded:: 4.1.0b12.dev

    **Type:** :code:`dict`

    **Default value:** :code:`{"http": null, "https": null}`

    **Description:**
        The global proxy settings to use when no rules is matching.

        The proxy settings matcher works with rules, meaning that it will first
        try to match any of the given rules against the hostname that is being
        requested against. If none is matching, it will just take over
        :code:`proxy[global][http]` and :code:`proxy[global][https]`.


.. note::
    Both :code:`http` and :code:`https` keys are required. But, if one is missing
    and the other one is given, PyFunceble will take over the given one.

    If you give the following - as example:

        .. code-block:: yaml

            http: http://example.org:8080
            https: null

    The proxy settings matcher will read/use when no rules is matched:

        .. code-block:: yaml

            http: http://example.org:8080
            https: http://example.org:8080

:code:`proxy[rules]`
""""""""""""""""""""

    .. versionadded:: 4.1.0b12.dev

    **Type:** :code:`list`

    **Default value:** :code:`[]` (None)

    **Description:**
        Sets the list of rules the proxy settings matcher has to follow.

        The proxy settings matcher will first look at the rules listed under
        this key.

        If you give the following - as example:

            .. code-block:: yaml

                proxy:
                  global:
                    http: http://example.de:8080
                    https: http://example.de:8080
                  rules:
                    - http: http://example.dev:8080
                      https: http://example.dev:8080
                      tld:
                        - com
                        - org
                    - http: socks5://example.org:8080
                      https: socks5://example.org:8080
                      tld:
                        - onion

        The proxy settings matcher will:

            - use :code:`http://example.dev:8080` for any :code:`HTTP` and
              :code:`HTTPS` requests to a subject that has the :code:`com` and
              :code:`org` Top-Level-Domain (TLD).

              **Example**: :code:`example.com` and :code:`example.org`

            - use :code:`socks5://example.org:8080` for any :code:`HTTP` and
              :code:`HTTPS` requests to a subject that has the :code:`onion`
              Top-Level-Domain (TLD).

              **Example**: :code:`example.onion`

            - use :code:`http://example.de` for any :code:`HTTP` and :code:`HTTPS`
              requests to any other subject that is not matching the previous
              rules.
