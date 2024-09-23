"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some utilities related to the WHOIS query.

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

from typing import Optional, Union

from sqlalchemy.orm import Session

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.dataset.base import DatasetBase
from PyFunceble.dataset.csv_base import CSVDatasetBase
from PyFunceble.dataset.db_base import DBDatasetBase
from PyFunceble.dataset.whois.csv import CSVWhoisDataset
from PyFunceble.dataset.whois.sql import SQLDBWhoisDataset


def get_whois_dataset_object(
    *, db_session: Optional[Session] = None
) -> Union[DatasetBase, CSVDatasetBase, DBDatasetBase]:
    """
    Provides the whois dataset object to work with.

    :param db_session:
        A database session to use.

    :raise ValueError:
        When the given database type is unkown.
    :raise RuntimeError:
        When the configuration was not loaded yet.
    """

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        result = None

        if PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "csv":
            result = CSVWhoisDataset()
        elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type in (
            "mariadb",
            "mysql",
            "postgresql",
        ):
            result = SQLDBWhoisDataset(db_session=db_session)

        if result:
            result.set_authorized(
                bool(PyFunceble.storage.CONFIGURATION.cli_testing.whois_db)
            )

            return result

        raise ValueError(
            "<config.db_type> "
            f"({PyFunceble.storage.CONFIGURATION.cli_testing.db_type}) is unknown."
        )
    raise RuntimeError("Configuration not loaded yet.")
