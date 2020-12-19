"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the MariaDB management.

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

from typing import Any, Optional

import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound

import PyFunceble.cli.factory
from PyFunceble.database.sqlalchemy.all_schemas import Continue
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.mariadb_base import MariaDBDatasetBase


class MariaDBContinueDataset(MariaDBDatasetBase, ContinueDatasetBase):
    """
    Provides the interface for the management and the Continue dataset unser
    mariadb.
    """

    ORM_OBJ: Continue = Continue

    def __contains__(self, value: str) -> bool:
        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            return (
                db_session.query(self.ORM_OBJ)
                .filter(
                    self.ORM_OBJ.idna_subject == value,
                )
                .with_entities(sqlalchemy.func.count())
                .scalar()
                > 0
            )

    def __getitem__(self, value: Any) -> Optional[Continue]:
        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            try:
                return (
                    db_session.query(self.ORM_OBJ)
                    .filter(
                        self.ORM_OBJ.idna_subject == value,
                    )
                    .one()
                )
            except NoResultFound:
                return None

    # pylint: disable=arguments-differ
    def cleanup(
        self, *, source: str, destination: str, checker_type: str
    ) -> "MariaDBContinueDataset":
        """
        Cleanups the dataset. Meaning that we delete every entries which are
        needed anymore.

        :param source:
            The source to delete.
        :param destination:
            The destination to delete.
        :param checker_type:
            The checker type to delete.
        """

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            db_session.query(self.ORM_OBJ).filter(self.ORM_OBJ.source == source).filter(
                self.ORM_OBJ.destination == destination
            ).filter(self.ORM_OBJ.checker_type == checker_type).delete(
                synchronize_session=False
            )
            db_session.commit()

        return self
