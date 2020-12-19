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

import functools
from typing import Any, Generator, Optional, Union

import sqlalchemy
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

import PyFunceble.cli.factory
from PyFunceble.dataset.db_base import DBDatasetBase


class MariaDBDatasetBase(DBDatasetBase):
    """
    Provides the base of all MariaDB stored dataset.
    """

    ORM_OBJ: Optional[DeclarativeMeta] = None

    def ensure_orm_obj_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the ORM object is given before launching the decorated
        method.

        :raise RuntimeError:
            When :code:`ORM_OBJ` is not declared.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.ORM_OBJ, DeclarativeMeta):
                raise RuntimeError("<self.ORM_OBJ> not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def __contains__(self, value: str) -> bool:
        raise NotImplementedError()

    def __getitem__(self, value: Any) -> Any:
        raise NotImplementedError()

    def get_content(self) -> Generator[dict, None, None]:
        """
        Provides a generator which provides the next dataset to read.
        """

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            for row in db_session.query(self.ORM_OBJ):
                row = row.to_dict()

                yield row

    @ensure_orm_obj_is_given
    def update(self, row: Union[dict, DeclarativeMeta]) -> "MariaDBDatasetBase":
        """
        Adds the given dataset into the database if it does not exists.
        Update otherwise.

        .. note::
            This should be the prefered method for introduction of new dataset.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or
            :class:`PyFunceble.database.sqlalchemy.base_schema.DeclarativeMeta`
        """

        existing_row = self.get_existing_row(row)

        if not existing_row:
            self.add(row)
        else:
            with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
                for field in self.FIELDS:
                    if field in row and getattr(existing_row, field) != row[field]:
                        setattr(existing_row, field, row[field])

                db_session.add(existing_row)
                db_session.commit()

    @ensure_orm_obj_is_given
    def remove(self, row: Union[dict, DeclarativeMeta]) -> "MariaDBDatasetBase":
        """
        Removes the given dataset from the database.

        :param row:
            The row or dataset to check.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or
            :class:`PyFunceble.database.sqlalchemy.base_schema.DeclarativeMeta`
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            if not isinstance(row, type(self.ORM_OBJ)):
                row = self[row["idna_subject"]]

            if row:
                db_session.delete(row)
                db_session.commit()

    @ensure_orm_obj_is_given
    def exists(self, row: Union[dict, DeclarativeMeta]) -> bool:
        """
        Checks if the given dataset exists in our dataset.

        :param row:
            The row or dataset to check.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or
            :class:`PyFunceble.database.sqlalchemy.base_schema.DeclarativeMeta`
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        if isinstance(row, type(self.ORM_OBJ)):
            row = row.to_dict()

        if self.remove_unneeded_fields:
            row = self.get_filtered_row(row)

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            result = db_session.query(self.ORM_OBJ)

            for field in self.COMPARISON_FIELDS:
                result = result.filter(getattr(self.ORM_OBJ, field) == row[field])

            return result.with_entities(sqlalchemy.func.count()).scalar() > 0

    @ensure_orm_obj_is_given
    def get_existing_row(
        self, row: Union[dict, DeclarativeMeta]
    ) -> Optional[DeclarativeMeta]:
        """
        Check if the given :code:`row` exists. And return the matiching
        dataset.

        :param row:
            The row or dataset to check,
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        if isinstance(row, type(self.ORM_OBJ)):
            row = row.to_dict()

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            result = db_session.query(self.ORM_OBJ)

            for field in self.COMPARISON_FIELDS:
                result = result.filter(getattr(self.ORM_OBJ, field) == row[field])

            try:
                return result.one()
            except NoResultFound:
                pass

        return None

    @ensure_orm_obj_is_given
    def add(self, row: Union[dict, DeclarativeMeta]) -> "MariaDBDatasetBase":
        """
        Adds the given dataset into the database.

        :param row:
            The row or dataset to add.

        :raise TypeError:
            When the given :code:`row` is not a :py:class:`dict` or
            :class:`PyFunceble.database.sqlalchemy.base_schema.DeclarativeMeta`
        """

        if not isinstance(row, (dict, type(self.ORM_OBJ))):
            raise TypeError(
                f"<row> should be {dict} or {self.ORM_OBJ}, {type(row)} given."
            )

        if not self.exists(row):
            with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
                if not isinstance(row, type(self.ORM_OBJ)):
                    # pylint: disable=not-callable
                    dataset = self.ORM_OBJ()
                else:
                    dataset = row

                for key, value in row.items():
                    setattr(dataset, key, value)

                db_session.add(dataset)
                db_session.commit()

        return self
