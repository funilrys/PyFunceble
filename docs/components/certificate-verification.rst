Certificate verification
------------------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

You might sometime be sure that every URL tested with PyFunceble have a valid certificate. This what it's all about!

How does it work?
^^^^^^^^^^^^^^^^^

If the certificate is not valid (catched with :code:`requests`). An :code:`INACTIVE` status is returned (if this component is activated of course)

How to use it?
^^^^^^^^^^^^^^

Simply change

::

    verify_ssl_certificate: False

to

::

    auto_verify_ssl_certificatecontinue: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--verify-ssl-certificate` argument from the CLI to activate it.
