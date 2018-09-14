Columns
=======

Because PyFunceble provide multiple information in a table, we choosed to document them all.
The objective of this page is to reflect what the code actually do in a more clear and understandeable way.

Domains
-------

This column is one of the basic ones as it gives us the name of the last tested domain or IP.

--------------------------------------------------------------------------------

Status
------

There's 3 possible output for this column.

ACTIVE
^^^^^^

This status is returned when **one of the following cases** is met:

- We can extract the expiration date from :code:`Lookup().whois()`.

  - *Please note that we don't check if the date is in the past.*

- :code:`Lookup().nslookup()` don't return an error.

  - *Please note that we don't read the returned value.*

- :code:`HTTPCode().get()` return one the following code :code:`[100, 101, 200, 201, 202, 203, 204, 205, 206]`.

INACTIVE
^^^^^^^^

This status is returned when **all the following cases** are met:

- We can't extract the expiration date from :code:`Lookup().whois()`.
- :code:`Lookup().nslookup()` don't return an error.

INVALID
^^^^^^^

This status is returned when **all the following cases** are met:

- Domain does not match ::

   ^(?=.{0,253}$)(([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9]))$

- IP does not match ::
   
   ^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)

- Domain extension is unregistered in `IANA`_ Root Zone Database.

  - Understand by this that the extension is not present in the :code:`iana-domains-db.json` file.


--------------------------------------------------------------------------------

Expiration Date
---------------

There's two possible output for this column.

Unknown
^^^^^^^

:code:`Unknown` is returned when we could not extract the expiration date from :code:`Lookup().whois()` outputs.

A date
^^^^^^

Only if we could extract the expiration date from :code:`Lookup().whois()`, the date becomes formatted like :code:`02-jan-2017`.

--------------------------------------------------------------------------------

Source
------

At this time, there's 5 possible output for this column.

HTTP Code
^^^^^^^^^

This source is returned when **all the following cases** are met:

- We can't extract the expiration date from :code:`Lookup().whois()`.
- The :code:`INACTIVE` status is the one returned by other methods.
- :code:`HTTPCode().get()` outputs is one the following :code:`[100, 101, 200, 201, 202, 203, 204, 205, 206]`.

IANA
^^^^

This source is always returned when the domain has the status :code:`INVALID` as invalid comparison data come from the `IANA`_ Root Zone Database.

NSLOOKUP
^^^^^^^^

This source is always returned when the taken decision of the status of the domain/IP comes from :code:`Lookup().nslookup()` outputs.

SPECIAL
^^^^^^^

As :code:`PyFunceble` grows, I thought that a bit of filtering for special cases would be great no I introduced SPECIAL into the sources.

Please consider all 3 digits number that are listed in this section as the HTTP status code catched by :code:`HTTPCode().get()`.

:code:`*.blogspot.*`
""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`
- All :code:`301` which are blocked by Google or does not exist are returned as :code:`INACTIVE`
- All :code:`302` which are blocked by Google are returned as :code:`INACTIVE`

:code:`*.canalblog.com`
"""""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.doubleclick.net`
"""""""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.liveadvert.com`
""""""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.skyrock.com`
"""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.tumblr.com`
""""""""""""""""""""

- All :code:`404` are returned as :code:`INACTIVE`

:code:`*.wordpress.com`
"""""""""""""""""""""""

- All :code:`301` which match :code:`doesn’t exist` are returned as :code:`INACTIVE`

IP with range
"""""""""""""

- All IPv4 with a range (for example :code:`0.0.0.0/24`) are returned as :code:`ACTIVE`

--------------------------------------------------------------------------------

HTTP Code
---------

.. note::
  This section reflect exactly what the code do. So any changes made here should also be reported to the code or at least the configuration file.

.. note::
  A :code:`***` in this colomn means that it was impossible to catch the HTTP status code from the webserver.

We have categorized the HTTP Code into 3 parts.

- Active

  - Consider those ones as the one that influences HTTP source logic.
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



.. _IANA: https://www.iana.org/domains/root/db