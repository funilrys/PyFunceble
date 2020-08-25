:code:`dns_lookup` (API)
------------------------

Provides the output of the DNS lookup.

Format 1: Normal DNS Lookup
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first and most common output will be like follow:

::

    {
        "A": ["string"],
        "AAAA": ["string"],
        "CNAME": ["string"],
        "NS": ["string"],
        "PTR": ["string"]
    }

where each list item represents the response from the DNS server.


Format 2: :code:`get_hosts_by_addr` (local subjects?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the system to not miss something, it will try to execute the :func:`socket.gethostbyaddr` (for IP) and :func:`socket.gethostbyname` (for the rest).
In both cases, the result will be like follow:

::

    {
        "hostname": "string",
        "aliases": ["string"],
        "ips": ["string"]
    }

