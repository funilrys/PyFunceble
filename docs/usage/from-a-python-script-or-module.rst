From a Python script or module
------------------------------

Before continuing reading this part, You should know that I consider that you can speak in Python. If it's not the case, well, it's the time to `learn Python`_!

As **PyFunceble** is written in Python, it can be easily imported and used inside a script or another module.

This section will present some examples.

Availability check of domains, IP or URL
""""""""""""""""""""""""""""""""""""""""

::

    """
    This is a basic example which prints one of the availability of
    the given domain and URL.

    .. note:
        Official output: ACTIVE, INACTIVE, INVALID
    """

    from PyFunceble import test as PyFunceble
    from PyFunceble import url_test as PyFuncebleURL

    DOMAIN, IP = ("github.com", "103.86.96.100")
    URL = "https://{}".format(DOMAIN)

    print(DOMAIN, PyFunceble(domain=DOMAIN))
    print(URL, PyFuncebleURL(url=URL))
    print(IP, PyFunceble(domain=IP))

Syntax check of domains, IP or URL
"""""""""""""""""""""""""""""""""""

::

    """
    This is a basic example which checks syntax of the given element.
    """

    from PyFunceble import syntax_check as PyFuncebleDomainSyntax
    from PyFunceble import url_syntax_check as PyFuncebleURLSyntax
    from PyFunceble import ipv4_syntax_check as PyFuncebleIPv4Syntax

    print("google.com", PyFuncebleDomainSyntax(domain="google.com"))
    print("https://google.com", PyFuncebleURLSyntax(url="https://google.com"))
    print("216.58.207.46", PyFuncebleIPv4Syntax(ip="216.58.207.46"))

    print("forest-jump", PyFuncebleDomainSyntax(domain="forest-jump"))
    print("https://forest-jump", PyFuncebleURLSyntax(url="https://forest-jump"))
    print("257.58.207.46", PyFuncebleIPv4Syntax(ip="257.58.207.46"))

IPv4 Range and subdomain syntax check
""""""""""""""""""""""""""""""""""""""

::

    """
    This is a basic example which checks syntax of the given element.
    """

    from PyFunceble import is_ipv4_range, is_subdomain

    print("hello.google.com", is_subdomain(domain="hello.google.com"))
    print("google.com", is_subdomain(domain="google.com"))

    print("192.168.0.0/24", is_ipv4_range(ip="192.168.0.0/24"))
    print("192.168.0.0", is_ipv4_range(ip="192.168.0.0"))


Loop example
""""""""""""

This part is unnecessary but we wanted to document it!!

::

    """
    This is a loop example which tests a list of domain and processes some action
        according to one of the official output of PyFunceble.

    ..note:
        * Official output: ACTIVE, INACTIVE, INVALID
        * You should always use PyFunceble().test() as it's the method which is especially
            suited for `__name__ != '__main__'` usage.
    """

    from PyFunceble import test as PyFunceble
    from PyFunceble import url_test as PyFuncebleURL

    DOMAINS = ["twitter.com", "google.com", "github.com", "github.comcomcom", "funilrys.co"]


    def domain_status(domain_or_ip):
        """
        Check the status of the given domain name or IP.

        Argument:
            - domain_or_ip: str
                The domain or IPv4 to test.

        Returns: str
            The status of the domain.
        """

        return PyFunceble(domain_or_ip)


    def url_status(url):
        """
        Check the status of the given url.

        Argument:
            - url: str
                The URL to test.

        Returns: str
            The status of the URL.
        """

        return PyFuncebleURL(url)


    for domain in DOMAINS:
        print(
            "%s is %s and %s is %s"
            % (
                domain,
                domain_status(domain),
                "http://" + domain,
                url_status("http://" + domain),
            )
        )

Advanced example
""""""""""""""""

**PyFunceble** allow you to get the following information as a dictionary.
The objective behind this feature is to let you know more about the element you are testing.

::

    {
        "_status": None, # If some extra rules are applied, this index will keep the status before the extra rules was applied.
        "_status_source": None, # If some extra rules are applied, this index will keep the source before the extra rules was applied.
        "domain_syntax_validation": None, # The domain syntax validation status.
        "expiration_date": None, # The expiration_date of the element if found.
        "http_status_code": None, # The status code of the tested element.
        "ip4_syntax_validation": None, # The IPv4 syntax validation status.
        "nslookup": [], # A list of IP of the tested element.
        "status_source": None, # The source which gives us the status.
        "status": None, # The status matched by PyFunceble.
        "tested": None, # The tested element.
        "url_syntax_validation": None, # The url syntax validation status.
        "whois_record": None, # The whois record if whois_server is found.
        "whois_server": None, # The whois server we use to get the whois record (if found).
    }

To get that information simply work with our interface like follow :)

::

    """
    This is an advanced example which get more information about the tested element.
    """


    from PyFunceble import test as PyFunceble
    from PyFunceble import url_test as PyFuncebleURL

    DOMAIN = "google.com"

    DOMAIN_RESULT_FROM_API = PyFunceble(domain=DOMAIN, complete=True)
    URL_RESULT_FROM_API = PyFuncebleURL(url="https://{}".format(DOMAIN), complete=True)

    print("nslookup", DOMAIN_RESULT_FROM_API["nslookup"])
    print("domain_syntax_validation", DOMAIN_RESULT_FROM_API["domain_syntax_validation"])
    print(DOMAIN_RESULT_FROM_API["tested"], DOMAIN_RESULT_FROM_API["status"])

    print("nslookup", URL_RESULT_FROM_API["nslookup"])
    print("domain_syntax_validation", URL_RESULT_FROM_API["domain_syntax_validation"])
    print("url_syntax_validation", URL_RESULT_FROM_API["url_syntax_validation"])
    print(URL_RESULT_FROM_API["tested"], DOMAIN_RESULT_FROM_API["status"])

Custom Configuration
""""""""""""""""""""

Sometime you may want to change **PyFunceble**'s configuration information from within your code.
Here are way to do it.

::

    """
    This is an example about how we can update the configuration while developping on top
    of PyFunceble.
    """
    import PyFunceble
    from PyFunceble import test as PyFuncebleTest

    # We preset the indexes (from .PyFunceble.yaml) that we want to update.
    CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET = {"no_whois": True}

    # We parse our custom indexes to PyFunceble before starting to use it.
    PyFunceble.load_config(custom=CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET)

    # From now, each call of test so in this example PyFuncebleTest,
    # will not try to get/request the WHOIS record.

    DOMAINS = ["google.com", "github.com"]

    print("Start with global custom configuration.")
    for DOMAIN in DOMAINS:
        # This should return None
        print(DOMAIN, PyFuncebleTest(domain=DOMAIN, complete=True)["whois_record"])
    print("End with global custom configuration.\n")

    print("Start with local custom configuration.")

    # We update our index so that we can test/see how to parse it localy.
    CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET["no_whois"] = False

    for DOMAIN in DOMAINS:
        print("Start of WHOIS record of %s \n\n" % DOMAIN)

        # This part should return the WHOIS record.

        # This will - at each call of PyFuncebleTest or PyFuncebleURLTest on url testing -
        # update the configuration data with the one you give.
        print(
            PyFuncebleTest(
                domain=DOMAIN, complete=True, config=CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET
            )["whois_record"]
        )
        print("\n\nEnd of WHOIS record of %s" % DOMAIN)
    print("End with local custom configuration.")

.. _learn Python: http://www.learnpython.org/