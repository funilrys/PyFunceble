..
    In this document I uses the following variables to ref:

    $DOMAIN or $URI as single instances
    $DOMAIN_FILE or $URL_FILES as files with content of same type

    Usage of example.tld

    We should strive to use the example.org for likeable examples and
    example.com for the evil (blacklistable) domains

    These values are set as UPPERCase as ref to output variables from a
    script. / @spirillen

    We uses double lines between sections (for the eye) / @spirillen

From a terminal
---------------

This chapter also relates to writing scripts in bash and PowerShell as
the uses the same syntaxes.


:code:`--show-completion "shell"`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Show shell completion script and exit.

**Available Values**: :code:`bash`, :code:`zsh`

.. note::
    This argument provides the  autocompletion script that you can use to get
    access to the autocompletion assistance.

    It is meant to be used like this:

    .. code-block:: console

        $ source <(pyfunceble --show-completion bash)
        $ pyfunceble --do[TAB]
        --domain  --dots

:code:`--help`
^^^^^^^^^^^^^^

Show the help message and exit.


------

:code:`-v` | :code:`--version`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Show the version of PyFunceble and exit.


------

Test sources
^^^^^^^^^^^^


:code:`-d "$DOMAIN"` | :code:`--domain "$DOMAIN"`
"""""""""""""""""""""""""""""""""""""""""""""""""

This argument takes one or more values separated by spaces.

Test one or more :code:`$DOMAIN`s,

.. code-block:: console

    $ PyFunceble -d example.org example.net

A domain is defined as it do NOT start with a :code:`protocol://` and it do not
contain a forward slash :code:`/`

This is a domain: :code:`example.org`

.. note::
    When this option is used, no output files are generated.


------

:code:`-u "$URI"` | :code:`--url "$URI"`
""""""""""""""""""""""""""""""""""""""""""

Test one or more full URL, separated by spaces.

This argument takes one or more values.

.. code-block:: console

    $ PyFunceble -url https://example.org/AlIvE https://example.com/GoNe

.. note::
    When we test the availability of a URL, we (only) check the HTTP status
    code of the given URL.

A URI or URL is defined by it is starting with a protocol.

    This is a URL :code:`http://example.org/?example=yes`

    This is another URL :code:`https://example.org`

    This is another URL :code:`ftp://ftp.example.org`


------

.. _domain_source:

:code:`-f "$DOMAIN"` | :code:`--file "$DOMAIN_FILE"`
""""""""""""""""""""""""""""""""""""""""""""""""""""

Read a local or remote (RAW link) file and test all domains inside it.
If remote (RAW link) file is given, PyFunceble will download it,
and test the content of the given RAW link as if it was a locally stored
file.

.. code-block:: console

    $ PyFunceble -f "$DOMAIN"_1 "$DOMAIN"_2
    $ PyFunceble -f "$DOMAIN_FILE"_1 "$DOMAIN_FILE"_2
    $ PyFunceble --file "$DOMAIN_FILE"_1 "$DOMAIN_FILE"_2

.. note::
    - This argument takes one or more space separated values.
    - You can combine :code:`-f` and :code:`-uf` in the same test.

.. warning::
    You can not combine the usage of :code:`-f`, :code:`-uf` with
    :code:`--adblock` at the same time


------

.. _URL_FILES:

:code:`-uf "$URL_FILES"` | :code:`--url-file "$URL_FILES"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Read a local or remote (RAW link) file and test all (full) URLs inside it.
If remote (RAW link) file is given, PyFunceble will download it,
and test the content of the given RAW link as if it was a locally stored
file.

This argument test if a URL which is inside the given file is available.
It ONLY tests full URLs.

.. code-block:: console

    $ PyFunceble -uf "$URI"_1 "$URI"_2

When a remote located source is provided, we will download the given URL and
test its content assuming that each line represents a URL to test.

.. code-block:: console

    $ PyFunceble -uf "$URL_FILES"

.. note::
    - This argument takes one or more space separated values.
    - You can combine :code:`-f` and :code:`-uf` in the same test.
    - We consider one line as one URL to test.

.. warning::
    A test with this argument consists of the comparison of the status code.
    No WHOIS record will be requested nor DNS Lookup will be done.

    You can not combine the usage of :code:`-f`, :code:`-uf` and
    :code:`--adblock` at the same time


------

Source filtering, decoding, conversion and expansion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:code:`--adblock`
"""""""""""""""""

This feature is used to extract all domains, IPv4 and IPv6 addresses from a
adblock formatted file and test the status and validate the extracted
domains.

To use this feature you'll need to set the :ref:`domain_source` to tell
PyFunceble from where to obtain the given list.

.. code-block:: console

    $ pyfunceble --adblock -f "$ADBLOCK_FILES"

**Default value:** :code:`adblock: False`

.. warning::
    You can not combine the usage of :code:`-f`, :code:`-uf` and
    :code:`--adblock` at the same time


------

:code:`--cidr`
""""""""""""""

This feature will expand CIDR formatted addresses.

**Default value:** :code:`cidr_expand: False`


------

:code:`--complements`
"""""""""""""""""""""

A complement is for example :code:`example.org` if :code:`www.example.org`
is given and vice-versa.

**Default value:** :code:`complements: False`


------

:code:`--filter "RegEx"`
""""""""""""""""""""""""

A Regex string to match in order to test a given line.

**Default value:** :code:`file_filter: null`

If you only want to test all :code:`blogspot` URI or domains from your list,
this argument allows you to do that!

.. code-block:: console

    $ pyfunceble --filter '^\.blogspot\.(com|net)$' -f $DOMAIN_FILE


------

:code:`--mining`
""""""""""""""""

.. TODO::

    Find out more about how this actually works...

Want to find domain or URL linked to a domain in your list? This argument will
exactly do that.

**Default value:** :code:`mining: False`


------

:code:`--rpz`
"""""""""""""
.. versionadded:: 3.3.3

.. sectionauthor:: @funilrys

Activates or disables the decoding of RPZ policies from each given input source
(:code:`-f`).

.. code-block:: console

    $ pyfunceble --rpz -f $RPZ_FILES

.. sectionauthor:: @spirillen

The :code:`--rpz` is used to test domains from a fully functional and valid
RPZ_ (Response Policy Zone). If you do provide the required zone :code:`SOA`
record it will extract the right domains to test.

Example of a fully functional RPZ_ zone

