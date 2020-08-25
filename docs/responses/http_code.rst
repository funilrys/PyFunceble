HTTP Code
---------

.. note::
    The API equivalent is :code:`http_status_code`.

.. note::
  This section reflects exactly what the code does. So any changes made here should also be reported to the code or at least the configuration file.

.. note::
  A :code:`XXX` in this column means that it was impossible to catch the HTTP status code from the web server.

.. note::
  The Status Codes we give to PyFunceble to test with can be fully customized in your own :code:`.PyFunceble.yaml`.

As active
^^^^^^^^^

.. note::
  While testing for domain and IP, a subject which has an HTTP code listed below, will be saved/logged into the :code:`output/Analytic/ACTIVE` directory.

.. warning::
  While testing for domain and IP, a subject which has an HTTP code listed below and a global status :code:`INACTIVE` or :code:`INVALID` will get its status
  updated to :code:`ACTIVE`.

.. warning::
  While testing for URL, if the extracted HTTP code is in the following list, the global status will be :code:`ACTIVE`.

- 100 - Continue
- 101 - Switching Protocols
- 200 - OK
- 201 - Created
- 202 - Accepted
- 203 - Non-Authoritative Information
- 204 - No Content
- 205 - Reset Content
- 206 - Partial Content

As potentially active
^^^^^^^^^^^^^^^^^^^^^

.. note::
  While testing for domain and IP, a subject which has an HTTP code listed below, will be saved/logged into the :code:`output/Analytic/POTENTIALLY_ACTIVE` directory.

.. warning::
  While testing for domain and IP, a subject which has an HTTP code listed below and a global status :code:`INACTIVE` or :code:`INVALID` will get its status
  updated to :code:`ACTIVE`.

.. warning::
  While testing for URL, if the extracted HTTP code is in the following list, the global status will be :code:`ACTIVE`.

- 000
- 300 - Multiple Choices
- 301 - Moved Permanently
- 302 - Found
- 303 - See Other
- 304 - Not Modified
- 305 - Use Proxy
- 307 - Temporary Redirect
- 403 - Forbidden
- 405 - Method Not Allowed
- 406 - Not Acceptable
- 407 - Proxy Authentication Required
- 408 - Request Timeout
- 411 - Length Required
- 413 - Request Entity Too Large
- 417 - Expectation Failed
- 500 - Internal Server Error
- 501 - Not Implemented
- 502 - Bad Gateway
- 503 - Service Unavailable
- 504 - Gateway Timeout
- 505 - HTTP Version Not Supported

As inactive or potentially inactive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
  While testing for domain and IP, a subject which has an HTTP code listed below, will be saved/logged into the :code:`output/Analytic/POTENTIALLY_INACTIVE` directory.

.. warning::
  While testing for URL, if the extracted HTTP code is in the following list, the global status will be :code:`INACTIVE`.

- 400 - Bad Request
- 401 - Unauthorized
- 402 - Payment Required (Not in use but may be seen in the future)
- 404 - Not Found
- 409 - Conflict
- 410 - Gone
- 412 - Precondition Failed
- 414 - Request-URI Too Long
- 415 - Unsupported Media Type
- 416 - Requested Range Not Satisfiable
