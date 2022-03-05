"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all Mariadb stored datasets.

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

import functools
from datetime import datetime
from typing import Any, Generator, Optional

import sqlalchemy.exc
from sqlalchemy.orm import Session

import PyFunceble.cli.factory
import PyFunceble.sessions
from PyFunceble.dataset.db_base import DBDatasetBase


class MariaDBDatasetBase(DBDatasetBase):
    """
    Provides the base of all MariaDB stored dataset.
    """

    STD_KEEP_SESSION_OPEN: bool = False
    ORM_OBJ = None

    db_session: Optional[Session] = None

    def __init__(
        self,
        *,
        authorized: Optional[bool] = None,
        remove_unneeded_fields: Optional[bool] = None,
        db_session: Optional[Session] = None,
    ) -> None:
        self.db_session = db_session

        super().__init__(
            authorized=authorized, remove_unneeded_fields=remove_unneeded_fields
        )

    def __contains__(self, value: str) -> bool:
        raise NotImplementedError()

    def __getitem__(self, value: Any) -> Any:
        raise KeyError(value)

    def ensure_orm_obj_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the ORM object is given before launching the decorated
        method.

        :raise RuntimeError:
            When :code:`ORM_OBJ` is not declared.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.ORM_OBJ is None:
                raise RuntimeError("<self.ORM_OBJ> not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @DBDatasetBase.execute_if_authorized(None)
    def get_content(self) -> Generator[dict, None, None]:
        """
        Provides a generator which provides the next dataset to read.
        """

        for row in self.db_session.query(self.ORM_OBJ):
            row = row.to_dict()

            yield row

    @DBDatasetBase.execute_if_authorized(None)
    def update(self, row, *, ignore_if_exist: bool = False) -> "MariaDBDatasetBase":
        """
        Adds the given dataset into the database if it does not exists.
        Update otherwise.

        .. note::
            This should be the preferred method for introduction of new dataset.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or sqlalchemy
            schema.
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        PyFunceble.facility.Logger.info("Started to update row.")

        if isinstance(row, type(self.ORM_OBJ)):
            row = row.to_dict()

        if "id" in row:
            self.db_session.execute(
                self.ORM_OBJ.__table__.update().where(self.ORM_OBJ.id == row["id"]),
                row,
            )

            self.db_session.commit()
        else:
            existing_row_id = self.get_existing_row_id(row)

            if existing_row_id is not None:
                if not ignore_if_exist:
                    row["id"] = existing_row_id
                    self.update(row, ignore_if_exist=ignore_if_exist)
            else:
                self.add(row)

        PyFunceble.facility.Logger.debug("Updated row:\n%r", row)
        PyFunceble.facility.Logger.info("Finished to update row.")

        return self

    @DBDatasetBase.execute_if_authorized(None)
    @ensure_orm_obj_is_given
    def remove(self, row) -> "MariaDBDatasetBase":
        """
        Removes the given dataset from the database.

        :param row:
            The row or dataset to check.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or sqlalchemy
            schema.
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        PyFunceble.facility.Logger.info("Started to remove row.")

        if not isinstance(row, type(self.ORM_OBJ)):
            row_id = self.get_existing_row_id(row)

            if row_id is not None:
                self.db_session.query(self.ORM_OBJ).filter(
                    self.ORM_OBJ == row_id
                ).delete()
                self.db_session.commit()
        else:
            self.db_session.delete(row)
            self.db_session.commit()

        PyFunceble.facility.Logger.debug("Removed row:\n%r", row)
        PyFunceble.facility.Logger.info("Finished to remove row.")

        return self

    @DBDatasetBase.execute_if_authorized(False)
    @ensure_orm_obj_is_given
    def exists(self, row) -> bool:
        """
        Checks if the given dataset exists in our dataset.

        :param row:
            The row or dataset to check.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or sqlalchemy
            schema.
        """

        return self.get_existing_row_id(row) is not None

    @DBDatasetBase.execute_if_authorized(None)
    @ensure_orm_obj_is_given
    def get_existing_row_id(self, row):
        """
        Returns the ID of the existing row.

        :param row:
            The row or dataset to check,
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        if isinstance(row, type(self.ORM_OBJ)):
            row = row.to_dict()

        result = self.db_session.query(self.ORM_OBJ.id)

        for field in self.COMPARISON_FIELDS:
            result = result.filter(getattr(self.ORM_OBJ, field) == row[field])

        result = result.first()

        if result is not None:
            return result.id
        return None

    @DBDatasetBase.execute_if_authorized(None)
    @ensure_orm_obj_is_given
    def get_existing_row(self, row):
        """
        Returns the matching row.

        :param row:
            The row or dataset to check,
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        if isinstance(row, type(self.ORM_OBJ)):
            row = row.to_dict()

        result = self.db_session.query(self.ORM_OBJ)

        for field in self.COMPARISON_FIELDS:
            result = result.filter(getattr(self.ORM_OBJ, field) == row[field])

        return result.first()

    @DBDatasetBase.execute_if_authorized(None)
    @ensure_orm_obj_is_given
    def add(self, row) -> "MariaDBDatasetBase":
        """
        Adds the given dataset into the database.

        :param row:
            The row or dataset to add.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or sqlalchemy
            schema.
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        PyFunceble.facility.Logger.info("Started to add row.")

        if isinstance(row, type(self.ORM_OBJ)):
            row = row.to_dict()

        try:
            self.db_session.execute(self.ORM_OBJ.__table__.insert(), row)
            self.db_session.commit()
        except sqlalchemy.exc.DataError as exception:
            if "expiration_date" not in row and "epoch" not in row:
                raise exception

            y2k38_limit = datetime(2037, 12, 31, 0, 0)
            new_date = datetime.fromtimestamp(float(row["epoch"]))
            new_date -= new_date - y2k38_limit

            row["epoch"] = str(new_date.timestamp())
            row["expiration_date"] = new_date.strftime("%d-%b-%Y")

            self.db_session.execute(self.ORM_OBJ.__table__.insert(), row)
            self.db_session.commit()

        PyFunceble.facility.Logger.debug("Added row:\n%r", row)
        PyFunceble.facility.Logger.info("Finished to add row.")

        return self