.. code-block:: console

    spyware.my-rpz.internal.   86400   IN      SOA     my.awesome.rps.zone. need.to.know.only. 2021011401 300 60 604800 3600
    *.360.com.spyware.my-rpz.internal. 86400   IN      CNAME   .
    *.360safe.com.cn.spyware.my-rpz.internal.  86400   IN      CNAME   .
    *.360totalsecurity.com.spyware.my-rpz.internal.    86400   IN      CNAME   .
    360.com.spyware.mypdns.cloud.   86400   IN      CNAME   .
    360safe.com.cn.spyware.mypdns.cloud.    86400   IN      CNAME   .
    360totalsecurity.com.spyware.mypdns.cloud.      86400   IN      CNAME   .

(PS. RPZ_ zones does not requires the NS records :rfc:`1034`)

From the example above PyFunceble will be testing the following domains.

.. code-block::

    360.com
    *.360.com
    360safe.com.cn
    *.360safe.com.cn
    360totalsecurity.com
    *.360totalsecurity.com

You can make a simple test with the above zone example by copy/pasting.

In case your RPZ zone are missing the required :code:`SOA` entry, you should
consider combining the :code:`--rpz` with `--wildcard <index.html#wildcard>`_ to
avoid all your wildcard's domain becoming marked as :code:`INVALID`

**Default value:** :code:`rpz: False`

.. warning::
    You can currently not use the :code:`--rpz` in combination with
    :code:`--syntax` to validate or syntax test a rpz formatted file.

.. seealso::
    See discussions
    `149 <https://github.com/funilrys/PyFunceble/discussions/149>`_ for more
    information and participate in it's development.


------

:code:`--wildcard`
""""""""""""""""""
.. versionadded:: 3.3.0

The flag to use when your source(:code:`-f`) of domains starts with a wildcard.

This flag will subtract the :code:`*.$DOMAIN` and test the :code:`$DOMAIN`
according to the test arguments given.

**Default value:** :code:`wildcard: False`

As examples of when to use this argument. The first one will
return INVALID if :code:`--wildcard` is not set to true.

This feature is related to the `--rpz <index.html#rpz>`_

.. code-block:: console

    '*.example.org'
    'example.org'


------

Test control
^^^^^^^^^^^^

:code:`--chancy`
""""""""""""""""

.. versionadded:: 4.1.0b4.dev

Activates a chancy mode that unleashes the safety workflow in place.

**Default value**: :code:`chancy_tester: False`

.. warning::
    You shouldn't have to use this unless you feel really lucky and trust your
    machine.

    This mode makes things look 'fast', but it may produce some unexpected
    results if :code:`N` process simultaneously write the same output file.

    This mode makes the graphical CLI output unparsable - either.

    **MAY THE FORCE BE WITH YOU!**

------

:code:`--cooldown-time`
"""""""""""""""""""""""

Sets a cooldown time (in second) to be applied between (sleep) before/between
each test cycles is done.

**Default value:** :code:`cooldown_time: 0.0`


------

:code:`--local`
"""""""""""""""

Activates or disables the consideration of the test(s) in or for a local
or private network context.

This option is to include testing ability of records only availeble for
local and private network. This argument will enable this functionality
by removing the usual limitation which do not apply to intranets.

**Default value:** :code:`local_network: False`

------

:code:`--collection-preferred-origin`
"""""""""""""""""""""""""""""""""""""

.. versionadded:: 4.0.0

Sets the preferred status origin.

**Default value:** :code:`collection.preferred_status_origin: frequent`

**Available values:** :code:`frequent`, :code:`latest`, :code:`recommended`


------

:code:`--collection-lookup`
"""""""""""""""""""""""""""

.. versionadded:: 4.0.0

Activates or disables the usage of the collection lookup whether possible.

**Default value:** :code:`lookup.collection: False`

Want to take advantage of the collection API ? This argument is for you.

------

:code:`--collection-lookup-only`
""""""""""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the collection lookup as test
method.

------

:code:`--dns-lookup`
""""""""""""""""""""

Activates or disables the usage of the DNS lookup whether possible.

**Default value:** :code:`dns: True`

Don't want to perform some DNS lookup? This argument is for you.

------

:code:`--dns-lookup-only`
"""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the DNS lookup as test
method.

------

:code:`--http-status-code-lookup` | :code:`--http`
""""""""""""""""""""""""""""""""""""""""""""""""""

Don't want to take the result of the HTTP code execution into consideration?

This argument allows you to disable the HTTP status code checker!

**Default value:** :code:`http_status_code: True`


------

:code:`--http-status-code-lookup-only`
""""""""""""""""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the HTTP Status code lookup as test
method.

------

:code:`--netinfo-lookup`
""""""""""""""""""""""""

Activates or disables the usage of the network information
(or network socket) whether possible.

Don't want to perform some netinfo lookup ? This argument is for you.

**Default value:** :code:`netinfo: True`


------


:code:`--netinfo-lookup-only`
"""""""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the NETINFO lookup as test
method.

------

:code:`--special-lookup`
""""""""""""""""""""""""

Activates or disables the usage of our SPECIAL and extra rules whether possible.

Don't want to use/apply the `Special Rules <../responses/source.html#special>`_
- which are explained in the source column section?

This argument disables them all.

**Default value:** :code:`special: True`


------


:code:`--special-lookup-only`
"""""""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the SPECIAL lookup as test
method.

------

:code:`--whois-lookup`
""""""""""""""""""""""
.. versionadded:: 4.0.0

Activates or disables the usage of the WHOIS record (or better said the
expiration date in it) when possible.

Don't want to use or take the :code:`whois` date into consideration?
This argument allows you to disable it!

**Default value:** :code:`whois: True`

.. note::
    When you use the :code:`--syntax` no WHOIS data lookup will be performed
    In other words: :code:`--syntax` overrules this argument


------


:code:`--whois-lookup-only`
"""""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the WHOIS lookup as test
method.

------

:code:`--reputation-lookup`
"""""""""""""""""""""""""""

.. TODO::

    Check which of the reputation is alive or the code difference

Want to take the reputation data into consideration?

Activates or disables the usage of the reputation dataset when possible.

**Default value:** :code:`reputation: False`


------


:code:`--reputation-lookup-only`
""""""""""""""""""""""""""""""""

.. versionadded:: 4.1.0b10

Activates or disables the exclusive usage of the Reputation lookup as test
method.

------

:code:`--reputation`
""""""""""""""""""""

Activates or disables the reputation checker.

**Default value:** :code:`False`


------

