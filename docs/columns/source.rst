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

This source is always returned when the domain has the status :code:`INVALID`.
The usage of this source comes from the comparison of the element extension against the `IANA`_ Root Zone Database.

SYNTAX
^^^^^^

This source is always returned when the domain has the status :code:`INVALID` or in the case that we are only checking for syntax instead of availability.
The usage of this source comes from the comparison of the element against our domain, IP or URL syntax validation system.


NSLOOKUP
^^^^^^^^

This source is always returned when the taken decision of the status of the domain/IP comes from :code:`Lookup().nslookup()` outputs.

SPECIAL
^^^^^^^

As :code:`PyFunceble` grows, I thought that a bit of filtering for special cases would be great. 
So I introduced the SPECIAL source.


.. note::
    Please consider all 3 digits number that are listed in this section as the HTTP status code catched by :code:`HTTPCode().get()`.

.. warning::
    Do not want those rules ? You can use following to disable them.

    * :code:`-ns`|:code`--no-special` arguments from the CLI.
    * :code:`no_special: True` into your local configuration file.

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
