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
    :ivar bool domain_syntax_validation:
        The domain syntax validation status.
    :ivar list, None dns_lookup:
        The DNS lookup status.
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

    resulting_indexes = [
        "_status_source",
        "_status",
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
        "whois_server",
        "whois_record",
    ]

    def __init__(self, subject):
        self.subject = subject
        self.checker = PyFunceble.Check(self.subject)

        pre_loading = {
            "_status_source": None,
            "_status": None,
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
            "whois_server": PyFunceble.lookup.Referer(self.subject).get(),
            "whois_record": None,
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
