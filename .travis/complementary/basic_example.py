"""
This is a basic example which prints one of the availability of
the given domain and URL.

.. note:
    Official output: ACTIVE, INACTIVE, INVALID
"""

from PyFunceble import load_config
from PyFunceble import test as PyFunceble
from PyFunceble import url_test as PyFuncebleURL

load_config(custom={"db_type": "json"})

print("Start of basic example.")
DOMAIN = "github.com"
URL = "https://{}".format(DOMAIN)

print(DOMAIN, PyFunceble(subject=DOMAIN))
print(URL, PyFuncebleURL(subject=URL))
print("End of basic example ")