:code:`--syntax`
""""""""""""""""

This code is to check the syntax of domains when the
`-f <index.html#f-domain-file-domain-file>`_ and URI's when
`--url <index.html#url-uri-url-uri>`_ is used as source.

You should be able to use both :code:`-f` and `code:`-uf` at the same time with
:code:`--syntax`

When you are using this flags there will not be performed any other test, such
as the `WHOIS <index.html#whois-lookup>`_ or
`HTTP status code <index.html#http-status-code-lookup-http>`_

**Default value:** :code:`syntax: False`

.. note::

    *TIP*: If you would like to gain some serious performance while testing
    with :code:`--syntax`, We recommend you disable
    `--auto-continue <index.html#c-auto-continue-continue>`_

    See note for :code:`--rpz`


------

:code:`-t "seconds"` | :code:`--timeout "seconds"`
""""""""""""""""""""""""""""""""""""""""""""""""""

Sets the default timeout to apply to each lookup utilities
every time it is possible to define a timeout.

**Default value:** :code:`timeout: 5` seconds

------

.. versionadded:: 4.0.3b1.dev

:code:`--max-http-retries "number"`
"""""""""""""""""""""""""""""""""""


Sets the maximum number of retries for an HTTP request.

**Default value:** :code:`max_http_retries: 3`

------

:code:`-ua "full string"` | :code:`--user-agent "full string"`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

User defined user agent to use in the
`http <index.html#http-status-code-lookup-http>`_ status code lookup.

.. code-block:: yaml

    user_agent:
        browser: chrome
        platform: linux

.. warning::
    If not given, we try to get the latest (automatically) for you

Example of how to change the default from CLI.

.. code-block:: console

    $ pyfunceble --user-agent "Mozilla/5.0 (X11; U; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"



------

:code:`-vsc` | :code:`--verify-ssl-certificate`
"""""""""""""""""""""""""""""""""""""""""""""""

Activates or disables the verification of the SSL/TLS certificate when
testing for URL.

**Default value:** :code:`verify_ssl_certificate: False`

.. warning::
    If you activate the verification of the SSL/TLS certificate, you may
    get **false-positive** results.

    Indeed if the certificate is not registered to the CA or is simply
    invalid and the domain is still alive, you will always get
    :code:`INACTIVE` as output.


------

DNS control
^^^^^^^^^^^

:code:`--dns`
"""""""""""""

By default, PyFunceble will use the system-wide DNS settings. This can be
changed with the ability to configure which DNS-Servers you like PyFunceble to
use during the test.

You set this up with the CLI command :code:`--dns` **or** insert it into your
personal :code:`.PyFunceble.yaml`

You can add several separated by spaces and they will all be used in a order.
(Kind of Round Robin style)

**Default value:** :code:`Follow OS DNS` ==> :code:`server: null`

.. code-block:: console

    $ pyfunceble -dns 127.0.1.53:5303 127.0.0.1 -f $DOMAIN_FILE

You can also set default DNS servers used for testing within the
:code:`my_project/.PyFunceble.yaml` file. (No secondary indent)

.. code-block:: yaml

      server:
      - 1.2.3.4
      - 5.6.7.8
      - 9.10.11.12:5302

.. warning::
    We expect a DNS server(s). If you add this flag but no DNS server(s) is
    given. You'll almost for certain get all results as :code:`INACTIVE`

    This could happen in case you use :code:`--dns -f`

.. note::
    You can specify the port number to be used on the DNS server if needed.

    If you provide an IPv6, we are expecting the :code:`[ip]:port` format.


------

.. _dns-protocol:

:code:`--dns-protocol`
""""""""""""""""""""""

Sets the protocol to use for the DNS queries.

**Default value:** :code:`protocol: UDP`

**Available values:** :code:`UDP`, :code:`TCP`, :code:`HTTPS`, :code:`TLS`.
Case-Sensitive

.. code-block:: console

    $ pyfunceble --dns doh.powerdns.org --dns-protocol HTTPS -f $DOMAIN_FILE

.. note:
    You can not mix protocols. IE. the following will only test on the
    :code:`doh.powerdns.org` dns server.

.. code-block:: console

    $ pyfunceble --dns 192.0.2.2:53 --dns doh.powerdns.org --dns-protocol HTTPS


------

.. _follow-server-order:


:code:`--follow-server-order`
"""""""""""""""""""""""""""""

.. versionadded:: 4.0.0

Let us follow or mix the order of usage of the given or found DNS server(s).

**Default value:** :code:`True`


------

.. _trust-dns-server:

:code:`--trust-dns-server`
""""""""""""""""""""""""""

.. versionadded:: 4.0.0

Activates or disable the trust mode.

**Default value:** :code:`False`

.. note::
    When active, when the first read DNS server give us a negative response
    - without error - we take it as it it.

    Otherwise, if not active, when the first read DNS server give us
    a negative response - without error - we still consolidate by
    checking all given/found server.

------


.. _dns-delay:

:code:`--dns-delay`
"""""""""""""""""""

.. versionadded:: 4.1.0b12.dev

Sets the delay to apply between each DNS query.

**Default value:** :code:`0.0`

.. note::
    When greater that :code:`0.0`, a delay will be applied between each DNS
    query.

    Otherwise, if equal to `0.0`, no delay will be applied.

------

Proxy control
^^^^^^^^^^^^^

.. _http-proxy:

:code:`--http-proxy`
""""""""""""""""""""

.. versionadded:: 4.1.0b12.dev

By default, PyFunceble will use the environment-wide Proxy Settings. This can be
changed with the ability to configure which Proxy Server you like PyFunceble to
use during the test of subject.

You can set this up with the CLI command :code:`--http-proxy` **or** insert it
into your personal :code:`.PyFunceble.overwrite.yaml`

**Default value:** :code:`Follow HTTP_PROXY variable`

.. code-block:: console

    $ pyfunceble --http-proxy http://127.0.0.1:9899 -f $DOMAIN_FILE

You can also set default DNS servers used for testing within the
:code:`my_project/.PyFunceble.yaml` file. (No secondary indent)

.. code-block:: yaml

    global:
        http: http://127.0.0.1:9899


.. warning::
    We expect a Proxy Server. If you add this flag but no valid Proxy Server is
    given. You'll almost for certain get all results as :code:`INACTIVE`

------

.. _https-proxy:

:code:`--https-proxy`
"""""""""""""""""""""

.. versionadded:: 4.1.0b12.dev

By default, PyFunceble will use the environment-wide Proxy Settings. This can be
changed with the ability to configure which Proxy Server you like PyFunceble to
use during the test of subject.

You can set this up with the CLI command :code:`--https-proxy` **or** insert it
into your personal :code:`.PyFunceble.overwrite.yaml`

**Default value:** :code:`Follow HTTPS_PROXY variable`

.. code-block:: console

    $ pyfunceble --https-proxy http://127.0.0.1:9899 -f $DOMAIN_FILE

You can also set default DNS servers used for testing within the
:code:`my_project/.PyFunceble.yaml` file. (No secondary indent)

.. code-block:: yaml

    global:
        https: http://127.0.0.1:9899


