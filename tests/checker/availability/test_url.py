"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our URL availability checker.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023 Nissar Chababy

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

from PyFunceble.checker.availability.url import URLAvailabilityChecker
from PyFunceble.checker.reputation.status import ReputationCheckerStatus
from PyFunceble.checker.reputation.url import URLReputationChecker


class TestURLAvailabilityChecker(unittest.TestCase):
    """
    Tests our URL availability checker.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.checker = URLAvailabilityChecker()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.checker

    def test_subject_propagator(self) -> None:
        """
        Tests that the subjects and its IDNA counterpart are correctly
        propagated.

        .. versionchanged:: 4.1.0b7.dev
           URL base propagation to allow DNS lookup.
        """

        given = "http://äxample.org"
        expected_subject = "http://äxample.org"
        expected_idna_subject = "http://xn--xample-9ta.org"
        expected_base_url = "xn--xample-9ta.org"

        self.checker.subject = given

        actual_subject = self.checker.status.subject
        actual_idna_propagated = [
            self.checker.domain_syntax_checker.subject,
            self.checker.ip_syntax_checker.subject,
            self.checker.url_syntax_checker.subject,
        ]

        self.assertEqual(expected_subject, actual_subject)
        self.assertEqual(expected_base_url, self.checker.dns_query_tool.subject)

        for actual in actual_idna_propagated:
            self.assertEqual(expected_idna_subject, actual)

        # Now, just make sure the the status get changed and propagated too.

        given = "http://äxample.net"
        expected_subject = "http://äxample.net"
        expected_idna_subject = "http://xn--xample-9ta.net"

        self.checker.subject = given

        actual = self.checker.status.subject

        actual_idna_propagated = [
            self.checker.domain_syntax_checker.subject,
            self.checker.ip_syntax_checker.subject,
            self.checker.url_syntax_checker.subject,
        ]

        self.assertEqual(expected_subject, actual)

        for actual in actual_idna_propagated:
            self.assertEqual(expected_idna_subject, actual)

    def test_try_to_query_status_from_http_status_code(self) -> None:
        """
        Tests the method that tries to define the status from the status code.
        """

        self.checker.subject = "http://example.org"

        self.checker.http_status_code_query_tool.get_status_code = (
            lambda: self.checker.http_status_code_query_tool.STD_UNKNOWN_STATUS_CODE
        )

        self.checker.try_to_query_status_from_http_status_code()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        self.checker.http_status_code_query_tool.get_status_code = lambda: 200

        self.checker.try_to_query_status_from_http_status_code()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "HTTP CODE"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

    @unittest.mock.patch.object(URLReputationChecker, "get_status")
    def test_try_to_query_status_from_reputation(
        self, reputation_checker_path: unittest.mock.MagicMock
    ) -> None:
        """
        Tests of the method that tries to define the status from the reputation
        checker.
        """

        self.checker.subject = "http://example.com"

        reputation_checker_path.return_value = ReputationCheckerStatus(
            subject="http://example.com",
            idna_subject="http://example.com",
            status="SANE",
            status_source="REPUTATION",
            tested_at=datetime.utcnow(),
        )

        self.checker.try_to_query_status_from_reputation()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        reputation_checker_path.return_value = ReputationCheckerStatus(
            subject="http://example.com",
            idna_subject="http://example.com",
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

    def test_try_to_query_status_from_dns(self) -> None:
        """
        Tests the method that tries to define the status from the DNS lookup.

        .. versionadded:: 4.1.0b7.dev
        """

        # Let's test the case that no answer is given back.
        # pylint: disable=unnecessary-lambda
        self.checker.subject = "http://example.org"
        self.checker.query_dns_record = (
            lambda: dict()  # pylint: disable=use-dict-literal
        )

        self.checker.try_to_query_status_from_dns()

        expected_status = "INACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Let's test the case that an answer is given back.
        self.checker.query_dns_record = lambda: {"NS": ["ns1.example.org"]}

        self.checker.try_to_query_status_from_dns()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = None
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)


if __name__ == "__main__":
    unittest.main()
