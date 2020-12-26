"""
This is an example which let us manipulate the data and also generate the files
as if it was the CLI.
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
from PyFunceble.cli.threads.file_producer import FileProducerThread

# We initiate the coloration.
colorama.init(autoreset=True)

# We are in control, so we need to manually start the loading.
PyFunceble.facility.ConfigLoader.custom_config = {
    "cli_testing": {"file_generation": {"plain": True}, "display_mode": {"quiet": True}}
}
PyFunceble.facility.ConfigLoader.start()


# This is needed as our idea is to communicate with the producer thread instead
# of trying to reimplement everything.
# So, this describes the dataset as they are sent to the tester thread (normally)
STD_COMMUNICATION_DATASET = {
    "type": "single",
    "subject_type": "domain",
    # Destination inside the output directory.
    "destination": "my_awesome_pyfunceble_wrapper",
    "subject": None,
    "idna_subject": None,
    "source": "my_awesome_pyfunceble_wrapper",
    "output_dir": None,  # Will be handled autom
    "checker_type": "AVAILABILITY",  # Must be one of our supported one!!
}

DOMAINS = ["github.com", "twitter.com"]

# In this example, we are cleaning up and regenerating the output directory
# at each run.
dir_structure_restoration = DirectoryStructureRestoration(
    parent_dirname=STD_COMMUNICATION_DATASET["destination"]
).restore_from_backup()

# We start the producer thread.
file_producer_thread = FileProducerThread()
file_producer_thread.start()

# We start and configure our availability checker.
avail_checker = DomainAvailabilityChecker(use_whois_lookup=False)

for domain in DOMAINS:
    # We loop through our list of subject to test.

    # We parse the current subject to the availability checker.
    avail_checker.subject = domain

    # Now we fetch the status object.
    test_result = avail_checker.get_status()

    # We prepare our communication dataset.
    communication_dataset = copy.deepcopy(STD_COMMUNICATION_DATASET)
    communication_dataset["subject"] = test_result.subject
    communication_dataset["idna_subject"] = test_result.idna_subject

    # We print the result (for us as we call this script.)
    print(
        f"{test_result.idna_subject} (IDNA: {test_result.subject}) "
        f"is {test_result.status}"
    )

    # We order the generation of the status file by putting our information
    # to the producer queue.
    file_producer_thread.add_to_the_queue((communication_dataset, test_result))

# We are now done, it's time to send the stop signal.
# The stop signal will inform thhe producer thread that it needs to stop
# listening to new order (from the time it reads the stop signal).
file_producer_thread.send_stop_signal()

# Now we wait until it's done.
file_producer_thread.wait()

# From here all files were generated we can do whatever we want with them.

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
