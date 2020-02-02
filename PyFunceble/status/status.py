"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the status interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import PyFunceble


# pylint: disable=too-many-instance-attributes
class Status:
    """
    The status object.

    Provides the result of one of the status gatherer.

    :param str subject:
        The subject which we describe.

    :ivar str _status_source:
        The status source before the application
        of our extra rules (if activated).
    :ivar str _status:
        The status before the application of our
        extra rules (if activated).
    :ivar list dns_lookup:
        The result of the DNS Lookup logic.
    :ivar bool domain_syntax_validation:
        The domain syntax validation status.
    :ivar str expiration_date:
        The expiration date of the subject.
    :ivar str http_status_code:
        The HTTP status code of the subject.
    :ivar bool ipv4_range_syntax_validation:
        The IPv4 range validation status.
    :ivar bool ipv4_syntax_validation:
        The IPv4 syntax validation status.
    :ivar bool ipv6_range_syntax_validation:
        The IPv6 range validation status.
    :ivar bool ipv6_syntax_validation:
        The IPv6 syntax validation status.
    :ivar str status_source:
        The final status source.
    :ivar str status:
        The final status.
    :ivar bool subdomain_syntax_validation:
        The subdomain syntax validation status.
    :ivar str tested:
        The tested subject.
    :ivar bool url_syntax_validation:
        The URL syntax validation status.
    :ivar str whois_server:
        The WHOIS server we contact-ed to get
        the WHOIS record.
    :ivar str whois_record:
        The WHOIS record.
    """

    # pylint: disable=no-member, attribute-defined-outside-init

    resulting_indexes = [
        "_status_source",
        "_status",
        "dns_lookup",
        "domain_syntax_validation",
        "expiration_date",
        "http_status_code",
        "ipv4_range_syntax_validation",
        "ipv4_syntax_validation",
        "ipv6_range_syntax_validation",
        "ipv6_syntax_validation",
        "status_source",
        "status",
        "subdomain_syntax_validation",
        "tested",
        "url_syntax_validation",
        "whois_record",
        "whois_server",
    ]

    def __init__(self, subject):
        self.subject = subject
        self.checker = PyFunceble.Check(self.subject)

        pre_loading = {
            "_status_source": None,
            "_status": None,
            "dns_lookup": None,
            "domain_syntax_validation": self.checker.is_domain(),
            "expiration_date": None,
            "http_status_code": PyFunceble.HTTP_CODE.not_found_default,
            "ipv4_range_syntax_validation": self.checker.is_ipv4_range(),
            "ipv4_syntax_validation": self.checker.is_ipv4(),
            "ipv6_range_syntax_validation": self.checker.is_ipv6_range(),
            "ipv6_syntax_validation": self.checker.is_ipv6(),
            "status_source": None,
            "status": None,
            "subdomain_syntax_validation": self.checker.is_subdomain(),
            "tested": self.subject,
            "url_syntax_validation": self.checker.is_url(),
            "whois_record": None,
            "whois_server": PyFunceble.lookup.Referer(self.subject).get()[-1],
        }

        for description, value in pre_loading.items():
            setattr(self, description, value)

    def __getitem__(self, index):
        return getattr(self, index)

    def __setitem__(self, index, value):
        setattr(self, index, value)

    def get(self):
        """
        Provides the status in a dict format.
        """

        return {x: y for x, y in self.__dict__.items() if x in self.resulting_indexes}
