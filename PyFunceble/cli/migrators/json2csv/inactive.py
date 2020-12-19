"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the our inactive DB migrator.

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


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

import datetime
import os

import domain2idna

import PyFunceble.cli.storage
import PyFunceble.storage
from PyFunceble.cli.migrators.json2csv.base import JSON2CSVMigratorBase
from PyFunceble.cli.utils.testing import get_destination_from_origin
from PyFunceble.dataset.inactive.csv import CSVInactiveDataset
from PyFunceble.helpers.file import FileHelper


class InactiveJSON2CSVMigrator(JSON2CSVMigratorBase):
    """
    The migrator of the inactive database dile.
    """

    source_file: str = os.path.join(
        PyFunceble.storage.CONFIG_DIRECTORY, PyFunceble.cli.storage.INACTIVE_DB_OLD_FILE
    )

    dataset: CSVInactiveDataset = CSVInactiveDataset()

    def migrate(self) -> "InactiveJSON2CSVMigrator":
        """
        Starts the migration.
        """

        file_helper = FileHelper(self.source_file)

        if file_helper.exists():
            self.dataset.set_authorized(True)
            dataset = {
                "idna_subject": None,
                "status": None,
                "status_source": None,
                "checker_type": "AVAILABILITY",
                "destination": None,
                "source": None,
                "tested_at": None,
            }

            with file_helper.open("r", encoding="utf-8") as file_stream:
                for line in file_stream:
                    line = (
                        line.strip()
                        .replace('"', "")
                        .replace(",", "")
                        .replace(
                            "{",
                            "",
                        )
                        .replace("}", "")
                    )

                    if ":" not in line:
                        continue

                    index, value = [x.strip() for x in line.rsplit(":", 1)]

                    if not value:
                        if index.isdigit():
                            dataset["tested_at"] = datetime.datetime.fromtimestamp(
                                float(index)
                            ).isoformat()
                        else:
                            dataset["source"] = os.path.abspath(index)
                            dataset["destination"] = get_destination_from_origin(
                                dataset["source"]
                            )

                        continue

                    dataset["idna_subject"] = domain2idna.domain2idna(index)
                    dataset["status"] = value

                    if not dataset["tested_at"]:
                        dataset["tested_at"] = datetime.datetime.utcnow().isoformat()

                    self.dataset.update(dataset)

            file_helper.delete()
        return self
