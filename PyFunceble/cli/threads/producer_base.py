"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our producer threads.

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

from typing import Tuple

import PyFunceble.checker.utils.whois
import PyFunceble.cli.storage
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.threads.base import ThreadsBase


class ProducerThreadBase(ThreadsBase):
    """
    Provides the base of all our producer threads.

    The thread behind this object, will read :code:`the_queue`, and procude
    the outputs.
    """

    thread_name: str = "pyfunceble_producer"

    INACTIVE_STATUSES: Tuple[str] = (
        PyFunceble.storage.STATUS.down,
        PyFunceble.storage.STATUS.invalid,
    )

    def should_we_block_printer(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> bool:
        """
        Checks if we should block the printer.

        The reason behindn this is that we don't want to generate an output
        when a subject was already into the inactive database.

        :param test_dataset:
            The test dataset.
        :param test_result:
            The test result
        """

        return (
            "from_inactive" in test_dataset
            and test_result.status in self.INACTIVE_STATUSES
        )

    @staticmethod
    def should_we_ignore(test_result: CheckerStatusBase) -> bool:
        """
        Checks if the we should ignore the given datasets.

        :param test_dataset:
            The test dataset.
        :param test_result:
            The test result
        """

        return isinstance(test_result, str) and test_result.startswith("ignored_")
