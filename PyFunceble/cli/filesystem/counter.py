"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to our counter tracker.

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

import copy
from typing import Dict, List, Union

import PyFunceble.cli.storage
import PyFunceble.cli.utils.testing
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.filesystem.json_base import FilesystemJSONBase


class FilesystemCounter(FilesystemJSONBase):
    """
    Provides our counter.
    """

    STD_DATASET: Dict[str, int] = {
        "counter": {
            PyFunceble.storage.STATUS.up: 0,
            PyFunceble.storage.STATUS.valid: 0,
            PyFunceble.storage.STATUS.sane: 0,
            PyFunceble.storage.STATUS.down: 0,
            PyFunceble.storage.STATUS.malicious: 0,
            PyFunceble.storage.STATUS.invalid: 0,
            "total": 0,
        },
        "percentage": {
            PyFunceble.storage.STATUS.up: 0,
            PyFunceble.storage.STATUS.valid: 0,
            PyFunceble.storage.STATUS.sane: 0,
            PyFunceble.storage.STATUS.down: 0,
            PyFunceble.storage.STATUS.malicious: 0,
            PyFunceble.storage.STATUS.invalid: 0,
            "total": 0,
        },
    }

    PERCENTAGE_STATUSES: Dict[str, List[str]] = {
        "SYNTAX": [
            PyFunceble.storage.STATUS.valid,
            PyFunceble.storage.STATUS.invalid,
        ],
        "REPUTATION": [
            PyFunceble.storage.STATUS.sane,
            PyFunceble.storage.STATUS.malicious,
        ],
        "AVAILABILITY": [
            PyFunceble.storage.STATUS.up,
            PyFunceble.storage.STATUS.down,
            PyFunceble.storage.STATUS.invalid,
        ],
    }

    SOURCE_FILE: str = PyFunceble.cli.storage.COUNTER_FILE

    @FilesystemJSONBase.fetch_dataset_beforehand
    def get_dataset_for_printer(self) -> List[Dict[str, Union[str, int]]]:
        """
        Provides the dataset that the printer may understand.

        :raise ValueError:
            When the current testing mode is not supported (yet?).
        """

        result = {}
        testing_mode = PyFunceble.cli.utils.testing.get_testing_mode()

        if testing_mode not in self.PERCENTAGE_STATUSES:
            raise ValueError("<testing_mode> ({testing_mode!r}) is not supported.")

        for status, value in self.dataset["counter"].items():
            if (
                status == "total"
                or status not in self.PERCENTAGE_STATUSES[testing_mode]
            ):
                continue

            result[status] = {"status": status, "amount": value}

        for status, value in self.dataset["percentage"].items():
            if (
                status == "total"
                or status not in self.PERCENTAGE_STATUSES[testing_mode]
            ):
                continue

            result[status]["percentage"] = f"{round(value)}%"

        # Apply the right order.
        return [result[x] for x in self.PERCENTAGE_STATUSES[testing_mode]]

    @FilesystemJSONBase.update_source_file_path_beforehand
    @FilesystemJSONBase.fetch_dataset_beforehand
    @FilesystemJSONBase.save_dataset_afterwards
    def count(self, status: CheckerStatusBase) -> "FilesystemCounter":
        """
        Starts the counting process.

        :param status:
            The status to count into our dataset.
        """

        if not isinstance(status, CheckerStatusBase):
            raise TypeError(
                f"<status> should be {CheckerStatusBase}, {type(status)} given."
            )

        if "counter" not in self.dataset:
            self.dataset = copy.deepcopy(self.STD_DATASET)

        self.dataset["counter"][status.status] += 1
        self.dataset["counter"]["total"] += 1

        self.dataset["percentage"][status.status] = (
            self.dataset["counter"][status.status] * 100
        ) / self.dataset["counter"]["total"]

        self.dataset["percentage"]["total"] = sum(
            y for x, y in self.dataset["percentage"].items() if x != "total"
        )

        return self