.. warning::
    We expect a Proxy Server. If you add this flag but no valid Proxy Server is
    given. You'll almost for certain get all results as :code:`INACTIVE`

------

Databases
^^^^^^^^^

:code:`--inactive-database`
"""""""""""""""""""""""""""

Switch the value of the usage of a database to store inactive domains of
the currently tested list.

**Default value:** :code:`db_clean: 28` Day(s).

This argument will disable or enable the usage of a database which saves all
:code:`INACTIVE` and :code:`INVALID` domain of the given file over time.


------

:code:`--database-type`
"""""""""""""""""""""""

Sets the database engine to use.

**Default value:** :code:`db_type: csv`

**Available values:** :code:`csv`, :code:`mariadb`, :code:`mysql`.


------

:code:`--inactive-db`
"""""""""""""""""""""

Activates or disables the usage of a 'database' to store all
'INACTIVE' and 'INVALID' subject for continuous retest.

Configured value: :code:`inactive_db: True`


------

:code:`-dbr "time"` | :code:`--days-between-db-retest "time"`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Sets the numbers of days since the introduction of a
subject into the inactive dataset before it gets retested.

**Default value:** :code:`db_retest: 1` Day(s)

.. note::
    This argument is only used if :code:`-db` or
    :code:`inactive_database : true` (under :code:`.PyFunceble.yaml`) are
    activated. See also `--inactive-db <index.html#inactive-db>`_


------

:code:`-wdb` | :code:`--whois-database`
"""""""""""""""""""""""""""""""""""""""

Activates or disables the usage of a "database" to store
the expiration date of all domains with a valid expiration date.

**Default value:** :code:`whois_db: True`


------

Output control
^^^^^^^^^^^^^^


:code:`-a` | :code:`--all`
""""""""""""""""""""""""""

Activates or disables the display of the all information in the table we
print to stdout (screen).

**Default value:** :code:`all: False`

**Default:**

.. code-block:: console

    Domain                        Status      Source
    ----------------------------- ----------- ----------
    pyfunceble.readthedocs.io     ACTIVE      SYNTAX

**When :code:`all: True`:**

.. code-block:: console

    Domain                        Status      Expiration Date   Source     HTTP Code  Checker
    ----------------------------- ----------- ----------------- ---------- ---------- -------------
    pyfunceble.readthedocs.io     ACTIVE      Unknown           NSLOOKUP   302        AVAILABILITY


------

:code:`--color` | :code:`--colour`
""""""""""""""""""""""""""""""""""

Activates or disables the coloration to STDOUT.

**Default value:** :code:`colour: True`

Don't want any colour ? This argument is for you!


------

:code:`--display-status`
""""""""""""""""""""""""
.. versionadded:: 4.0.0

Sets the status that we are allowed to print to stdout.

Multiple space separated statuses can be given.

**Default value:** :code:`status: all`

**Available values:** :code:`all`, :code:`ACTIVE`, :code:`INACTIVE`,
:code:`INVALID`, :code:`VALID`, :code:`SANE`, :code:`MALICIOUS`

*Default response*

.. code-block:: console

    $ pyfunceble -d google-analytics.com duckduckgo.com --whois-lookup

    Subject                                              Status      Source
    ---------------------------------------------------- ----------- ----------
    duckduckgo.com                                       ACTIVE      DNSLOOKUP
    google-analytics.com                                 INACTIVE    STDLOOKUP

*Show only active and inactive*

.. code-block:: console

    $ pyfunceble -d google-analytics.com duckduckgo.com --whois-lookup \
    --display-status INACTIVE ACTIVE

    Subject                                              Status      Source
    ---------------------------------------------------- ----------- ----------
    duckduckgo.com                                       ACTIVE      DNSLOOKUP
    google-analytics.com                                 INACTIVE    STDLOOKUP

*Show only inactive*

.. code-block:: console

    $ pyfunceble -d google-analytics.com duckduckgo.com --whois-lookup \
      --display-status INACTIVE

    Subject                                              Status      Source
    ---------------------------------------------------- ----------- ----------
    google-analytics.com                                 INACTIVE    STDLOOKUP

.. note::
    If you have provided more than one $DOMAIN_FILE as input source, then the
    printed status will be in same order as your $DOMAIN_FILE was given in the
    input.

    For an example you can visit:
    `github <https://github.com/funilrys/PyFunceble/issues/238>`_


------

:code:`-ex` | :code:`--execution`
"""""""""""""""""""""""""""""""""

Want to know the execution time of your test? Well, this argument will let
you know!

**Default value:** :code:`execution_time: False`


------

:code:`--hierarchical`
""""""""""""""""""""""

Activates or disables the sorting of the files content (output) in a
hierarchical order.

**Default value:** :code:`hierarchical: False`

This argument will output the result listed in a hierarchical order.


------

:code:`-h` | :code:`--hosts`
""""""""""""""""""""""""""""

This argument will let the system know if it want to generate a hosts formatted
result file for each status.

**Default value:** :code:`hosts: True`

.. seealso::

    :ref:`--plain <plaindomain>`, :ref:`--no-files <no-file>`

.. note::

    There is an ongoing request to set the default value of :code:`hosts: False`
    You should be following this issue as it might affect your setup/results
    later on.
    `Flip defaults for host <https://github.com/funilrys/PyFunceble/issues/178>`_


------

:code:`-ip "ip-address"` | :code:`--hosts-ip` "ip-address"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Sets the IP to prefix each lines of the hosts file.

**Default value:** :code:`0.0.0.0`


------

.. _logging-level:

:code:`--logging-level`
"""""""""""""""""""""""
    .. versionadded:: 4.0.0

You can configure the logging level to be outputted in STDOUT (screen)
when you uses :code:`--no-files`. Default outputs to
:code:`output/__pyfunceble_loggging__/*.log`

Please notice this is a separated folder at the same lever as your
tested sources.

.. code-block:: console

    ├── /tmp/pyfunceble/output/__pyfunceble_loggging__/
    ├── /tmp/pyfunceble/output/my-blacklist/


Optional values. (From less to more information)

.. hlist::
    :columns: 1

    * :code:`--logging-level critical` ==> CRITICAL
    * :code:`--logging-level error` ==> ERROR
    * :code:`--logging-level info` ==> INFO **(default)**
    * :code:`--logging-level warning` ==> WARNING
    * :code:`--logging-level debug` ==> DEBUG


------

.. _merge-output

:code:`--merge-output`
""""""""""""""""""""""

Activates or disables the merging of the outputs of all inputted files inside a
single subdirectory as opposed to the normal behavior.

**Default value:** :code:`merge_output_dirs: False`


------

.. _no-file:

:code:`--no-files`
""""""""""""""""""

Activates or disables the generation of any non-logs and status file(s).

