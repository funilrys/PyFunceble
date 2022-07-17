"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all CSV storeed datasets.

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

import csv
import tempfile
from datetime import datetime, timedelta
from typing import Generator, Optional, Tuple

import PyFunceble.facility
from PyFunceble.dataset.db_base import DBDatasetBase
from PyFunceble.helpers.file import FileHelper


class CSVDatasetBase(DBDatasetBase):
    """
    Provides the base of all CSV dataset.
    """

    @DBDatasetBase.ensure_source_file_exists
    def get_csv_writer(self) -> Tuple[csv.DictWriter, open]:
        """
        Provides the standard and initiated CSV Dict writer along with the
        file that was open with it.
        """

        file_helper = FileHelper(self.source_file)

        add_header = not file_helper.exists()

        file_handler = file_helper.open("a+", newline="", encoding="utf-8")
        writer = csv.DictWriter(file_handler, fieldnames=self.FIELDS)

        if add_header:
            writer.writeheader()

        return writer, file_handler

    def update(self, row: dict, *, ignore_if_exist: bool = False) -> "DBDatasetBase":
        """
        Adds the given dataset into the database if it does not exists.
        Update otherwise.

        :param row:
            The row or dataset to manipulate.

        :param ignore_if_exist:
            Ignore the insertion/update if the row already exists.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        if not isinstance(row, dict):
            raise TypeError(f"<row> should be {dict}, {type(row)} given.")

        PyFunceble.facility.Logger.info("Started to update row.")

        if self.exists(row):
            if not ignore_if_exist:
                self.remove(row)
                self.add(row)
        else:
            self.add(row)

        PyFunceble.facility.Logger.debug("Updated row:\n%r", row)
        PyFunceble.facility.Logger.info("Finished to update row.")

        return self

    @DBDatasetBase.ensure_source_file_exists
    @DBDatasetBase.execute_if_authorized(None)
    def add(self, row: dict) -> "CSVDatasetBase":
        """
        Adds the given dataset into the CSV file.

        :param row:
            The row or dataset to add.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        if not isinstance(row, dict):
            raise TypeError(f"<row> should be {dict}, {type(row)} given.")

        PyFunceble.facility.Logger.info("Started to add row.")

        if self.remove_unneeded_fields:
            row = self.get_filtered_row(row)

        writer, file_handler = self.get_csv_writer()

        writer.writerow(row)

        file_handler.close()

        PyFunceble.facility.Logger.debug("Added row:\n%r", row)

        PyFunceble.facility.Logger.info("Finished to add row.")

        return self

    @DBDatasetBase.ensure_source_file_exists
    @DBDatasetBase.execute_if_authorized(None)
    def remove(self, row: dict) -> "CSVDatasetBase":
        """
        Removes the given dataset from the CSV file.

        :param row:
            The row or dataset to add.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        if not isinstance(row, dict):
            raise TypeError(f"<row> should be {dict}, {type(row)} given.")

        PyFunceble.facility.Logger.info("Started to remove row.")

        if self.remove_unneeded_fields:
            row = self.get_filtered_row(row)

        our_temp_file = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
        our_temp_filename = our_temp_file.name

        writer = csv.DictWriter(our_temp_file, fieldnames=self.FIELDS)
        writer.writeheader()

        for read_row in self.get_content():
            if self.are_equal(read_row, row):
                continue

            writer.writerow(read_row)

        our_temp_file.close()

        FileHelper(our_temp_filename).move(self.source_file)

        PyFunceble.facility.Logger.debug("Removed row:\n%r", row)

        PyFunceble.facility.Logger.info("Finished to remove row.")

        return self

    @DBDatasetBase.ensure_source_file_exists
    @DBDatasetBase.execute_if_authorized(None)
    def get_content(self) -> Generator[Optional[dict], None, None]:
        """
        Provides a generator which provides the next line to read.
        """

        file_helper = FileHelper(self.source_file)

        if file_helper.exists():
            file_handler = file_helper.open(newline="", encoding="utf-8")
            reader = csv.DictReader(file_handler)

            for row in reader:
                if "tested_at" in row:
                    try:
                        row["tested_at"] = datetime.fromisoformat(row["tested_at"])
                    except (TypeError, ValueError):
                        row["tested_at"] = datetime.utcnow() - timedelta(days=365)

                yield row

            file_handler.close()

    @DBDatasetBase.execute_if_authorized(None)
    def get_filtered_content(
        self, filter_map: dict
    ) -> Generator[Optional[dict], None, None]:
        """
        Provides a generator which provides the next line to read.

        :param filter_map:
            A dictionary representing what we need to filter.

        :raise TypeError:
            When the given :code:`filter_map` is not a :py:class:`dict`.
        """

        if not isinstance(filter_map, dict):
            raise TypeError(f"<filter_map> should be {dict}, {type(filter_map)} given.")

        for row in self.get_content():
            if all(x in row and row[x] == y for x, y in filter_map.items()):
                yield row

    def get_filtered_comparision_row(self, row: dict):
        """
        Makes the given row ready for comparison.
        """

        if self.COMPARISON_FIELDS:
            row = {x: y for x, y in row.items() if x in self.COMPARISON_FIELDS}
            row.update({x: "" for x in self.COMPARISON_FIELDS if x not in row})

            return row

        return row

    @DBDatasetBase.ensure_source_file_exists
    @DBDatasetBase.execute_if_authorized(False)
    def exists(self, row: dict) -> bool:
        """
        Checks if the given dataset exists in our dataset.

        :param row:
            The row or dataset to check.
        """

        if self.remove_unneeded_fields:
            row = self.get_filtered_row(row)

        row = self.get_filtered_comparision_row(row)

        for read_row in self.get_content():
            if self.are_equal(read_row, row):
                return True

        return False

    @DBDatasetBase.execute_if_authorized(False)
    def are_equal(self, read_row: dict, row: dict) -> bool:
        """
        Compares the given :code:`read_row` to the `row`.

        :param read_row:
            The row read from the dataset infrastructure.
        :param row:
            The row given by the testing infrastructure.
        """

        if self.remove_unneeded_fields:
            read_row = self.get_filtered_row(read_row)
            row = self.get_filtered_row(row)

        read_row = self.get_filtered_comparision_row(read_row)
        row = self.get_filtered_comparision_row(row)

        return row.items() <= read_row.items()
