"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to the registrar counter.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from typing import Dict, List, Optional, Union

import PyFunceble.cli.storage
from PyFunceble.cli.filesystem.json_base import FilesystemJSONBase
from PyFunceble.helpers.list import ListHelper


class RegistrarCounter(FilesystemJSONBase):
    """
    Provides our registrar stats counter.
    """

    STD_DATASET: Dict[str, int] = {
        "counter": {
            "total": 0,
        },
        "percentage": {"total": 0},
    }

    SUPPORTED_TEST_MODES: List[str] = ["AVAILABILITY"]

    SOURCE_FILE: str = PyFunceble.cli.storage.REGISTRAR_COUNTER_FILE

    @FilesystemJSONBase.fetch_dataset_beforehand
    def get_dataset_for_printer(
        self, *, limit: Optional[int] = 15
    ) -> List[Dict[str, Union[str, int]]]:
        """
        Provides the dataset that the printer may understand.

        :param limit:
            Maximum number of registrars to display.

            .. warning::
                If set to :code:`None`, all registrars will be displayed.

        :raise ValueError:
            When the current testing mode is not supported (yet?).
        """

        result = {}
        testing_mode = PyFunceble.cli.utils.testing.get_testing_mode()

        if testing_mode not in self.SUPPORTED_TEST_MODES:
            raise ValueError("<testing_mode> ({testing_mode!r}) is not supported.")

        for registrar, value in self.dataset["counter"].items():
            if registrar == "total":
                continue

            result[registrar] = {"registrar": registrar, "amount": value}

        for registrar, value in self.dataset["percentage"].items():
            if registrar == "total":
                continue

            result[registrar]["percentage"] = f"{round(value)}%"

        # Apply the right order.
        result = (
            ListHelper([y for _, y in result.items()])
            .custom_sort(key_method=lambda x: x["amount"], reverse=True)
            .subject
        )

        return result[:limit] if limit else result

    @FilesystemJSONBase.update_source_file_path_beforehand
    @FilesystemJSONBase.fetch_dataset_beforehand
    @FilesystemJSONBase.save_dataset_afterwards
    def count(self, registrar: str) -> "RegistrarCounter":
        """
        Starts the counting process.

        :param registrar:
            The registrar to count into our dataset.
        """

        if not isinstance(registrar, str):
            raise TypeError(f"<registrar> should be {str}, {type(registrar)} given.")

        if registrar not in self.dataset["counter"]:
            self.dataset["counter"][registrar] = 1
        else:
            self.dataset["counter"][registrar] += 1

        self.dataset["counter"]["total"] += 1

        self.dataset["percentage"][registrar] = (
            self.dataset["counter"][registrar] * 100
        ) / self.dataset["counter"]["total"]

        for key in self.dataset["percentage"]:
            if key in ("total", registrar):
                continue

            self.dataset["percentage"][key] = (
                self.dataset["counter"][key] * 100
            ) / self.dataset["counter"]["total"]

        self.dataset["percentage"]["total"] = sum(
            y for x, y in self.dataset["percentage"].items() if x != "total"
        )

        return self
