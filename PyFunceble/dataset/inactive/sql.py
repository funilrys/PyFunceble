"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the inactive DB (mariadb) management.

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

from datetime import datetime, timedelta, timezone
from typing import Generator, Optional, Tuple

from PyFunceble.database.sqlalchemy.all_schemas import Inactive
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.dataset.sql_base import SQLDBDatasetBase


class SQLDBInactiveDataset(SQLDBDatasetBase, InactiveDatasetBase):
    """
    Provides tht interface for the management and the WHOIS dataset under
    mariadb.
    """

    ORM_OBJ: Inactive = Inactive

    @SQLDBDatasetBase.execute_if_authorized(None)
    @SQLDBDatasetBase.ensure_orm_obj_is_given
    def get_to_retest(
        self, destination: str, checker_type: str, *, min_days: Optional[int]
    ) -> Generator[Tuple[str, str, Optional[int]], dict, None]:
        days_ago = datetime.now(timezone.utc) - timedelta(days=min_days)

        result = (
            self.db_session.query(self.ORM_OBJ)
            .filter(self.ORM_OBJ.destination == destination)
            .filter(self.ORM_OBJ.checker_type == checker_type)
            .filter(self.ORM_OBJ.tested_at < days_ago)
        )

        for row in result:
            if not hasattr(row, "tested_at"):
                # This is just a safety.
                continue

            yield row.to_dict()
