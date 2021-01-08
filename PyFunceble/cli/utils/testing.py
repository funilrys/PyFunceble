"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some testing related utilities

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import os
from typing import Union

import PyFunceble.storage
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset
from PyFunceble.dataset.autocontinue.mariadb import MariaDBContinueDataset
from PyFunceble.dataset.autocontinue.mysql import MySQLContinueDataset
from PyFunceble.dataset.base import DatasetBase
from PyFunceble.dataset.csv_base import CSVDatasetBase
from PyFunceble.dataset.db_base import DBDatasetBase
from PyFunceble.dataset.inactive.csv import CSVInactiveDataset
from PyFunceble.dataset.inactive.mariadb import MariaDBInactiveDataset
from PyFunceble.dataset.inactive.mysql import MySQLInactiveDataset
from PyFunceble.helpers.regex import RegexHelper


def get_testing_mode() -> str:
    """
    Tries to provides the testing mode to apply to the CLI.
    """

    if PyFunceble.storage.CONFIGURATION.cli_testing.testing_mode.syntax:
        return "SYNTAX"
    if PyFunceble.storage.CONFIGURATION.cli_testing.testing_mode.reputation:
        return "REPUTATION"

    if PyFunceble.storage.CONFIGURATION.cli_testing.testing_mode.availability:
        return "AVAILABILITY"
    return "UNKNOWN"


def get_continue_databaset_object() -> Union[
    DatasetBase, CSVDatasetBase, DBDatasetBase
]:
    """
    Provides the continue object to work with.

    :raise ValueError:
        When the given database type is unkown.
    """

    result = None

    if PyFunceble.storage.CONFIGURATION.cli_testing.db_type in "csv":
        result = CSVContinueDataset()
    elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "mariadb":
        result = MariaDBContinueDataset()
    elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "mysql":
        result = MySQLContinueDataset()

    if result:
        result.set_authorized(
            bool(PyFunceble.storage.CONFIGURATION.cli_testing.autocontinue)
        )

        return result

    raise ValueError(
        "<config.db_type> "
        f"({PyFunceble.storage.CONFIGURATION.cli_testing.db_type}) is unknown."
    )


def get_inactive_dataset_object() -> Union[DatasetBase, CSVDatasetBase, DBDatasetBase]:
    """
    Provides the inactive object to work with.

    :raise ValueError:
        When the given database type is unkown.
    """

    result = None

    if PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "csv":
        result = CSVInactiveDataset()
    elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "mariadb":
        result = MariaDBInactiveDataset()
    elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "mysql":
        result = MySQLInactiveDataset()

    if result:
        result.set_authorized(
            bool(PyFunceble.storage.CONFIGURATION.cli_testing.inactive_db)
        )

        return result

    raise ValueError(
        "<config.db_type> "
        f"({PyFunceble.storage.CONFIGURATION.cli_testing.db_type}) is unknown."
    )


def get_destination_from_origin(origin: str) -> str:
    """
    Given the origin, we provides the destination.
    """

    if "/" in origin:
        origin = origin.rsplit("/", 1)[-1]

    if os.sep in origin:
        origin = origin.rsplit(os.sep, 1)[-1]

    return RegexHelper("[^a-zA-Z0-9._-]").replace_match(origin, "_")
