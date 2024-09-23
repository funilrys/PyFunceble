"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the WHOIS DB (sql) management.

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

from datetime import datetime, timezone
from typing import Any, Generator, Optional, Union

import sqlalchemy
from sqlalchemy.exc import ProgrammingError

import PyFunceble.cli.factory
import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.sessions
import PyFunceble.storage
from PyFunceble.database.sqlalchemy.all_schemas import WhoisRecord
from PyFunceble.dataset.sql_base import SQLDBDatasetBase
from PyFunceble.dataset.whois.base import WhoisDatasetBase


class SQLDBWhoisDataset(SQLDBDatasetBase, WhoisDatasetBase):
    """
    Provides the interface for the management of the WHOIS database under
    (mariadb).
    """

    ORM_OBJ: WhoisRecord = WhoisRecord

    @SQLDBDatasetBase.execute_if_authorized(None)
    def __contains__(self, value: str) -> bool:
        try:
            return (
                self.db_session.query(self.ORM_OBJ)
                .filter(
                    sqlalchemy.or_(
                        self.ORM_OBJ.subject == value,
                        self.ORM_OBJ.idna_subject == value,
                    )
                )
                .first()
                is not None
            )
        except ProgrammingError:
            return None

    @SQLDBDatasetBase.execute_if_authorized(None)
    def __getitem__(self, value: Any) -> Optional[WhoisRecord]:
        try:
            return (
                self.db_session.query(self.ORM_OBJ)
                .filter(
                    sqlalchemy.or_(
                        self.ORM_OBJ.subject == value,
                        self.ORM_OBJ.idna_subject == value,
                    )
                )
                .first()
            )
        except ProgrammingError:
            return None

    @SQLDBDatasetBase.execute_if_authorized(None)
    def get_content(self) -> Generator[dict, None, None]:
        """
        Provides a generator which provides the next dataset to read.
        """

        for row in super().get_content():
            row["epoch"] = float(row["epoch"])

            yield row

    @SQLDBDatasetBase.execute_if_authorized(None)
    def update(
        self, row: Union[dict, WhoisRecord], *, ignore_if_exist: bool = False
    ) -> "SQLDBWhoisDataset":
        """
        Adds the given dataset into the database if it does not exists.
        Update otherwise.

        ..note::
            This should be the prefered method for introduction of new dataset.

        ..warning::
            This method do nothing if the row is expired.

        :param row:
            The row or dataset to manipulate.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        if not self.is_expired(row):
            try:
                super().update(row, ignore_if_exist=ignore_if_exist)
            except ProgrammingError:
                pass
        else:
            PyFunceble.facility.Logger.debug("Expired dataset:\n%r", row)

        return self

    @SQLDBDatasetBase.execute_if_authorized(None)
    def cleanup(self) -> "SQLDBWhoisDataset":
        """
        Cleanups the dataset. Meaning that we delete every entries which are
        in the past.
        """

        current_timestamp = int(datetime.now(timezone.utc).timestamp())

        try:
            self.db_session.query(self.ORM_OBJ).filter(
                self.ORM_OBJ.epoch < current_timestamp
            ).delete(synchronize_session=False)
            self.db_session.commit()
        except ProgrammingError:
            pass

        PyFunceble.facility.Logger.debug("Deleted all expired WHOIS records")

        return self
