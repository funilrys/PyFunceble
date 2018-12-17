HTTP Code
---------

.. note::
  This section reflects exactly what the code does. So any changes made here should also be reported to the code or at least the configuration file.

.. note::
  A :code:`***` in this column means that it was impossible to catch the HTTP status code from the web server.

We have categorized the HTTP Code into 3 parts.

- Active

  - Consider those ones like the one that influences HTTP source logic.
  - Please note that the domain is automatically introduced into the official outputs but we keep a record of it :code:`output/Analytic/ACTIVE`.

- Potentially Active

  - If the domain status returned by other methods are different from :code:`INACTIVE` or :code:`INVALID` and the HTTP status code is into that list, we save the domain into :code:`output/Analytic/POTENTIALLY_ACTIVE`

- Inactive or potentially inactive

  - If the domain status returned by other methods are different from :code:`ACTIVE` and the HTTP status code is on that list, we save the domain into :code:`output/Analytic/POTENTIALLY_INACTIVE`


As active
^^^^^^^^^

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
