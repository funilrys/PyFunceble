"""
This is an example which checks that the test with the reputation data is correct.
"""

import colorama

from PyFunceble import DomainAndIPReputationChecker
from PyFunceble.dataset.ipv4_reputation import IPV4ReputationDataset

colorama.init(autoreset=True)


reputation_checker = DomainAndIPReputationChecker()
reputation_dataset = IPV4ReputationDataset().get_content()

LIMIT = 10
MALICIOUS_SUBJECTS = [
    next(reputation_dataset).split("#", 1)[0] for _ in range(LIMIT + 1)
]

SANE_SUBJECTS = ["twitter.com", "google.com", "github.com"]


for subject in MALICIOUS_SUBJECTS:
    reputation_checker.subject = subject
    status = reputation_checker.get_status()

    if not status.is_malicious():
        raise RuntimeError(f"Something is wrong with {subject}.")
    print(f"{subject} is {status.status}")

for subject in SANE_SUBJECTS:
    reputation_checker.subject = subject
    status = reputation_checker.get_status()

    if not status.is_sane():

        raise RuntimeError(
            f"Something is wrong with {subject}. Dataset:\n{status.to_json()}"
        )
    print(f"{subject} is {status.status}")
