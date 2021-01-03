"""
This is an example about how we can update the configuration while developping on top
of PyFunceble.
"""

import PyFunceble.facility
from PyFunceble import DomainAvailabilityChecker

# We preset the indexes (from .PyFunceble.yaml) that we want to update.
CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET = {
    "lookup": {"whois": False, "dns": False},
    "cli_testing": {"db_type": "csv"},
}

# We parse our custom indexes to PyFunceble before starting to use it.
PyFunceble.facility.ConfigLoader.start()
PyFunceble.facility.ConfigLoader.custom_config = CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET

# From now, each call of test so in this example PyFuncebleTest,
# will not try to get/request the WHOIS record.

DOMAINS = ["google.com", "github.com"]

print("Start with global custom configuration.")
for DOMAIN in DOMAINS:
    # This should return None.
    print(DOMAIN, DomainAvailabilityChecker(DOMAIN).get_status().whois_record)
print("End with global custom configuration.\n")

print("Start with local setting.")
for DOMAIN in DOMAINS:
    print(f"Start of WHOIS record of {DOMAIN} \n")

    # This part should return the WHOIS record.

    # This will - at each call we manually overwrite the configurated value.
    print(
        DOMAIN,
        DomainAvailabilityChecker(DOMAIN, use_whois_lookup=True)
        .get_status()
        .whois_record,
    )

    print(f"End of WHOIS record of {DOMAIN} \n")
print("End with local setting.")
