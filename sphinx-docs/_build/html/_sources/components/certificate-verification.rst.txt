Certificate verification
------------------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

You might sometime be sure that every URL tested with PyFunceble have a
valid certificate. This what it's all about!

How does it work?
^^^^^^^^^^^^^^^^^

By default we don't check the certificate, but if you choose to activate this,
as soon as the verification is failed, an :code:`INACTIVE` status will be
returned while testing for URL.

How to use it?
^^^^^^^^^^^^^^

Simply change

::

    verify_ssl_certificate: False

to

::

    verify_ssl_certificate: True


into your personal :code:`.PyFunceble.yaml` or use
the :code:`--verify-ssl-certificate` argument from the CLI to activate it.
