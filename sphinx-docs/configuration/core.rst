:code:`share_logs`
^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the logs sharing.

.. warning::
    As the underlying API and infrastructure was not changed since 2017, I
    choosed to remove all source code related to logs sharing.

    Please consider this as reserved for future usages.

:code:`verify_ssl_certificate`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`boolean`

    **Default value:** :code:`False`

    **Description:** Activates or disables the verification of the
    SSL/TLS certificate when testing for URL.

.. warning::
    If you set this index to :code:`True`, you may get **false positive**
    result.

    Indeed if the certificate is not registered to the CA or is simply
    invalid and the domain is still alive, you will always get
    :code:`INACTIVE` as output.

:code:`max_http_retries`
^^^^^^^^^^^^^^^^^^^^^^^^

    **Type:** :code:`integer`

    **Default value:** :code:`3`

    **Description:** Sets the maximum number of retries for an HTTP request.
