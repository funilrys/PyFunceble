"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our IP availability checker.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/latest/

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

import unittest
import unittest.mock
from datetime import datetime

from PyFunceble.checker.availability.ip import IPAvailabilityChecker
from PyFunceble.checker.reputation.ip import IPReputationChecker
from PyFunceble.checker.reputation.status import ReputationCheckerStatus


class TestIPAvailabilityChecker(unittest.TestCase):
    """
    Tests of our IP availability checker.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.checker = IPAvailabilityChecker()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.checker

    @unittest.mock.patch.object(IPReputationChecker, "get_status")
    def test_try_to_query_status_from_reputation(
        self, reputation_checker_path: unittest.mock.MagicMock
    ) -> None:
        """
        Tests of the method that tries to define the status from the reputation
        checker.
        """

        self.checker.subject = "192.168.1.1"

        reputation_checker_path.return_value = ReputationCheckerStatus(
            subject="192.168.1.1",
            idna_subject="192.168.1.1",
            status="SANE",
            status_source="REPUTATION",
            tested_at=datetime.utcnow(),
        )

        self.checker.try_to_query_status_from_reputation()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        reputation_checker_path.return_value = ReputationCheckerStatus(
            subject="192.168.1.1",
            idna_subject="192.168.1.1",
            status="MALICIOUS",
            status_source="REPUTATION",
            tested_at=datetime.utcnow(),
        )

        self.checker.try_to_query_status_from_reputation()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "REPUTATION"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)


if __name__ == "__main__":
    unittest.main()
