"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our file sorter worker. This is the description of a file sorter worker.

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

import contextlib
import heapq
import os
import secrets
import tempfile
from typing import Any, List, Optional, Tuple

import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.processes.workers.base import WorkerBase
from PyFunceble.cli.utils.sort import get_best_sorting_key
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.list import ListHelper


class FileSorterWorker(WorkerBase):
    """
    Provides our file sorter worker. The objective of this worker is to provides
    a single worker (or process if you prefer) which will be used to handle
    the sorting of the content of all generated files.
    """

    STD_NAME: str = "pyfunceble_file_sorter_worker"
    MAX_LINES: int = 1000

    def __post_init__(self) -> None:
        # We don't need to wait for anything here :-)
        self.accept_waiting_delay = False

        return super().__post_init__()

    @staticmethod
    def get_files_to_sort(output_dir: str) -> List[str]:
        """
        Provides the list of files to sort.

        :param output_dir:
            The directory to start from.
        """

        dirs_to_ignore = [
            os.path.join(
                output_dir,
                PyFunceble.cli.storage.OUTPUTS.logs.directories.parent,
            ),
            os.path.join(output_dir, PyFunceble.cli.storage.OUTPUTS.splitted.directory),
        ]

        files_to_ignore = [".gitignore", ".gitkeep", ".running", "counter.json"]

        result = []

        for root, _, files in os.walk(output_dir):
            if any(x in root for x in dirs_to_ignore):
                continue

            for file in files:
                if file in files_to_ignore:
                    continue

                result.append(os.path.join(root, file))

        PyFunceble.facility.Logger.debug("List of files to sort:\n%r.", result)

        return result

    def process_file_sorting(self, file: str) -> None:
        """
        Process the sorting of the given file.

        The idea is to split the file piece by piece and at the end join all
        sorted files. For that job, we create a temporary directory which will
        store the temporary files.
        """

        temp_directory = tempfile.TemporaryDirectory()
        file_helper = FileHelper(file)

        with file_helper.open("r", encoding="utf-8") as file_stream:
            PyFunceble.facility.Logger.info("Started sort of %r.", file_helper.path)

            to_sort = []
            file_finished = False

            while True:
                for _ in range(self.MAX_LINES + 1):
                    try:
                        next_line = next(file_stream).strip()
                    except StopIteration:
                        file_finished = True
                        break

                    if next_line and not next_line.startswith("#"):
                        to_sort.append(next_line)

                with FileHelper(
                    os.path.join(temp_directory.name, secrets.token_hex(6))
                ).open("w", encoding="utf-8") as temp_file_stream:
                    # pylint: disable=line-too-long
                    temp_file_stream.write(
                        "\n".join(
                            ListHelper(to_sort)
                            .remove_duplicates()
                            .custom_sort(key_method=get_best_sorting_key())
                            .subject
                        )
                    )

                if file_finished:
                    break

            with contextlib.ExitStack() as stack:
                sorted_files = []

                for root_temp_dir, _, new_files in os.walk(temp_directory.name):
                    sorted_files = [
                        stack.enter_context(open(os.path.join(root_temp_dir, x)))
                        for x in new_files
                    ]

                if sorted_files:
                    with file_helper.open("w", encoding="utf-8") as final_file_stream:
                        final_file_stream.write(FilePrinter.STD_FILE_GENERATION)
                        final_file_stream.write(FilePrinter.get_generation_date_line())
                        final_file_stream.write("\n\n")
                        final_file_stream.writelines(heapq.merge(*sorted_files))

            PyFunceble.facility.Logger.info("Finished sort of %r.", file_helper.path)

        temp_directory.cleanup()

    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        if not isinstance(consumed, dict) and "destination" not in consumed:
            PyFunceble.facility.Logger.info(
                "Ignoring consumed data because no " "data to work with."
            )

            return None

        # Just for human brain :-)
        output_dir = FilesystemDirBase(consumed["destination"]).get_output_basedir()

        files_to_sort = self.get_files_to_sort(output_dir)

        for file in files_to_sort:
            self.process_file_sorting(file)

        return None
