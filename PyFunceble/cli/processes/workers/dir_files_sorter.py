"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our directory files sorter worker. This is the description of a
single directory file sorter worker.


Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import concurrent.futures
import os
from typing import Any, List, Optional, Tuple

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.processes.workers.file_sorter_base import FileSorterWorkerBase


class DireFileSorterWorker(FileSorterWorkerBase):
    """
    Provides our directory files sorter worker. The objective of this worker is
    to provides a single worker (or process if you prefer) which will be used
    to handle the sorting of the content of a submitted directory.

    Expected (input) message:

    ::

        {
            "directory": str,
            "remove_duplicates": bool,
            "write_header": bool
        }

    Expected (output) message:

    ::

        None
    """

    STD_NAME: str = "pyfunceble_dir_files_sorter_worker"

    @staticmethod
    def get_files_to_sort(directory: str) -> List[str]:
        """
        Provides the list of files to sort.

        :param directory:
            The directory to start from.
        """

        dirs_to_ignore = [
            os.path.join(
                directory,
                PyFunceble.cli.storage.OUTPUTS.logs.directories.parent,
            ),
            os.path.join(directory, PyFunceble.cli.storage.OUTPUTS.splitted.directory),
        ]

        files_to_ignore = [
            ".gitignore",
            ".gitkeep",
            PyFunceble.cli.storage.TEST_RUNNING_FILE,
            PyFunceble.cli.storage.COUNTER_FILE,
            PyFunceble.cli.storage.PRE_LOADER_FILE,
        ]

        result = []

        for root, _, files in os.walk(directory):
            if any(x in root for x in dirs_to_ignore):
                continue

            for file in files:
                if file in files_to_ignore:
                    continue

                result.append(os.path.join(root, file))

        PyFunceble.facility.Logger.debug("List of files to sort:\n%r.", result)

        return result

    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        if (
            not isinstance(consumed, dict)
            and "directory" not in consumed
            or not consumed["directory"]
        ):
            PyFunceble.facility.Logger.info(
                "Ignoring consumed data because no " "data to work with."
            )

            return None

        # Just for human brain :-)
        directory = consumed["directory"]

        if "remove_duplicates" in consumed:
            remove_duplicates = consumed["remove_duplicates"]
        else:
            remove_duplicates = True

        if "write_header" in consumed:
            write_header = consumed["write_header"]
        else:
            write_header = True

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
        ) as executor:
            submitted_list = []

            for file in self.get_files_to_sort(directory):
                submitted = executor.submit(
                    self.process_file_sorting, file, remove_duplicates, write_header
                )
                submitted_list.append(submitted)

            for submitted in concurrent.futures.as_completed(submitted_list):
                # Ensure that everything is finished

                if submitted.exception():
                    raise submitted.exception()

        return None
