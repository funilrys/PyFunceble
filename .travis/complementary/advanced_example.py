"""
This is an advanced example which get more information about the tested element.
"""

from json import dumps

from PyFunceble import test as PyFunceble
from PyFunceble import url_test as PyFuncebleURL

CONFIG = {"no_whois": True, "db_type": "json"}
SUBJECTS = ["google.com", "github.com", "example.org", "8.8.8.8", "8.4.4.8"]

for subject in SUBJECTS:
    output = PyFunceble(subject=subject, complete=True, config=CONFIG)
    url_output = PyFuncebleURL(
        subject="https://{}".format(subject), complete=True, config=CONFIG
    )

    print("============== COMPLETE DATA: {0} ==============".format(output["tested"]))

    print(dumps(output, indent=4, ensure_ascii=False, sort_keys=True))
    print(
        "=============================={0}===============".format(
            "=" * len(output["tested"])
        )
    )

    print(
        "============== COMPLETE DATA: {0} ==============".format(url_output["tested"])
    )

    print(dumps(output, indent=4, ensure_ascii=False, sort_keys=True))
    print(
        "=============================={0}===============".format(
            "=" * len(url_output["tested"])
        )
    )
