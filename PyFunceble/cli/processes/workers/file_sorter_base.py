"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our file sorter worker base. This is the base of all our file sorter.

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


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

import heapq
import os
import secrets
import tempfile
from io import TextIOWrapper
from itertools import islice
from typing import Any, Generator, List, Tuple

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.processes.workers.base import WorkerBase
from PyFunceble.cli.utils.sort import get_best_sorting_key
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.list import ListHelper


class FileSorterWorkerBase(WorkerBase):
    """
    Provides our the base of all our file sorters.
    """

    MAX_LINES: int = 32_000
    FILE_BUFFER_SIZE: int = 64 * 1024

    def __post_init__(self) -> None:
        # We don't need to wait for anything here :-)
        self.accept_waiting_delay = False

        return super().__post_init__()

    @classmethod
    def process_file_sorting(
        cls,
        file: str,
        remove_duplicates: bool = True,
        write_header: bool = True,
        sorting_key: Any = None,
    ) -> None:
        """
        Process the sorting of the given file.

        The idea is to split the file piece by piece and at the end join all
        sorted files. For that job, we create a temporary directory which will
        store the temporary files.

        :param file:
            The file to sort.
        :param remove_duplicates:
            Activates the deletion of duplicates.
        :param write_header:
            Activates the writing of the PyFunceble related header.

            .. warning::
                When this is set to :py:class:`True`, we assume that the header
                itself was already given. Meaning that the first 2 commented
                lines will be excluded from the sorting and regenerated.
        :param sorting_key:
            The sorting key to apply while sorting.

            This is the lambda/function that goes into the :code:`key` argument
            of the :py:class:`sorted` function.
        """

        # pylint: disable=too-many-locals,too-many-statements

        def merge_files(
            files: List[TextIOWrapper],
        ) -> Generator[Tuple[List[TextIOWrapper]], str, None]:
            """
            Merges the given files and yield each "lines" of the merged file.

            :param files:
                The files to merge.
            """

            result = []

            for index, file in enumerate(files):
                try:
                    iterator = iter(file)
                    value = next(iterator)

                    heapq.heappush(
                        result, ((sorting_key(value), index, value, iterator, file))
                    )
                except StopIteration:
                    file.close()

            previous = None
            comment_count = 0
            max_comment_count = 2

            while result:
                ignore = False

                _, index, value, iterator, file = heapq.heappop(result)

                if remove_duplicates and value == previous:
                    ignore = True

                if (
                    write_header
                    and comment_count < max_comment_count
                    and value[0] == "#"
                ):
                    ignore = True
                    max_comment_count += 1

                if not ignore:
                    yield value
                    previous = value

                try:
                    value = next(iterator)

                    heapq.heappush(
                        result, ((sorting_key(value), index, value, iterator, file))
                    )
                except StopIteration:
                    file.close()

        temp_directory = tempfile.TemporaryDirectory()
        temporary_output_file = os.path.join(temp_directory.name, secrets.token_hex(6))

        if not sorting_key:
            sorting_key = get_best_sorting_key()

        file_helper = FileHelper(file)

        sorted_files = []

        PyFunceble.facility.Logger.info("Started sort of %r.", file)

        with file_helper.open(
            "r", encoding="utf-8", buffering=cls.FILE_BUFFER_SIZE
        ) as file_stream:
            while True:
                to_sort = list(islice(file_stream, cls.MAX_LINES))

                if not to_sort:
                    break

                new_file = open(
                    os.path.join(temp_directory.name, secrets.token_hex(6)),
                    "w+",
                    encoding="utf-8",
                    buffering=cls.FILE_BUFFER_SIZE,
                )
                new_file.writelines(
                    ListHelper(to_sort)
                    .remove_duplicates()
                    .custom_sort(key_method=sorting_key)
                    .subject
                )
                new_file.flush()
                new_file.seek(0)
                sorted_files.append(new_file)

        with open(
            temporary_output_file, "w", cls.FILE_BUFFER_SIZE, encoding="utf-8"
        ) as file_stream:
            if write_header:
                file_stream.write(FilePrinter.STD_FILE_GENERATION)
                file_stream.write(FilePrinter.get_generation_date_line())
                file_stream.write("\n\n")

            file_stream.writelines(merge_files(sorted_files))

        FileHelper(temporary_output_file).move(file)

        PyFunceble.facility.Logger.info("Finished sort of %r.", file)

        temp_directory.cleanup()
