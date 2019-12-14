Using the PyFunceble (Python) API
---------------------------------

If you are working with a python script, module or even class,
you can integrate **PyFunceble** to your main logic by importing
it and using its API (cf: :ref:`api`).

This section will present some example of the way you can interact
with PyFunceble from anything written in Python.

Get the availability of domains or IP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This example can be found in `our examples repository`_.

.. todo::
    Add IPs in the loop.

::

    """
    This is an example which respond to the following problematic(s):

        * How can I get the avaibility of a domain or IP with PyFunceble ?
    """

    # We want some coloration so we import the tool do to that :)
    from PyFunceble import initiate_colorama, Fore, Style
    # We import the tool to print the colored CLI logo.
    from PyFunceble.cli_core import CLICore
    # We import the configuration loader.
    from PyFunceble import load_config
    # We import the test method of the PyFunceble API.
    from PyFunceble import test as PyFunceble

    # We initiate the list of domains we are going to test.
    DOMAINS = [
        "google.com",
        "tweeetttter.com",
        "github.com",
        "examplessss.ooooorgg",
        "twitter.com",
        "forest-jump"
    ]

    # We initiate colorama.
    initiate_colorama(True)

    # We load our configuration.
    #
    # Note: We need this to print the logo but if you
    # doesn't need the logo, you can ignore this.
    load_config(generate_directory_structure=False)

    # We print the PyFunceble logo.
    CLICore.colorify_logo(home=True)

    def print_result(subject, status):
        """
        Given the subject and its status, we print it to STDOUT.

        :param str subject: The subject we are going to print.
        :param str status: The status of the domain.
        """

        if status == "ACTIVE":
            print(f"{Fore.GREEN + Style.BRIGHT}{domain} is {status}")
        elif status == "INACTIVE":
            print(f"{Fore.RED + Style.BRIGHT}{domain} is {status}")
        else:
            print(f"{Fore.CYAN + Style.BRIGHT}{domain} is {status}")

    for domain in DOMAINS:
        # We loop through the list of domain.

        # And we print the domain and status with the right coloration!
        print_result(domain, PyFunceble(domain))

Get the availability of URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This example can be found in `our examples repository`_.

::

    """
    This is an example which respond to the following problematic(s):

        * How can I get the avaibility of an URL with PyFunceble ?
    """

    # We want some coloration so we import the tool do to that :)
    from PyFunceble import initiate_colorama, Fore, Style
    # We import the tool to print the colored CLI logo.
    from PyFunceble.cli_core import CLICore
    # We import the configuration loader.
    from PyFunceble import load_config
    # We import the test method of the PyFunceble API.
    from PyFunceble import url_test as PyFunceble

    # We initiate the list of URLs we are going to test.
    URLS = [
        "https://google.com",
        "http://tweeetttter.com",
        "ftp://github.com",
        "http://examplessss.ooooorgg",
        "http://twitter.com",
    ]

    # We initiate colorama.
    initiate_colorama(True)

    # We load our configuration.
    #
    # Note: We need this to print the logo but if you
    # doesn't need the logo, you can ignore this.
    load_config(generate_directory_structure=False)

    # We print the PyFunceble logo.
    CLICore.colorify_logo(home=True)

    def print_result(subject, status):
        """
        Given the subject and its status, we print it to STDOUT.

        :param str subject: The subject we are going to print.
        :param str status: The status of the domain.
        """

        if status == "ACTIVE":
            print(f"{Fore.GREEN + Style.BRIGHT}{domain} is {status}")
        elif status == "INACTIVE":
            print(f"{Fore.RED + Style.BRIGHT}{domain} is {status}")
        else:
            print(f"{Fore.CYAN + Style.BRIGHT}{domain} is {status}")

    for url in URLS:
        # We loop through the list of domain.

        # And we print the domain and status with the right coloration!
        print_result(url, PyFunceble(url))

Complete dataset while getting the avaibility of domains, IPs or URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While using our API, you can request to see/get everything with the help of the :code:`complete=True` argument.

You'll then get the following :code:`dict` as output.


::

    {
        "_status": None, # If some extra rules are applied, this index will keep the status before the extra rules was applied.
        "_status_source": None, # If some extra rules are applied, this index will keep the source before the extra rules was applied.
        "domain_syntax_validation": None, # The domain syntax validation status.
        "expiration_date": None, # The expiration date of the tested subject (if found).
        "http_status_code": None, # The status code of the tested subejct.
        "ip4_syntax_validation": None, # The IPv4 syntax validation status.
        "dns_lookup": [], # The DNS Lookup output.
        "status_source": None, # The (final) source which gave us the status.
        "status": None, # The (final) status returned by PyFunceble.
        "tested": None, # The tested subject.
        "url_syntax_validation": None, # The url syntax validation status.
        "whois_record": None, # The whois record (if found).
        "whois_server": None, # The whois server we use to get the whois record (if found).
    }

Set custom configuration index while getting the avaibility of domains, IPs or URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While using PyFunceble, you might want to set or overwritte a default behaviour.

You can do that in 2 ways. Globally or locally.

Globally
^^^^^^^^

To set globally simply initiate the configuration loader and parse your custom configuration along with
the initialization.

As example, you can do it like follow:

::

    # We import the configuration loader.
    from PyFunceble import load_config

    # We set our list of indexes to overwritte.
    OUR_PYFUNCEBLE_CONFIG = {"share_logs":False, "no_files": True}

    # We load our configuration and parse our custom indexes.
    load_config(generate_directory_structure=False, custom=OUR_PYFUNCEBLE_CONFIG)

    ## We can then play with PyFunceble and/or other business logic ...

