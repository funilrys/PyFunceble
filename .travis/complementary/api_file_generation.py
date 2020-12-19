"""
This is an example which check that the file generation from the API is still
working.
"""

import copy
import os
import sys

import colorama

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble import DomainAvailabilityChecker
from PyFunceble.cli.filesystem.dir_structure.restore import (
    DirectoryStructureRestoration,
)
from PyFunceble.cli.threads.producer import ProducerThread

# We initiate the coloration.
colorama.init(autoreset=True)

# We are in control, so we need to manually start the loading.
PyFunceble.facility.ConfigLoader.custom_config = {
    "cli_testing": {"file_generation": {"plain": True}, "display_mode": {"quiet": True}}
}
PyFunceble.facility.ConfigLoader.start()


STD_COMMUNICATION_DATASET = {
    "type": "single",
    "subject_type": "domain",
    # Destination in the output directory.
    "destination": "my_awesome_pyfunceble_wrapper",
    "subject": None,
    "idna_subject": None,
    "source": "my_awesome_pyfunceble_wrapper",
    "output_dir": None,  # Will be handled autom
    "checker_type": "AVAILABILITY",  # Must be one of our supported one!!
}

DOMAINS = ["github.com", "twitter.com"]


dir_structure_restoration = DirectoryStructureRestoration(
    parent_dirname=STD_COMMUNICATION_DATASET["destination"]
).restore_from_backup()

producer_thread = ProducerThread()
producer_thread.start()

avail_checker = DomainAvailabilityChecker(use_whois_lookup=False)

for domain in DOMAINS:
    avail_checker.subject = domain
    test_result = avail_checker.get_status()
    communication_dataset = copy.deepcopy(STD_COMMUNICATION_DATASET)

    communication_dataset["subject"] = test_result.subject
    communication_dataset["idna_subject"] = test_result.idna_subject

    print(
        f"{test_result.idna_subject} (IDNA: {test_result.subject}) "
        f"is {test_result.status}"
    )

    producer_thread.add_to_the_queue((communication_dataset, test_result))

producer_thread.send_stop_signal()
producer_thread.wait()

if os.path.isfile(
    os.path.join(
        dir_structure_restoration.get_output_basedir(), "domains", "ACTIVE", "list"
    )
):
    print(
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}All right, "
        "files correctly generated!"
    )
    sys.exit(0)
else:
    print(
        f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Something went wrong, "
        "files not correctly generated!"
    )
    sys.exit(1)