**Default value:** :code:`no_file: False`

.. note:
    If you set this to true, this will also disable the generation of the end
    statistic.

.. seealso::

    `-h | --host <#h-host>`_,
    :ref:`--plain <plaindomain>`


------

:code:`--output-location`
"""""""""""""""""""""""""
    .. versionadded:: 4.0.0

This is used to direct the output location and matches
`PYFUNCEBLE_OUTPUT_LOCATION <#global-variables>`_.

With this new option you no longer need to add the Global Variable but can
append it directly to the CLI string.

.. code-block:: console

    $ pyfunceble --output-location /tmp/pyfunceble -f $DOMAIN_FILE


------

:code:`--unified-results`
"""""""""""""""""""""""""

Activates or disables the generation of the unified results file instead of the
divided output in individual subfolder under :code:`output/`.

**Default value:** :code:`unified_results: False`

This argument disables the generation of the :code:`result.txt` file.


------

:code:`--percentage`
""""""""""""""""""""

Activates or disables the display and generation of the
percentage - file - of each status.

**Default value:** :code:`percentage: True`

This argument will disable or enable the generation of the percentage of each
status.

------

:code:`--registrar`
"""""""""""""""""""

.. versionadded:: 4.1.0b1.dev

Activates or disables the display and generation of the (top) registrar stats -
file.

**Default value:** :code:`registrar: False`

------

:code:`--max-registrar`
"""""""""""""""""""""""

.. versionadded:: 4.1.0b1.dev

Sets the maximum number of registrar to display.

**Default value:** :code:`max_registrar: 15`

.. note::
    This option does not take effect on the generated file.

------

.. _plaindomain:

:code:`--plain`
"""""""""""""""

Activates or disables the generation of the generation of clean file(s).

This will output a file per status only containing the subject(s). (One record
per line)

**Default value:** :code:`plain: True`

.. seealso::

    `-h | --host <#h-host>`_, :ref:`--no-files <no-file>`


------

:code:`--dots`
""""""""""""""

**CLI** only: Activate or disables the display of dots or other characters when we
**skip** the test of a subject.

**CI** only: If you combine the :code:`--ci --dots` we display a dot for each
record we tests.

**Default value:** :code:`dots: False`


------

:code:`-q` | :code:`--quiet`
""""""""""""""""""""""""""""

Activates or disables the display of output to the terminal.

**Default value:** :code:`quiet: False`

------

:code:`--push-collection`
"""""""""""""""""""""""""

.. versionadded:: 4.0.0

Activates or disables the push of the test results into the collection API.

**Default value:** :code:`collection.push: False`

Want to take submit data into the collection API ? This argument is for you.

.. warning::

    This argument is useless if the :code:`PYFUNCEBLE_COLLECTION_API` environment
    variable is not defined.

------

:code:`--share-logs`
""""""""""""""""""""

Want to help make PyFunceble a better tool?

Then you can share your logs with our backend API which collect all logs!

**Default value:** :code:`share_logs: False`

.. versionchanged:: 4.0.0

.. seealso::
    `Logs Sharing Component </components/index.html#logs-sharing>`_.


------

:code:`-s` | :code:`--simple`
"""""""""""""""""""""""""""""

Activates or disables the simple output mode.

**Default value:** :code:`simple: False`

Want as less as possible data on screen? This argument returns as less as
possible on screen!


------

Multiprocessing
^^^^^^^^^^^^^^^

:code:`-w` | :code:`--max-workers`
""""""""""""""""""""""""""""""""""

    .. versionadded:: 4.0.0

Sets the number of maximal worker to use.

Keep in mind that the :code:`--max-workers` mostly - if not only - affects
the number of tester sub-processes. Because we want to safely write the
files, we still need a single process which read the submitted results and
generate the outputs.

The reason we added this to PyFunceble :code:`4.0.0` is we don't want to
have a wrongly formatted output file.

If you have more than 2 CPU cores/processes the default will be number of
CPU - 2. Otherwise, it will 1.

**Default value:** :code:`max_workers: null`

.. note::

    If you have a CPU with 4 cores or Threads (depends on it's age) Then the
    number of workers will be 4 - 2 = 2 workers

.. warning::

    This section about `max-workers` is still under construction, but it is
    close to how it is working.

    - **This means you should be experimenting a bit your self.**

    To follow the "behind the scene" talk about the subject, please take a
    look at `issue <https://mypdns.org/spirillen/PyFunceble/-/issues/34>`_


------

CI / CD
^^^^^^^

:code:`--ci`
""""""""""""

Activates or disables the Continuous Integration mechanism.

**Default value:** :code:`active: False`

.. note::
    If you combine this argument with the :code:`--quiet` argument, the test
    will output a dotted line, where each dot (:code:`.`) represent one test
    result or input which was skipped because it was previously tested.

Want to use PyFunceble under a supported CI infrastructure/network? This
argument is suited for your needs!


------

:code:`--ci-max-minutes`
""""""""""""""""""""""""

Sets the number of minutes to wait before starting to stop a CI session.

**Default value:** :code:`max_exec_minutes: 15`


------

:code:`--ci-branch`
"""""""""""""""""""

Sets our git working branch. This is the branch from where
we are supposed to store the tests (excepts the final results).

**Default value:** :code:`branch: master`

.. note::
    Currently the branch need to exist, but there are being worked on a path
    to have PyFunceble to create the sub-branch and finally merge it into the
    :code:`--ci-distribution-branch`


------

:code:`--ci-distribution-branch`
""""""""""""""""""""""""""""""""

Sets our git distributions branch. This is the branch from where we are
supposed to store and push the final results.

**Default value:** :code:`distribution_branch: master`

.. note::
    The difference between this and :code:`--ci-branch` is the fact
    that this branch will get the (final) result only when the test is finished
    under the given :code:`--ci-branch`.

As an example, this allows us to have 2 branches:

.. code-block:: console

    --ci-branch processing # (CI branch), for the tests with PyFunceble.
    --ci-distribution-branch master # (CI distribution branch), for the
                                    # distribution of the results of PyFunceble.


------

:code:`--ci-command "something"`
""""""""""""""""""""""""""""""""

    .. versionchanged:: 4.0.0

Sets the command to execute before each commit (except the final one).

**Default value:** :code:`command: null`

.. note::
    In this example, :code:`something` should be a script or a program which
    have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true` (under
    :code:`.PyFunceble.yaml`) are activated.


------

:code:`--ci-end-command "something"`
""""""""""""""""""""""""""""""""""""
.. versionchanged:: 4.0.0

Sets the command to execute before the final commit.

**Default value:** :code:`end_command: null`

.. note::
    In this example, :code:`something` should be a script or a program which
    have to be executed when we reached the end of the given file.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are activated.


------

:code:`--ci-commit-message "message"`
"""""""""""""""""""""""""""""""""""""
.. versionchanged:: 4.0.0

Sets the commit message to apply every time we have to apply a commit except
for the really last one.

**Default value:** :code:`commit_message: "PyFunceble - AutoSave"`

This argument allows us to set a custom commit message which is going to be
used as a commit message when saving.

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we have to split the work into multiple
    processes because a list is too long or the timeout is reached.

.. warning::
    Please avoid the usage of :code:`[ci skip]` here.


------

:code:`--ci-end-commit-message`
"""""""""""""""""""""""""""""""
.. versionchanged:: 4.0.0

Sets the commit message to apply at the really end.

**Default value:** :code:`end_commit_message: "PyFunceble - Results"`

.. note::
    This argument is only used if :code:`--ci` or :code:`ci: true`  (under
    :code:`.PyFunceble.yaml`) are used.

.. note::
    This argument is only used if we reached the end of the list we are or
    have to test.


------

:code:`-c` | :code:`--auto-continue` | :code:`--continue`
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This argument is to used for auto-continuing from a previously under CI

**Default value:** :code:`autocontinue: False`

This argument activates or deactivates the auto-continue subsystem.
Indeed, as we can automatically continue if the script has been stopped,
this switch allows us to disable or enable the usage of that specific
subsystem.


------

:code:`--preload`
"""""""""""""""""

