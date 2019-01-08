"""
This is an advanced example which prints some information about the tested element.

Note:
* Official output: ACTIVE, INACTIVE, INVALID
"""

from PyFunceble import test as PyFunceble
from PyFunceble import url_test as PyFuncebleURL

DOMAIN = "google.com"

DOMAIN_RESULT_FROM_API = PyFunceble(domain=DOMAIN, complete=True)
URL_RESULT_FROM_API = PyFuncebleURL(url="https://{}".format(DOMAIN), complete=True)

print("Start of information from API for {}.".format(DOMAIN))
print("nslookup", DOMAIN_RESULT_FROM_API["nslookup"])
print("domain_syntax_validation", DOMAIN_RESULT_FROM_API["domain_syntax_validation"])
print(DOMAIN_RESULT_FROM_API["tested"], DOMAIN_RESULT_FROM_API["status"])

print("nslookup", URL_RESULT_FROM_API["nslookup"])
print("domain_syntax_validation", URL_RESULT_FROM_API["domain_syntax_validation"])
print("url_syntax_validation", URL_RESULT_FROM_API["url_syntax_validation"])
print(URL_RESULT_FROM_API["tested"], DOMAIN_RESULT_FROM_API["status"])
print("End of information from API for {DOMAIN}.")
