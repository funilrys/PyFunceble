"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to sort the content of
all interesting files.

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

import concurrent
import contextlib
import heapq
import os
import secrets
import tempfile
from typing import List

import PyFunceble.checker.utils.whois
import PyFunceble.cli.utils.sort
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.threads.base import ThreadsBase
from PyFunceble.cli.threads.utils import wait_until_completion
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.list import ListHelper


class FileSorterThread(ThreadsBase):
    """
    Provides our file sorter thread logic.
    The main idea is that we start read the given protocol and sort all the
    files that needs to be sorted.
    """

    MAX_LINES: int = 1000

    thread_name: str = "pyfunceble_file_sorter"

    @staticmethod
    def get_files_to_sort_content(output_dir: str) -> List[str]:
        """
        Provides the list  of files to work with.
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

    def process_sorting(self, file: str) -> None:
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
                            .custom_sort(
                                key_method=PyFunceble.cli.utils.sort.get_best_sorting_key()
                            )
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

    def target(self) -> None:
        """
        This is our core logic. Everything starts here!
        """

        stop_message_caught = False

        while True:
            if self.the_queue.empty():
                continue

            consumed = self.the_queue.get()

            PyFunceble.facility.Logger.info("Got: %r", consumed)

            if consumed == "stop":
                PyFunceble.facility.Logger.info(
                    "Got stop message. Stopping reading from the queue."
                )
                stop_message_caught = True
                break

            if not isinstance(consumed, dict) and "destination" not in consumed:
                continue

            output_dir = FilesystemDirBase(consumed["destination"]).get_output_basedir()
            files_to_sort = self.get_files_to_sort_content(output_dir)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
                thread_name_prefix=self.thread_name,
            ) as executor:
                submitted_list = []

                for file in files_to_sort:
                    submitted = executor.submit(self.process_sorting, file)
                    submitted_list.append(submitted)

            wait_until_completion(submitted_list, raise_exc=True)

        if stop_message_caught:
            self.add_to_output_queue("stop")