Locally
"""""""

To set globally simply parse your configuration along with the test method.

As example, you can do it like follow:

::

    # We import the test method.
    from PyFunceble import test as AvailabilityTest

    # We set our list of indexes to overwritte.
    OUR_PYFUNCEBLE_CONFIG = {"share_logs":False, "no_files": True}

    # We get the status and parse our configuration.
    status = AvailabilityTest("hello.world", config=OUR_PYFUNCEBLE_CONFIG)

    ## We can then manipulate the status and/or other business logic ...


Check the syntax of domains
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This example can be found in `our examples repository`_.

::

    """
    This is an example which respond to the following problematic(s):

        * How can I check the syntax of a domain with PyFunceble ?
    """

    # We want some coloration so we import the tool do to that :)
    from PyFunceble import initiate_colorama, Fore, Style
    # We import the tool to print the colored CLI logo.
    from PyFunceble.cli_core import CLICore
    # We import the configuration loader.
    from PyFunceble import load_config
    # We import the test method of the PyFunceble API.
    from PyFunceble import is_domain as PyFunceble

    # We initiate the list of domains we are going to test.
    DOMAINS = [
        "google.com",
        "tweeetttter.com",
        "github.com",
        "examplessss.ooooorgg",
        "twitter.com",
        "forest-jump",
    ]


    # We initiate colorama.
    initiate_colorama(True)

    # We load our configuration.
    #
    # Note: We need this to print the logo but if you
    # doesn't need the logo, you can ignore this.
    load_config(generate_directory_structure=False)

    # We print the PyFunceble logo.
    CLICore.colorify_logo(home=True)

    def print_syntax_result(subject, status):
        """
        Given the subject and its validation, we print it to STDOUT.

        :param str subject: The subject we are going to print.
        :param bool status: The validation state.
        """

        if status is True:
            print(f"{Fore.GREEN + Style.BRIGHT}{subject} is VALID")
        else:
            print(f"{Fore.CYAN + Style.BRIGHT}{subject} is INVALID")

    for domain in DOMAINS:
        # We loop through the list of domain.

        # And we print the domain and status with the right coloration!
        print_syntax_result(domain, PyFunceble(domain))


Check the syntax of IPv4s
^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This example can be found in `our examples repository`_.

::

    """
    This is an example which respond to the following problematic(s):

        * How can I check the syntax of an IPv4/IPv6 with PyFunceble ?
    """

    # We want some coloration so we import the tool do to that :)
    from PyFunceble import initiate_colorama, Fore, Style
    # We import the tool to print the colored CLI logo.
    from PyFunceble.cli_core import CLICore
    # We import the configuration loader.
    from PyFunceble import load_config
    # We import the test method of the PyFunceble API.
    from PyFunceble import is_ip as PyFunceble

    # We initiate the list of IPs we are going to test.
    IPS = ["216.58.207.46", "257.58.207.46"]


    # We initiate colorama.
    initiate_colorama(True)

    # We load our configuration.
    #
    # Note: We need this to print the logo but if you
    # doesn't need the logo, you can ignore this.
    load_config(generate_directory_structure=False)

    # We print the PyFunceble logo.
    CLICore.colorify_logo(home=True)

    def print_syntax_result(subject, status):
        """
        Given the subject and its validation, we print it to STDOUT.

        :param str subject: The subject we are going to print.
        :param bool status: The validation state.
        """

        if status is True:
            print(f"{Fore.GREEN + Style.BRIGHT}{subject} is VALID")
        else:
            print(f"{Fore.CYAN + Style.BRIGHT}{subject} is INVALID")

    for ip in IPS:
        # We loop through the list of IP.

        # And we print the IP and status with the right coloration!
        print_syntax_result(ip, PyFunceble(ip))

Check the syntax of URLs
^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This example can be found in `our examples repository`_.

::

    """
    This is an example which respond to the following problematic(s):

        * How can I check the syntax of an URL with PyFunceble ?
    """

    # We want some coloration so we import the tool do to that :)
    from PyFunceble import initiate_colorama, Fore, Style
    # We import the tool to print the colored CLI logo.
    from PyFunceble.cli_core import CLICore
    # We import the configuration loader.
    from PyFunceble import load_config
    # We import the test method of the PyFunceble API.
    from PyFunceble import is_url as PyFunceble

    # We initiate the list of URLs we are going to test.
    URLS = [
        "https://google.com",
        "http://tweeetttter.com",
        "htp://github.com",
        "httpp://examplessss.ooooorgg",
        "https:///twitter.com",
        "http:forest-jump",
    ]


    # We initiate colorama.
    initiate_colorama(True)

    # We load our configuration.
    #
    # Note: We need this to print the logo but if you
    # doesn't need the logo, you can ignore this.
    load_config(generate_directory_structure=False)

    # We print the PyFunceble logo.
    CLICore.colorify_logo(home=True)

    def print_syntax_result(subject, status):
        """
        Given the subject and its validation, we print it to STDOUT.

        :param str subject: The subject we are going to print.
        :param bool status: The validation state.
        """

        if status is True:
            print(f"{Fore.GREEN + Style.BRIGHT}{subject} is VALID")
        else:
            print(f"{Fore.CYAN + Style.BRIGHT}{subject} is INVALID")

    for url in URLS:
        # We loop through the list of URL.

        # And we print the URL and status with the right coloration!
        print_syntax_result(url, PyFunceble(url))



.. _`our examples repository`: https://github.com/PyFunceble/examples