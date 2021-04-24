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
from PyFunceble.cli.processes.producer import ProducerProcessesManager
from PyFunceble.utils.platform import PlatformUtility

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


if __name__ == "__main__":
    # We initiate the coloration.
    colorama.init(autoreset=True)

    # We are in control, so we need to manually start the loading.
    PyFunceble.facility.ConfigLoader.custom_config = {
        "cli_testing": {
            "file_generation": {"plain": True},
            "display_mode": {"quiet": True},
        }
    }
    PyFunceble.facility.ConfigLoader.start()

    # In this example, we are cleaning up and regenerating the output directory
    # at each run.
    dir_structure_restoration = DirectoryStructureRestoration(
        parent_dirname=STD_COMMUNICATION_DATASET["destination"]
    ).restore_from_backup()

    # We start the producer thread.
    producer_process_manager = ProducerProcessesManager(
        max_worker=1, daemon=True, generate_output_queue=False
    )
    producer_process_manager.send_feeding_signal(worker_name="main")
    producer_process_manager.start()

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
        producer_process_manager.add_to_input_queue(
            (communication_dataset, test_result)
        )

    # We are now done, it's time to send the stop signal.
    # The stop signal will inform thhe producer thread that it needs to stop
    # listening to new order (from the time it reads the stop signal).
    producer_process_manager.send_stop_signal(worker_name="main")

    # Now we wait until it's done.
    producer_process_manager.wait()

    # From here all files were generated we can do whatever we want with them.

    unix_path = os.path.join(
        dir_structure_restoration.get_output_basedir(), "domains", "ACTIVE", "list"
    )

    win_path = f"{unix_path}.txt"

    path_to_use = unix_path if PlatformUtility.is_unix() else win_path

    if os.path.isfile(path_to_use):
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
