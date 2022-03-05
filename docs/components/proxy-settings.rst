Proxy Settings - Matcher
------------------------

.. versionadded:: 4.1.0b12.dev

Why do we need it?
^^^^^^^^^^^^^^^^^^

The primary need is the ability to delegate HTTP(s) queries to a proxy.

The secondary need is the ability to be able to delegate HTTPS(s) queries to
a specif proxy server when a set of rules are matched.

How does it work?
^^^^^^^^^^^^^^^^^

The proxy settings matcher except a subject and return a JSON/dict with the
proxy settings to use. The returned value is then use by our very own Request
Adapter to process the request.

It will first try to extract the extension from the given subject.
As example, if :code:`example.org` is given, the extension will be `org`.

Then, it will go through the list of rules and check if the given extension is
listed inside the :code:`proxy[rules][N][tld]` list. If the extension is in
the read list, the proxy settings matcher will return the provided
:code:`proxy[rules][N][http]` and :code:`proxy[rules][N][https]` proxies.

If no rules is was matched, it will return the provided :code:`proxy[global][http]`
and :code:`proxy[global][https]` proxies.

How to use it?
^^^^^^^^^^^^^^

Simply provides your own own settings into your personal
:code:`.PyFunceble.overwride.yaml` file.

**Example:**

    .. code-block:: yaml

        global:
          http: http://example.org:8080
          https: http://example.org:8080
        rules:
          - http: http://example.com:8080
            https: http://example.org:8080
            tld:
              - com
              - org
              - dev
          - http: socks5://example.dev:8080
            https: socks5://example.dev:8080
            tld:
              - onion
