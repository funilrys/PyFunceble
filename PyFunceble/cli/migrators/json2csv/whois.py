"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the our whois DB migrator.

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
from typing import Optional

import domain2idna

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.migrators.json2csv.base import JSON2CSVMigratorBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.dataset.whois.csv import CSVWhoisDataset
from PyFunceble.helpers.file import FileHelper


class WhoisJSON2CSVMigrator(JSON2CSVMigratorBase):
    """
    The migrator of the inactive database dile.
    """

    dataset: Optional[CSVWhoisDataset] = CSVWhoisDataset()

    def __post_init__(self) -> None:
        self.source_file = os.path.join(
            PyFunceble.storage.CONFIG_DIRECTORY,
            PyFunceble.cli.storage.WHOIS_DB_OLD_FILE,
        )

        self.dataset = CSVWhoisDataset()
        return super().__post_init__()

    def migrate(self) -> "WhoisJSON2CSVMigrator":
        """
        Provides the migration logic.
        """

        file_helper = FileHelper(self.source_file)

        if file_helper.exists():
            self.dataset.set_authorized(True)
            dataset = {
                "subject": None,
                "idna_subject": None,
                "expiration_date": None,
                "epoch": None,
            }

            delete_file = True

            with file_helper.open("r", encoding="utf-8") as file_stream:
                for line in file_stream:
                    if (
                        self.continuous_integration
                        and self.continuous_integration.is_time_exceeded()
                    ):
                        delete_file = False
                        break

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

                    index, value = [x.strip() for x in line.split(":")]

                    if not value:
                        dataset["subject"], dataset["idna_subject"] = (
                            index,
                            domain2idna.domain2idna(index),
                        )
                        continue

                    if index == "epoch":
                        dataset["epoch"] = float(value)
                    elif index == "expiration_date":
                        dataset["expiration_date"] = value
                    elif index == "state":
                        PyFunceble.facility.Logger.debug(
                            "Decoded dataset:\n%r.", dataset
                        )

                        self.dataset.update(dataset)

                        if self.print_action_to_stdout:
                            print_single_line()

                        PyFunceble.facility.Logger.info(
                            "Added %r into %r", dataset["idna_subject"], self.dataset
                        )

            if delete_file:
                file_helper.delete()
                self.done = True
        return self
