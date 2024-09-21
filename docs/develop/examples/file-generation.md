# File Generation

Using the API is great, but how do we get the same file structure as the CLI ?

Here is an example that tries to demontrate how to achieve that.

```python linenums="1" title="Test and generate files using the API"
import copy

import colorama

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble import DomainAvailabilityChecker
from PyFunceble.cli.filesystem.dir_structure.restore import (
    DirectoryStructureRestoration,
)
from PyFunceble.cli.processes.producer import ProducerProcessesManager
from PyFunceble.cli.utils import ascii_logo

# We initiate the coloration.
colorama.init(autoreset=True)


# We are in control, so we need to manually start the loader.
PyFunceble.facility.ConfigLoader.custom_config = {
    "cli_testing": {
        "file_generation": {"plain": True},
        "display_mode": {"quiet": True, "color": True},
    }
}
PyFunceble.facility.ConfigLoader.start()

print(ascii_logo.get_home_representation())

# This is needed as our idea is to communicate with the producer process instead
# of trying to implement everything again.
# So, this describes the dataset as they are sent to the tester process
# (normally from the CLi).
STD_COMMUNICATION_DATASET = {
    "type": "single",
    "subject_type": "domain",
    # Destination inside the output directory.
    "destination": "my_awesome_pyfunceble_wrapper",
    "subject": None,
    "idna_subject": None,
    "source": "my_awesome_pyfunceble_wrapper",
    "output_dir": None,  # Will be handled automatically
    "checker_type": "AVAILABILITY",  # Must be one of our supported one!!
}

DOMAINS = ["github.com", "twitter.com", "www.аррӏе.com"]

# In this example, we are cleaning up and regenerating the output directory
# at each run.
#
# Note: the backup in question is the "dir_structure.json" file.
dir_structure_restoration = DirectoryStructureRestoration(
    parent_dirname=STD_COMMUNICATION_DATASET["destination"]
).restore_from_backup()

# We start the producer process.
producer_proc = ProducerProcessesManager()
# We start the process manager now that we are ready.
producer_proc.start()

# We start and configure our availability checker.
avail_checker = DomainAvailabilityChecker(use_whois_lookup=False)

for domain in DOMAINS:
    # We loop through our list of subject to test.

    # We parse the current subject to the availability checker.
    avail_checker.subject = domain

    # Now we fetch the status object.
    test_result = avail_checker.get_status()
    dict_result = test_result.to_dict()

    # We prepare our communication dataset.
    communication_dataset = copy.deepcopy(STD_COMMUNICATION_DATASET)
    communication_dataset = {
        key: dict_result.get(key, value) for key, value in communication_dataset.items()
    }

    # We print the result (for us as we call this script.)
    print(
        f"{test_result.subject} (IDNA: {test_result.idna_subject}) "
        f"is {test_result.status}"
    )

    # We order the generation of the status file by putting our information
    # to the producer queue.
    producer_proc.add_to_input_queue(
        (communication_dataset, test_result), worker_name="main"
    )

# We are now done, it's time to send the stop signal.
# The stop signal will inform the producer process that it needs to stop
# listening to new order (from the time it reads the stop signal).
producer_proc.send_stop_signal()

# Now we wait until it's done.
producer_proc.wait()

# From here all files were generated we can do whatever we want with them.
```