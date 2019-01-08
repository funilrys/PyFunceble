"""
This is a basic example which prints one of the official output of PyFunceble.

Note:
* Official output: ACTIVE, INACTIVE, INVALID
"""

from PyFunceble import test as PyFunceble
from PyFunceble import url_test as PyFuncebleURL

print("Start of basic example.")
DOMAIN = "github.com"
URL = "https://{}".format(DOMAIN)

print(DOMAIN, PyFunceble(domain=DOMAIN))
print(URL, PyFuncebleURL(url=URL))
print("End of basic example ")