.. versionadded:: 4.0.0

Activates or disables the preloading of the input file(s) into the continue
dataset before starting the tests.

The `--preload` argument - or its option counterpart - ping
is given, we decode and load the given input files into the continue
dataset before starting the test.

This reduces the waiting time while continuing a previous session.

.. note::
    This argument is useless unless the
    `auto continue <index.html#c-auto-continue-continue>`_ subsystem is
    active.

    The preloading may take some time depending of the size of the file to
    test, but this is the price for a smooth and better autocontinue.
    Especially under CI's.


------

Global Variables
^^^^^^^^^^^^^^^^

Here is the list of environment variables we use and how we use them if they
are set.

.. note::
    If used in a script like bash or a terminal directly you have to use the
    :code:`export` as PyFunceble is running as sub-processes

+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| **Environment Variable**                | **How to use them?**                                                                                                 |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_AUTO_CONFIGURATION`   | Tell us if we have to install/update the configuration file automatically.                                           |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_COLLECTION_API_TOKEN` | Sets the API token to use when pushing data into the collection API.                                                 |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_CONFIG_DIR`           | Tell us the location of the directory to use as the configuration directory.                                         |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_CHARSET`           | Tell us the MariaDB charset to use.                                                                                  |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_HOST`              | Tell us the host or the Unix socket (absolute file path) of the MariaDB database.                                    |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_NAME`              | Tell us the name of the MariaDB database to use.                                                                     |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_PASSWORD`          | Tell us the MariaDB user password to use.                                                                            |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_PORT`              | Tell us the MariaDB connection port to use.                                                                          |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DB_USERNAME`          | Tell us the MariaDB user-name to use.                                                                                |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DEBUG`                | Tell us to log everything into the :code:`output/logs/*.log` files.                                                  |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DEBUG_LVL`            | Sets the logging level to use. :ref:`logging-level`                                                                  |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_DEBUG_ON_SCREEN`      | Tell us to log everything to :code:`stdout` bool (true | false)                                                      |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_LOGGING_LVL`          | Same as :code:`PYFUNCEBLE_DEBUG_LVL`. :ref:`logging-level`                                                           |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`PYFUNCEBLE_OUTPUT_LOCATION`      | Tell us where we should generate the :code:`output/` directory.                                                      |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`APPDATA`                         | Used under Windows to construct/get the configuration directory if :code:`PYFUNCEBLE_CONFIG_DIR` is not found.       |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GH_TOKEN`                        | Tell us the GitHub token to set into the repository configuration when using PyFunceble under Travis CI.             |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GL_TOKEN`                        | Tell us the GitLab token to set into the repository configuration when using PyFunceble under GitLab CI/CD.          |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GIT_EMAIL`                       | Tell us the :code:`git.email` configuration to set when using PyFunceble under any supported CI environment.         |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GIT_NAME`                        | Tell us the :code:`git.name` configuration to set when using PyFunceble under any supported CI environment.          |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`TRAVIS_BUILD_DIR`                | Used to confirm that we are running under a Travis CI container.                                                     |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GITLAB_CI`                       | Used to confirm that we are running under a GitLab CI/CD environment.                                                |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| :code:`GITLAB_USER_ID`                  | Used to confirm that we are running under a GitLab CI/CD environment.                                                |
+-----------------------------------------+----------------------------------------------------------------------------------------------------------------------+


Global overview
^^^^^^^^^^^^^^^

