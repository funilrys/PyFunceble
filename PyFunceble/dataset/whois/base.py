"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all WHOIS related dataset.

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

from datetime import datetime
from typing import List, Union

from PyFunceble.database.sqlalchemy.all_schemas import WhoisRecord
from PyFunceble.dataset.db_base import DBDatasetBase


class WhoisDatasetBase(DBDatasetBase):
    """
    Provides the base of all Whois related interface.
    """

    FIELDS: List[str] = [
        "subject",
        "idna_subject",
        "expiration_date",
        "epoch",
        "registrar",
    ]

    COMPARISON_FIELDS: List[str] = ["subject", "idna_subject"]

    @staticmethod
    def is_expired(row: Union[dict, WhoisRecord]) -> bool:
        """
        Given a row, we look if the row is expired.
        """

        if isinstance(row, WhoisRecord):
            to_check = row.epoch
        elif "epoch" in row:
            to_check = row["epoch"]
        else:
            return True

        return datetime.utcnow() > datetime.fromtimestamp(float(to_check))

    @DBDatasetBase.execute_if_authorized(None)
    def get_filtered_row(self, row: Union[dict, WhoisRecord]) -> dict:
        """
        Removes all unkowns fields (not declared) from the given row.

        :param row:
            The row to work with.
        """

        if isinstance(row, WhoisDatasetBase):
            row = row.to_dict()

        result = super().get_filtered_row(row)

        if "epoch" in result and isinstance(result["epoch"], float):
            # We do this here because we have to convert to a string in
            # order to be able to write into the CSV file.
            result["epoch"] = str(result["epoch"])

        return result
