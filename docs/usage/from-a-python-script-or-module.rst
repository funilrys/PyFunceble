From a Python script or module
------------------------------

Before continuing reading this part, You should know that I consider that you can speak in Python. If it's not the case, well, it's the time to `learn Python`_!

As **PyFunceble** is written in Python, it can be easily imported and used inside a script. This part will represent a basic example of usage.

Basic example
"""""""""""""

::


    """
    This is a basic example which prints one of the official output of PyFunceble.

    Note:
    * Official output: ACTIVE, INACTIVE, INVALID
    """

    from PyFunceble import test as PyFunceble
    from PyFunceble import url_test as PyFuncebleURL

    print(PyFunceble(domain='google.com'))
    print(PyFuncebleURL(url='https://google.com'))

.. _learn Python: http://www.learnpython.org/

Loop example
""""""""""""

This part is unnecessary but we wanted to document it!!

::

    """
    This is a loop example which tests a list of domain and processes some action
        according to one of the official output of PyFunceble.

    Note:
    * Official output: ACTIVE, INACTIVE, INVALID
    * You should always use PyFunceble().test() as it's the method which is specially
        suited for `__name__ != '__main__'` usage.
    """
    from PyFunceble import test as PyFunceble
    from PyFunceble import url_test as PyFuncebleURL

    DOMAINS = [
        'twitter.com',
        'google.com',
        'github.com',
        'github.comcomcom',
        'funilrys.co']


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
        print('%s is %s and %s is %s' % (domain, domain_status(domain), 'http://' + domain, url_status('http://' + domain)))

Advanced example
""""""""""""""""

**PyFunceble** now allow you to get the following information as dictionnary. 
The objective behind this feature is to let you know more about the element you are testing.

::

    {
        "tested": None, # The tested element.
        "expiration_date": None, # The expiration_date of the element if found.
        "domain_syntax_validation": None, # The domain syntax validation status.
        "http_status_code": None, # The status code of the tested element.
        "ip4_syntax_validation": None, # The IPv4 syntax validation status.
        "nslookup": [], # A list of IP of the tested element.
        "status": None, # The status matched by PyFunceble.
        "url_syntax_validation": None, # The url syntax validation status.
        "whois_server": None, # The whois server if found.
        "whois_record": None, # The whois record if whois_server is found. 
    }

To get those information simply work with our interface like follow :)

::

    """
    This is an advanced example which prints some information about the tested element.

    Note:
    * Official output: ACTIVE, INACTIVE, INVALID
    """

    from PyFunceble import test as PyFunceble
    from PyFunceble import url_test as PyFuncebleURL

    domain_testing = PyFunceble(domain='google.com', complete=True)
    url_testing = PyFuncebleURL(url='https://google.com', complete=True)

    print(domain_testing['nslookup'])
    print(domain_testing['domain_syntax_validation'])
    print(domain_testing['domain'], domain_testing['status'])

    print(url_testing['nslookup'])
    print(url_testing['domain_syntax_validation'])
    print(url_testing['domain'], domain_testing['status'])
