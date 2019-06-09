"""
This is a loop example which tests a list of domain and processes some action
    according to one of the official output of PyFunceble.

Note:
* Official output: ACTIVE, INACTIVE, INVALID
* You should always use PyFunceble().test() as it's the method which is especially
    suited for `__name__ != '__main__'` usage.
"""
from PyFunceble import load_config
from PyFunceble import test as PyFunceble
from PyFunceble import url_test as PyFuncebleURL

load_config(custom={"db_type": "json"})

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


print("Start of loop example.")
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
print("End of loop example.")
