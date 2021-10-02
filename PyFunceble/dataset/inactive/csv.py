"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the inactive db  CSV management.

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

import os
from datetime import datetime, timedelta
from typing import Generator, Optional, Tuple

import PyFunceble.cli.storage
import PyFunceble.storage
from PyFunceble.dataset.csv_base import CSVDatasetBase
from PyFunceble.dataset.inactive.base import InactiveDatasetBase


class CSVInactiveDataset(CSVDatasetBase, InactiveDatasetBase):
    """
    Provides the interface for the management of the inactive
    CSV file.
    """

    def __post_init__(self) -> None:
        self.source_file = os.path.join(
            PyFunceble.storage.CONFIG_DIRECTORY, PyFunceble.cli.storage.INACTIVE_DB_FILE
        )

        return super().__post_init__()

    @CSVDatasetBase.execute_if_authorized(None)
    def get_to_retest(
        self, destination: str, checker_type: str, *, min_days: Optional[int]
    ) -> Generator[Tuple[str, str, Optional[int]], dict, None]:

        days_ago = datetime.utcnow() - timedelta(days=min_days)

        for dataset in self.get_filtered_content(
            {"destination": destination, "checker_type": checker_type}
        ):
            if not isinstance(dataset["tested_at"], datetime):
                try:
                    date_of_inclusion = datetime.fromisoformat(dataset["tested_at"])
                except (TypeError, ValueError):
                    date_of_inclusion = datetime.utcnow() - timedelta(days=365)
            else:
                date_of_inclusion = dataset["tested_at"]

            if date_of_inclusion > days_ago:
                continue

            yield dataset
