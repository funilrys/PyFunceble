Expiration Date
---------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we want to determine the availability from the WHOIS record - if available,
we need to extract and provide the expiration date.

How does it work?
^^^^^^^^^^^^^^^^^

After the query of the WHOIS record, it is parsed so that we can extract
the expiration date.

When successful, a date in the format :code:`09-oct-1970` is provided to the
end-user. Otherwise, :code:`null` is provided to those using the API and
:code:`Unknown` to those using the CLI.

How to use it?
^^^^^^^^^^^^^^

You can simply allow the usage of the WHOIS lookup through:

- the (Python) API,
- the CLI argument,
- or, your configuration file.
