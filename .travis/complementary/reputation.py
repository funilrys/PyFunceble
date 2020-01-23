"""
This is an example which checks that the test with the reputation data is correct.
"""

import PyFunceble
import PyFunceble.cli

PyFunceble.cli.initiate_colorama(True)
PyFunceble.load_config(generate_directory_structure=False,)
PyFunceble.output.Clean()

LIMIT = 10
MALICIOUS_SUBJECTS = [
    x.split("#")[0]
    for x in PyFunceble.REQUESTS.get(
        PyFunceble.LINKS.ipv4_reputation
    ).text.splitlines()[:10]
]

SANE_SUBJECTS = ["twitter.com", "google.com", "github.com"]


for subject in MALICIOUS_SUBJECTS:
    data = PyFunceble.core.API(subject, complete=True).reputation("domain")

    if data["status"] != "MALICIOUS":
        raise Exception("Something is wrong.")
    print(f"{subject} is {data['status']}")

for subject in SANE_SUBJECTS:
    data = PyFunceble.core.API(subject, complete=True).reputation("domain")

    if data["status"] != "SANE":
        raise Exception("Something is wrong.")
    print(f"{subject} is {data['status']}")
