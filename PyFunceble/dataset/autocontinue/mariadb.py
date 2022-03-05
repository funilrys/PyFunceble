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

from datetime import datetime, timedelta
from typing import Generator, Tuple

import PyFunceble.cli.factory
import PyFunceble.sessions
from PyFunceble.database.sqlalchemy.all_schemas import Continue
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.mariadb_base import MariaDBDatasetBase


class MariaDBContinueDataset(MariaDBDatasetBase, ContinueDatasetBase):
    """
    Provides the interface for the management and the Continue dataset unser
    mariadb.
    """

    ORM_OBJ: Continue = Continue

    @MariaDBDatasetBase.execute_if_authorized(None)
    # pylint: disable=arguments-differ
    def cleanup(self, *, session_id: str) -> "MariaDBContinueDataset":
        """
        Cleanups the dataset. Meaning that we delete every entries which are
        needed anymore.

        :param source:
            The source to delete.
        :param session_id:
            The session ID to cleanup.
        """

        self.db_session.query(self.ORM_OBJ).filter(
            self.ORM_OBJ.session_id == session_id
        ).delete(synchronize_session=False)
        self.db_session.commit()

        PyFunceble.facility.Logger.debug(
            "Deleted data related to %s (session_id", session_id
        )

        return self

    @MariaDBDatasetBase.execute_if_authorized(None)
    def get_to_test(self, session_id: str) -> Generator[Tuple[str], str, None]:
        twenty_years_ago = datetime.utcnow() - timedelta(days=365.25 * 20)

        result = (
            self.db_session.query(self.ORM_OBJ)
            .filter(self.ORM_OBJ.session_id == session_id)
            .filter(self.ORM_OBJ.tested_at < twenty_years_ago)
        )

        for row in result:
            if not row.idna_subject:
                continue

            yield row.idna_subject
