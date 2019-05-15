"""
This is an advanced example which get more information about the tested element.
"""

from PyFunceble import test as PyFunceble
from PyFunceble import url_test as PyFuncebleURL

CONFIG = {"no_whois": True}
DOMAIN = "google.com"

DOMAIN_RESULT_FROM_API = PyFunceble(subject=DOMAIN, complete=True, config=CONFIG)
URL_RESULT_FROM_API = PyFuncebleURL(
    subject="https://{}".format(DOMAIN), complete=True, config=CONFIG
)

print("Start of information from API for {}.".format(DOMAIN))
print("dns_lookup", DOMAIN_RESULT_FROM_API["dns_lookup"])
print("domain_syntax_validation", DOMAIN_RESULT_FROM_API["domain_syntax_validation"])
print(DOMAIN_RESULT_FROM_API["tested"], DOMAIN_RESULT_FROM_API["status"])

print("dns_lookup", URL_RESULT_FROM_API["dns_lookup"])
print("domain_syntax_validation", URL_RESULT_FROM_API["domain_syntax_validation"])
print("url_syntax_validation", URL_RESULT_FROM_API["url_syntax_validation"])
print(URL_RESULT_FROM_API["tested"], DOMAIN_RESULT_FROM_API["status"])
print(f"End of information from API for {DOMAIN}.")
