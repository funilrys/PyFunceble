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

import os
from typing import List, Optional, Union

from sqlalchemy.orm import Session

import PyFunceble.storage
from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject
from PyFunceble.converter.cidr2subject import CIDR2Subject
from PyFunceble.converter.input_line2subject import InputLine2Subject
from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject
from PyFunceble.converter.rpz_policy2subject import RPZPolicy2Subject
from PyFunceble.converter.subject2complements import Subject2Complements
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.converter.wildcard2subject import Wildcard2Subject
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset
from PyFunceble.dataset.autocontinue.sql import SQLDBContinueDataset
from PyFunceble.dataset.base import DatasetBase
from PyFunceble.dataset.csv_base import CSVDatasetBase
from PyFunceble.dataset.db_base import DBDatasetBase
from PyFunceble.dataset.inactive.csv import CSVInactiveDataset
from PyFunceble.dataset.inactive.sql import SQLDBInactiveDataset
from PyFunceble.helpers.list import ListHelper
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


def get_continue_databaset_object(
    db_session: Optional[Session] = None,
) -> Union[DatasetBase, CSVDatasetBase, DBDatasetBase]:
    """
    Provides the continue object to work with.

    :param db_session:
        A database session to use.

    :raise ValueError:
        When the given database type is unkown.
    """

    result = None

    if PyFunceble.storage.CONFIGURATION.cli_testing.db_type in "csv":
        result = CSVContinueDataset()
    elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type in (
        "mariadb",
        "mysql",
        "postgresql",
    ):
        result = SQLDBContinueDataset(db_session=db_session)

    if result:
        result.set_authorized(
            bool(PyFunceble.storage.CONFIGURATION.cli_testing.autocontinue)
        )

        return result

    raise ValueError(
        "<config.db_type> "
        f"({PyFunceble.storage.CONFIGURATION.cli_testing.db_type}) is unknown."
    )


def get_inactive_dataset_object(
    db_session: Optional[Session] = None,
) -> Union[DatasetBase, CSVDatasetBase, DBDatasetBase]:
    """
    Provides the inactive object to work with.

    :param db_session:
        A database session to use.

    :raise ValueError:
        When the given database type is unkown.
    """

    result = None

    if PyFunceble.storage.CONFIGURATION.cli_testing.db_type == "csv":
        result = CSVInactiveDataset()
    elif PyFunceble.storage.CONFIGURATION.cli_testing.db_type in (
        "mariadb",
        "mysql",
        "postgresql",
    ):
        result = SQLDBInactiveDataset(db_session=db_session)

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


def get_subjects_from_line(
    line: str,
    checker_type: str,
    *,
    subject_type: str = "domain",
    adblock_inputline2subject: Optional[AdblockInputLine2Subject] = None,
    wildcard2subject: Optional[Wildcard2Subject] = None,
    rpz_policy2subject: Optional[RPZPolicy2Subject] = None,
    rpz_inputline2subject: Optional[RPZInputLine2Subject] = None,
    inputline2subject: Optional[InputLine2Subject] = None,
    subject2complements: Optional[Subject2Complements] = None,
    url2netloc: Optional[Url2Netloc] = None,
    cidr2subject: Optional[CIDR2Subject] = None,
) -> List[str]:
    """
    Provides the list of subject to test.
    """

    result = []

    if adblock_inputline2subject is None:
        adblock_inputline2subject = AdblockInputLine2Subject(
            aggressive=bool(PyFunceble.storage.CONFIGURATION.cli_decoding.aggressive)
        )

    if wildcard2subject is None:
        wildcard2subject = Wildcard2Subject(
            aggressive=bool(PyFunceble.storage.CONFIGURATION.cli_decoding.aggressive)
        )

    if rpz_policy2subject is None:
        rpz_policy2subject = RPZPolicy2Subject()

    if rpz_inputline2subject is None:
        rpz_inputline2subject = RPZInputLine2Subject(
            aggressive=bool(PyFunceble.storage.CONFIGURATION.cli_decoding.aggressive)
        )

    if inputline2subject is None:
        inputline2subject = InputLine2Subject(
            aggressive=bool(PyFunceble.storage.CONFIGURATION.cli_decoding.aggressive)
        )

    if subject2complements is None:
        subject2complements = Subject2Complements()

    if url2netloc is None:
        url2netloc = Url2Netloc(
            aggressive=bool(PyFunceble.storage.CONFIGURATION.cli_decoding.aggressive)
        )

    if cidr2subject is None:
        cidr2subject = CIDR2Subject()

    adblock_inputline2subject.aggressive = wildcard2subject.aggressive = (
        rpz_inputline2subject.aggressive
    ) = inputline2subject.aggressive = url2netloc.aggressive = bool(
        PyFunceble.storage.CONFIGURATION.cli_decoding.aggressive
    )

    if inputline2subject.aggressive and subject_type == "url":
        # URL Decoder doesn't have an aggressive mode.
        # Therefore, we fix the "misconfiguration"
        inputline2subject.aggressive = not inputline2subject.aggressive

    if PyFunceble.storage.CONFIGURATION.cli_decoding.adblock:
        result.extend(
            # pylint: disable=line-too-long
            adblock_inputline2subject.set_data_to_convert(line).get_converted()
        )
    elif PyFunceble.storage.CONFIGURATION.cli_decoding.wildcard:
        result.append(wildcard2subject.set_data_to_convert(line).get_converted())
    elif PyFunceble.storage.CONFIGURATION.cli_decoding.rpz:
        result.extend(
            [
                rpz_policy2subject.set_data_to_convert(x).get_converted()
                for x in rpz_inputline2subject.set_data_to_convert(line).get_converted()
            ]
        )
    else:
        result.extend(inputline2subject.set_data_to_convert(line).get_converted())

    if PyFunceble.storage.CONFIGURATION.cli_testing.complements:
        result.extend(
            [
                y
                for x in result
                for y in subject2complements.set_data_to_convert(x).get_converted()
            ]
        )

    if PyFunceble.storage.CONFIGURATION.cli_testing.cidr_expand:
        result = [
            y
            for x in result
            for y in cidr2subject.set_data_to_convert(x).get_converted()
        ]

    if checker_type.lower() != "syntax":
        for index, subject in enumerate(result):
            if not subject:
                continue

            netloc = url2netloc.set_data_to_convert(subject).get_converted()

            result[index] = subject.replace(netloc, netloc.lower())

    return ListHelper(result).remove_duplicates().remove_empty().subject
