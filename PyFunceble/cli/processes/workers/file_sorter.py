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

from typing import Any, Optional, Tuple

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.processes.workers.file_sorter_base import FileSorterWorkerBase


class FileSorterWorker(FileSorterWorkerBase):
    """
    Provides our file sorter worker. The objective of this worker is to provides
    a single worker (or process if you prefer) which will be used to handle
    the sorting of the content of a given file.

    Expected (input) message:

    ::

        {
            "file": str,
            "remove_duplicates": bool,
            "write_header": bool
        }

    Expected (output) message:

    ::

        None
    """

    STD_NAME: str = "pyfunceble_file_sorter_worker"

    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        if (
            not isinstance(consumed, dict)
            and "file" not in consumed
            or not consumed["file"]
        ):
            PyFunceble.facility.Logger.info(
                "Ignoring consumed data because no data to work with."
            )

            return None

        # Just for human brain :-)
        file = consumed["file"]

        if "remove_duplicates" in consumed:
            remove_duplicates = consumed["remove_duplicates"]
        else:
            remove_duplicates = True

        if "write_header" in consumed:
            write_header = consumed["write_header"]
        else:
            write_header = True

        self.process_file_sorting(
            file, remove_duplicates=remove_duplicates, write_header=write_header
        )

        return None
