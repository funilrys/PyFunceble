"""
This is a basic example which prints one of the availability of
the given domain and URL.

.. note:
    Official output: ACTIVE, INACTIVE, INVALID
"""

from PyFunceble import DomainAndIPAvailabilityChecker, URLAvailabilityChecker

print("Start of basic example.")
DOMAIN = "github.com"
URL = f"https://{DOMAIN}"

print(DOMAIN, DomainAndIPAvailabilityChecker(DOMAIN).get_status().status)
print(URL, URLAvailabilityChecker(URL).get_status().status)
print("End of basic example ")
