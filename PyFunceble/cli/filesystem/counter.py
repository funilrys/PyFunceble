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

import copy
import functools
import os
from typing import Dict, List, Optional, Union

import PyFunceble.cli.storage
import PyFunceble.cli.utils.testing
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper


class FilesystemCounter(FilesystemDirBase):
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

    dataset: Dict[str, int] = {}
    source_file: Optional[str] = None

    def update_source_file_beforehand(func):  # pylint: disable=no-self-argument
        """
        Updates the source file before launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.source_file = os.path.join(
                self.get_output_basedir(), PyFunceble.cli.storage.COUNTER_FILE
            )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def fetch_dataset_beforehand(func):  # pylint: disable=no-self-argument
        """
        Updates the dataset to work with before launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.fetch_dataset()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def save_dataset_afterwards(func):  # pylint: disable=no-self-argument
        """
        Saves the dataset after launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.save_dataset()

            return result

        return wrapper

    @update_source_file_beforehand
    def fetch_dataset(self) -> "FilesystemCounter":
        """
        Fetches the source file into the current instance.
        """

        file_helper = FileHelper(self.source_file)

        if file_helper.exists():
            self.dataset = DictHelper().from_json_file(file_helper.path)
        else:
            self.dataset = copy.deepcopy(self.STD_DATASET)

        return self

    def save_dataset(self) -> "FilesystemCounter":
        """
        Saves the current dataset into it's final destination.
        """

        DictHelper(self.dataset).to_json_file(self.source_file)

        return self

    @fetch_dataset_beforehand
    def get_dataset_for_printer(self) -> List[Dict[str, Union[str, int]]]:
        """
        Provides the dataset that the printer may understand.

        :raise ValueError:
            When the current testing mode is not supported (yet?).
        """

        result = dict()
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

    @update_source_file_beforehand
    @fetch_dataset_beforehand
    @save_dataset_afterwards
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

        self.dataset["counter"][status.status] += 1
        self.dataset["counter"]["total"] += 1

        self.dataset["percentage"][status.status] = (
            self.dataset["counter"][status.status] * 100
        ) / self.dataset["counter"]["total"]

        self.dataset["percentage"]["total"] = sum(
            [y for x, y in self.dataset["percentage"].items() if x != "total"]
        )
