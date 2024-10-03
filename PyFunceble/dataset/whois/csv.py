"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the WHOIS DB CSV management.

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

import os
from typing import Any, Generator, Optional

import PyFunceble.cli.storage
import PyFunceble.storage
from PyFunceble.dataset.csv_base import CSVDatasetBase
from PyFunceble.dataset.whois.base import WhoisDatasetBase


class CSVWhoisDataset(CSVDatasetBase, WhoisDatasetBase):
    """
    Provides the interface for the management of the WHOIS (db)
    CSV file.
    """

    def __post_init__(self) -> None:
        self.source_file = os.path.join(
            self.config_dir, PyFunceble.cli.storage.WHOIS_DB_FILE
        )

        return super().__post_init__()

    def __contains__(self, value: str) -> bool:
        for row in self.get_content():
            try:
                if value in (row["subject"], row["idna_subject"]):
                    return True
            except KeyError:
                break

        return False

    def __getitem__(self, value: Any) -> Optional[dict]:
        try:
            for row in self.get_content():
                if value in (row["subject"], row["idna_subject"]):
                    return row
        except TypeError:
            pass

        return None

    @CSVDatasetBase.execute_if_authorized(None)
    def get_content(self) -> Generator[Optional[dict], None, None]:
        """
        Provides a generator which provides the next line to read.
        """

        for row in super().get_content():
            try:
                row["epoch"] = float(row["epoch"])
            except (TypeError, ValueError):
                continue

            yield row

    @CSVDatasetBase.execute_if_authorized(None)
    def update(self, row: dict, *, ignore_if_exist: bool = False) -> "CSVWhoisDataset":
        """
        Adds the given dataset into the database if it does not exists.
        Update otherwise.

        ..note::
            This should be the prefered method for introduction of new dataset.

        ..warning::
            This method do nothing if the row is expired.

        :param row:
            The row or dataset to manipulate.

        :param ignore_if_exist:
            Ignores the insertion/update if the row already exists.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        if not isinstance(row, dict):
            raise TypeError(f"<row> should be {dict}, {type(row)} given.")

        if not self.is_expired(row):
            if self.exists(row):
                if not ignore_if_exist and self[row["subject"]] != row:
                    self.remove(row)
                    self.add(row)
            else:
                self.add(row)

        return self

    @CSVDatasetBase.execute_if_authorized(None)
    def remove(self, row: dict) -> "CSVDatasetBase":
        """
        Removes the given dataset from the CSV file.

        :param row:
            The row or dataset to add.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        # If we don't do this, the comparison will fail. #
        # We don't want to overwrite the whole (remove) method just for what
        # we need.
        previous_remove_uneeded_fields = self.remove_unneeded_fields

        self.set_remove_unneeded_fields(False)

        super().remove(row)

        self.set_remove_unneeded_fields(previous_remove_uneeded_fields)

        return self

    def cleanup(self) -> "CSVWhoisDataset":
        """
        Cleanups the dataset. Meaning that we delete every entries which are
        in the past.
        """

        for row in self.get_content():
            if self.is_expired(row):
                self.remove(row)

        return self
