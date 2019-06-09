"""
This is an example about how we can update the configuration while developping on top
of PyFunceble.
"""
import PyFunceble
from PyFunceble import test as PyFuncebleTest

# We preset the indexes (from .PyFunceble.yaml) that we want to update.
CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET = {"no_whois": True, "db_type": "json"}

# We parse our custom indexes to PyFunceble before starting to use it.
PyFunceble.load_config(custom=CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET)

# From now, each call of test so in this example PyFuncebleTest,
# will not try to get/request the WHOIS record.

DOMAINS = ["google.com", "github.com"]

print("Start with global custom configuration.")
for DOMAIN in DOMAINS:
    # This should return None
    print(DOMAIN, PyFuncebleTest(subject=DOMAIN, complete=True)["whois_record"])
print("End with global custom configuration.\n")

print("Start with local custom configuration.")

# We update our index so that we can test/see how to parse it localy.
CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET["no_whois"] = False

for DOMAIN in DOMAINS:
    print("Start of WHOIS record of %s \n\n" % DOMAIN)

    # This part should return the WHOIS record.

    # This will - at each call of PyFuncebleTest or PyFuncebleURLTest on url testing -
    # update the configuration data with the one you give.
    print(
        PyFuncebleTest(
            subject=DOMAIN,
            complete=True,
            config=CUSTOM_CONFIGURATION_INDEX_VALUE_TO_SET,
        )["whois_record"]
    )
    print("\n\nEnd of WHOIS record of %s" % DOMAIN)
print("End with local custom configuration.")