::

    usage: pyfunceble [--show-completion {bash,zsh,tcsh}]
                    [-d DOMAINS [DOMAINS ...]] [-u URLS [URLS ...]]
                    [-f FILES [FILES ...]] [-uf URL_FILES [URL_FILES ...]]
                    [--adblock] [--cidr] [--complements] [--preload]
                    [--filter CLI_TESTING__FILE_FILTER] [--mining] [--rpz]
                    [--wildcard] [--chancy] [-c]
                    [--cooldown-time CLI_TESTING__COOLDOWN_TIME] [--local]
                    [--collection-preferred-origin {frequent,latest,recommended}]
                    [--collection-lookup] [--collection-lookup-only]
                    [--dns-lookup] [--dns-lookup-only] [--http] [--http-only]
                    [--netinfo-lookup] [--netinfo-lookup-only]
                    [--special-lookup] [--special-lookup-only] [--whois-lookup]
                    [--whois-lookup-only] [--reputation-lookup]
                    [--reputation-lookup-only] [--reputation] [--syntax]
                    [-t LOOKUP__TIMEOUT] [--max-http-retries MAX_HTTP_RETRIES]
                    [-ua USER_AGENT__CUSTOM] [-vsc]
                    [--dns DNS__SERVER [DNS__SERVER ...]]
                    [--dns-protocol {UDP,TCP,HTTPS,TLS}] [--follow-server-order]
                    [--trust-dns-server] [--dns-delay DNS__DELAY]
                    [--http-proxy PROXY__GLOBAL__HTTP]
                    [--https-proxy PROXY__GLOBAL__HTTPS] [--inactive-db]
                    [--database-type {csv,mariadb,mysql}]
                    [-dbr CLI_TESTING__DAYS_BETWEEN__DB_RETEST] [-wdb] [-a]
                    [-ex] [--colour]
                    [--display-status {all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} [{all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} ...]]
                    [--dots] [--hierarchical] [-h] [-ip CLI_TESTING__HOSTS_IP]
                    [--merge-output] [--no-files]
                    [--output-location OUTPUT_LOCATION] [--unified-results]
                    [--percentage] [--registrar]
                    [--max-registrar CLI_TESTING__DISPLAY_MODE__MAX_REGISTRAR]
                    [--plain] [-q] [--push-collection] [-s]
                    [-w CLI_TESTING__MAX_WORKERS]
                    [--ci-max-minutes CLI_TESTING__CI__MAX_EXEC_MINUTES] [--ci]
                    [--ci-branch CLI_TESTING__CI__BRANCH]
                    [--ci-distribution-branch CLI_TESTING__CI__DISTRIBUTION_BRANCH]
                    [--ci-command CLI_TESTING__CI__COMMAND]
                    [--ci-end-command CLI_TESTING__CI__END_COMMAND]
                    [--ci-commit-message CLI_TESTING__CI__COMMIT_MESSAGE]
                    [--ci-end-commit-message CLI_TESTING__CI__END_COMMIT_MESSAGE]
                    [--help] [-v]

    PyFunceble - The tool to check the availability or syntax of domain, IP or URL.

    options:
        --show-completion {bash,zsh,tcsh}
                                Show Shell completion script and exit.
        --help                Show this help message and exit.
        -v, --version         Show the version of PyFunceble and exit.

    Test sources:
        -d DOMAINS [DOMAINS ...], --domain DOMAINS [DOMAINS ...]
                                Test one or more domains, separated by spaces.

                                When this option is used, no output files are generated.
        -u URLS [URLS ...], --url URLS [URLS ...]
                                Test one or more full URL, separated by spaces.
        -f FILES [FILES ...], --file FILES [FILES ...]
                                Read a local or remote (RAW link) file and test all domains inside it.
                                If remote (RAW link) file is given, PyFunceble will download it,
                                and test the content of the given RAW link as if it was a locally stored file.
        -uf URL_FILES [URL_FILES ...], --url-file URL_FILES [URL_FILES ...]
                                Read a local or remote (RAW link) file and test all (full) URLs inside it.
                                If remote (RAW link) file is given, PyFunceble will download it,
                                and test the content of the given RAW link as if it was a locally stored file.

                                This argument test if an URL is available. It ONLY test full URLs.

    Source filtering, decoding, conversion and expansion:
        --adblock             Activates or deactivates the decoding of the adblock format.
                                Configured value: False
        --cidr                Activates or disables the expansion of CIDR formatted
                                addresses.
                                Configured value: False
        --complements         Activates or disables the generation and test of the
                                complements.
                                A complement is for example `example.org` if 'www.example.org'
                                is given and vice-versa.
                                Configured value: False
        --preload             Activates or disables the preloading of the input
                                file(s) into the continue dataset before starting the tests.

                                This reduces the waiting time while continuing a previous
                                session.
                                Note: This is useless when the auto continue subsystem is not active.
                                Configured value: False
        --filter CLI_TESTING__FILE_FILTER
                                Regex to match in order to test a given line.
                                Configured value: None
        --mining              Activates or disables the mining subsystem.
                                Configured value: False
        --rpz                 Activates or disables the decoding of RPZ policies
                                from each given input files.
                                Configured value: False
        --wildcard            Activates or disables the decoding of wildcards for
                                each given input files.
                                Configured value: False

    Test control:
        --chancy, --ludicrous
                                Activates a chancy mode that unleashes the safety
                                workflow in place.

                                WARNING: You shouldn't have to use this unless you feel really lucky
                                and trust your machine. This mode makes things look 'fast',
                                but it may produce some unexpected results if N process
                                simultaneously write the same output file.
                                This mode makes the graphical CLI output unparsable - either.

                                MAY THE FORCE BE WITH YOU!

                                Configured value: False
        -c, --auto-continue, --continue
                                Activates or disables the autocontinue subsystem.
                                Configured value: False
        --cooldown-time CLI_TESTING__COOLDOWN_TIME
                                Sets the cooldown time (in second) to apply between
                                each test.
                                Configured value: 0.0
        --local               Activates or disables the consideration of the test(s)
                                in or for a local or private network context.
                                Configured value: False
        --collection-preferred-origin {frequent,latest,recommended}
                                Sets the preferred status origin.
                                Configured value: 'recommended'
        --collection-lookup   Activates or disables the usage of the Collection lookup
                                whether possible.
                                Configured value: False
        --collection-lookup-only
                                Only perform a Collection lookup.
        --dns-lookup          Activates or disables the usage of the DNS lookup
                                whether possible.
                                Configured value: True
        --dns-lookup-only     Only perform a DNS lookup.
        --http, --http-status-code-lookup
                                Switch the value of the usage of HTTP code.
                                Configured value: True
        --http-only, --http-status-code-lookup-only
                                Only perform a HTTP Code lookup.
        --netinfo-lookup      Activates or disables the usage of the network
                                information (or network socket) whether possible.
                                Configured value: True
        --netinfo-lookup-only
                                Only perform a network information (or networket socket) lookup.
        --special-lookup      Activates or disables the usage of our SPECIAL and
                                extra rules whether possible.
                                Configured value: True
        --special-lookup-only
                                Only perform a SPECIAL lookup.
        --whois-lookup        Activates or disables the usage of the WHOIS record
                                (or better said the expiration date in it) whether possible.
                                Configured value: True
        --whois-lookup-only   Only perform a WHOIS lookup.
        --reputation-lookup   Activates or disables the usage of the reputation
                                dataset whether possible.
                                Configured value: False
        --reputation-lookup-only
                                Only perform a reputation lookup.
        --reputation          Activates or disables the reputation checker.
                                Configured value: False
        --syntax              Activates or disables the syntax checker.
                                Configured value: False
        -t LOOKUP__TIMEOUT, --timeout LOOKUP__TIMEOUT
                                Sets the default timeout to apply to each lookup
                                utilities every time it is possible to define a timeout.
                                Configured value: 5
        --max-http-retries MAX_HTTP_RETRIES
                                Sets the maximum number of retries for an HTTP request.
                                Configured value: 0
        -ua USER_AGENT__CUSTOM, --user-agent USER_AGENT__CUSTOM
                                Sets the user agent to use.

                                If not given, we try to get the latest (automatically) for you.
        -vsc, --verify-ssl-certificate
                                Activates or disables the verification of the SSL/TLS
                                certificate when testing for URL.
                                Configured value: False

    DNS control:
        --dns DNS__SERVER [DNS__SERVER ...]
                                Sets one or more (space separated) DNS server(s) to use during testing.

                                To specify a port number for the DNS server you append
                                it as :port [ip:port].

                                If no port is specified, the default DNS port (53) is used.
                                Configured value: <BoxList: ['1.1.1.1']>
        --dns-protocol {UDP,TCP,HTTPS,TLS}
                                Sets the protocol to use for the DNS queries.
                                Configured value: 'UDP'
        --follow-server-order
                                Let us follow or mix the order of usage of the given
                                or found DNS server(s).
                                Configured value: True
        --trust-dns-server    Activates or disable the trust mode.

                                When active, when the first read DNS server give us a negative
                                response - without error - we take it as it it.
                                Otherwise, if not active, when the first read DNS server give us
                                a negative response - without error - we still consolidate by
                                checking all given/found server.

                                Configured value: False
        --dns-delay DNS__DELAY
                                Sets the delay (in seconds) to apply between each DNS
                                queries.

                                Configured value: 0.0

    Proxy control:
        --http-proxy PROXY__GLOBAL__HTTP
                                Sets the proxy to use when testing subjects over HTTP.
                                Configured value: None
        --https-proxy PROXY__GLOBAL__HTTPS
                                Sets the proxy to use when testing subjects over HTTPS.
                                Configured value: None

    Databases:
        --inactive-db         Activates or disables the usage of a 'database' to
                                store all 'INACTIVE' and 'INVALID'  subject for continuous retest.
                                Configured value: False
        --database-type {csv,mariadb,mysql}
                                Sets the database engine to use.
                                You can choose between the following: `csv | mariadb | mysql`
                                Configured value: 'csv'
        -dbr CLI_TESTING__DAYS_BETWEEN__DB_RETEST, --days-between-db-retest CLI_TESTING__DAYS_BETWEEN__DB_RETEST
                                Sets the numbers of days since the introduction of
                                subject into the inactive dataset before it gets retested.
                                Configured value: 1
        -wdb, --whois-database
                                Activates or disables the usage of a 'database' to
                                store the expiration date of all domains with a valid
                                expiration date.
                                Configured value: True

    Output control:
        -a, --all             Activates or disables the display of the all
                                information in the table we print to stdout.
                                Configured value: False
        -ex, --execution      Activates or disables the display of the execution time.
                                Configured value: False
        --colour, --color     Activates or disables the coloration to STDOUT.
                                Configured value: True
        --display-status {all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} [{all,ACTIVE,INACTIVE,VALID,INVALID,MALICIOUS,SANE} ...]
                                Sets the status that we are allowed to print to STDOUT.

                                Multiple space separated statuses can be given.
                                Configured value: 'all'
        --dots                Activate or disables the display of dots or other
                                characters when we skip the test of a subject.
                                Configured value: False
        --hierarchical        Activates or disables the sorting of the files
                                content (output) in a hierarchical order.
                                Configured value: False
        -h, --host            Activates or disables the generation of the
                                hosts file(s).
                                Configured value: False
        -ip CLI_TESTING__HOSTS_IP, --hosts-ip CLI_TESTING__HOSTS_IP
                                Sets the IP to prefix each lines of the hosts file.
                                Configured value: '0.0.0.0'
        --merge-output        Activates or disables the merging of the outputs of all
                                inputted files inside a single subdirectory as opposed to the
                                normal behavior.
                                Configured value: False
        --no-files            Activates or disables the generation of any non-logs
                                file(s).
                                Configured value: False
        --output-location OUTPUT_LOCATION
                                Sets the location where we are supposed to generation
                                the output directory from.
                                Configured value: '/home/pyfunceble-dev/repositories/github/source/PyFunceble'
        --unified-results     Activates or disables the generation of the unified
                                results file instead of the divided ones.
                                Configured value: False
        --percentage          Activates or disables the display and generation
                                of the percentage - file - of each status.
                                Configured value: True
        --registrar           Activates or disables the display and generation
                                of the registrar - file - status at the end of a test.
                                The registrar file contains the top domain registrar found
                                while testing.
                                Configured value: True
        --max-registrar CLI_TESTING__DISPLAY_MODE__MAX_REGISTRAR
                                Sets the maximal number of registrar to display.
                                Note: This argument has no effect when the --registrar
                                argument is not set. This argument only takes effect on
                                display but not
                                in the log file
                                Configured value: 15
        --plain               Activates or disables the generation of the
                                RAW file(s). What is meant is a list with only a list of
                                subject (one per line).
                                Configured value: True
        -q, --quiet           Activates or disables the display of output to the
                                terminal.
                                Configured value: False
        --push-collection     Activates or disables the push of test result into the
                                collection API.
                                Configured value: False
        -s, --simple          Activates or disables the simple output mode.
                                Configured value: False

    Multiprocessing:
        -w CLI_TESTING__MAX_WORKERS, --max-workers CLI_TESTING__MAX_WORKERS
                                Sets the number of maximal workers to use.
                                If not given, 20 (based on the current machine) will be applied.
                                Configured value: None

    CI / CD:
        --ci-max-minutes CLI_TESTING__CI__MAX_EXEC_MINUTES
                                Sets the number of minutes to wait before starting
                                to stop a CI session.
                                Configured value: 15
        --ci                  Activates or disables the Continuous Integration
                                mechanism.
                                Configured value: False
        --ci-branch CLI_TESTING__CI__BRANCH
                                Sets our git working branch. This is the branch
                                from where we are supposed to store the tests
                                (excepts the final results).
                                Configured value: 'master'
        --ci-distribution-branch CLI_TESTING__CI__DISTRIBUTION_BRANCH
                                Sets our git distributions branch. This is the
                                branch from where we are supposed to store and push
                                the final results.
                                Configured value: 'master'
        --ci-command CLI_TESTING__CI__COMMAND
                                Sets the command to execute before each commit
                                (except the final one).
                                Configured value: None
        --ci-end-command CLI_TESTING__CI__END_COMMAND
                                Sets the command to execute before the final commit.
                                Configured value: None
        --ci-commit-message CLI_TESTING__CI__COMMIT_MESSAGE
                                Sets the commit message to apply every time we have
                                to apply a commit except for the really last one.
                                Configured value: 'PyFunceble - AutoSave'
        --ci-end-commit-message CLI_TESTING__CI__END_COMMIT_MESSAGE
                                Sets the commit message to apply at the really end.
                                Configured value: 'PyFunceble - Results'

    For an in-depth usage, explanation and examples of the arguments,
    you should read the documentation at https://pyfunceble.readthedocs.io/en/dev/

    Crafted with ♥ by Nissar Chababy (@funilrys) with the help of
    https://git.io/JkUPS && https://git.io/JkUPF

.. _RPZ: https://www.mypdns.org/w/rpz/
