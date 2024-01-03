HTTP Status Code
----------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we want to determine the availability of a domain, IP, or URL; one of our
testing method is the gathering of the HTTP status code.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    We never send a generic User-Agent. You can define your own or let
    PyFunceble choose one of the latest one of one of the major browser for
    you.

When it is the turn of the HTTP status code lookup tool to try to gather a
status for the given subject, an HTTP query is made to the given IP, domain
or subject.

When testing for a domain, a successful HTTP response is considered as
:code:`ACTIVE`.

Otherwise, the following default classification applies.

.. note::
    The classification can be changed by end-user through their configuration
    file.

As ACTIVE
"""""""""

Please note that the following HTTP status codes are considered as ACTIVE.

If you are using the CLI with the analytic files generated, you will get any
matching subject flagged as ACTIVE officially and into your analytic files.

- :code:`100`: Continue
- :code:`101`: Switching Protocols
- :code:`102`: Processing
- :code:`200`: OK
- :code:`201`: Created
- :code:`202`: Accepted
- :code:`203`: Non-Authoritative Information
- :code:`204`: No Content
- :code:`205`: Reset Content
- :code:`206`: Partial Content
- :code:`207`: Multi-Status
- :code:`208`: Already Reported
- :code:`226`: IM User
- :code:`429`: Too Many Request.

As potentially ACTIVE
"""""""""""""""""""""

Please note that the following HTTP status codes are considered as potentially
ACTIVE but still officially reported as ACTIVE when caught.

If you are using the CLI with the analytic files generated, you will get any
matching subject flagged as ACTIVE officially and into your analytic files as
potentially ACTIVE.

- :code:`300`: Multiple Choices
- :code:`301`: Moved Permanently
- :code:`302`: Found
- :code:`303`: See Other
- :code:`304`: Not Modified
- :code:`305`: Use Proxy
- :code:`307`: Temporary Redirect
- :code:`308`: Permanent Redirect
- :code:`403`: Forbidden
- :code:`405`: Method Not Allowed
- :code:`406`: Not Acceptable
- :code:`407`: Proxy Authentication Required
- :code:`408`: Request Timeout
- :code:`411`: Length Required
- :code:`413`: Payload Too Large
- :code:`417`: Expectation Failed
- :code:`418`: I'm a teapot
- :code:`421`: Misdirect Request
- :code:`422`: Unprocessable Entity
- :code:`423`: Locked
- :code:`424`: Failed Dependency
- :code:`426`: Upgrade Required
- :code:`428`: Precondition Required
- :code:`431`: Request Header Fields Too Large
- :code:`500`: Internal Server Error
- :code:`501`: Not Implemented
- :code:`502`: Bad Gateway
- :code:`503`: Service Unavailable
- :code:`504`: Gateway Timeout
- :code:`505`: HTTP Version Not Supported
- :code:`506`: Variant Also Negotiates
- :code:`507`: Insufficient Storage
- :code:`508`: Loop Detected
- :code:`510`: Not Extended
- :code:`511`: Network Authentication Required

As INACTIVE or potentially INACTIVE
"""""""""""""""""""""""""""""""""""

Please note that the following HTTP status codes are considered as INACTIVE or
potentially INACTIVE. Therefore officially reported as INACTIVE when caught.

If you are using the CLI with the analytic files generated, you will get any
matching subject flagged as INACTIVE officially and into your analytic files as
potentially INACTIVE.

- :code:`400`: Bad Request
- :code:`402`: Payment Required
- :code:`404`: Not Found
- :code:`409`: Conflict
- :code:`410`: Gone
- :code:`412`: Precondition Failed
- :code:`414`: Request-URI Too Long
- :code:`415`: Unsupported Media Type
- :code:`416`: Request Range Not Satisfiable
- :code:`451`: Unavailable For Legal Reasons

How to use it?
^^^^^^^^^^^^^^

You can simply allow the usage of the HTTP status code lookup through:

- the (Python) API,
- the CLI argument,
- or, your configuration file.
