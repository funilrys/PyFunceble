"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our URL reputation checker.

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

import unittest
import unittest.mock

from PyFunceble.checker.reputation.url import URLReputationChecker
from PyFunceble.query.dns.query_tool import DNSQueryTool

try:
    import reputation_test_base
except ModuleNotFoundError:  # pragma: no cover
    from . import reputation_test_base


class TestURLReputationChecker(reputation_test_base.ReputationCheckerTestBase):
    """
    Tests of the URL reputation checker.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        upstream_result = super().setUp()

        self.checker = URLReputationChecker()
        self.checker.ipv4_reputation_query_tool.source_file = self.tempfile.name

        self.dns_query_tool_path = unittest.mock.patch.object(DNSQueryTool, "query")
        self.mock_query_tool = self.dns_query_tool_path.start()

        # Not needed in this scope :-)
        self.checker.do_syntax_check_first = False

        return upstream_result

    def tearDown(self) -> None:
        """
        Destroys everything previously initiated for the tests.
        """

        upstream_result = super().tearDown()

        self.dns_query_tool_path.stop()

        del self.dns_query_tool_path
        del self.mock_query_tool

        return upstream_result

    def test_query_status_positive_domain(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the resolved IP of the given URL is known to be malicious.
        """

        self.mock_query_tool.return_value = self.fake_query_a_record()

        self.checker.subject = "https://example.org"
        self.checker.query_status()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_positive_ipv4(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the IP of the given URL is known to be malicious.
        """

        self.mock_query_tool.return_value = ["127.176.134.253"]

        self.checker.subject = "https://127.176.134.253"
        self.checker.query_status()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_positive_ipv6(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the IP of the given URL is known to be malicious.
        """

        self.mock_query_tool.return_value = self.fake_query_a_record()

        self.checker.subject = "https://[2606:2800:220:1:248:1893:25c8:1946]"
        self.checker.query_status()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_negative_domain(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the resolved IP of the given URL is not known to be malicious.
        """

        self.mock_query_tool.return_value = self.fake_query_a_record_not_known()

        self.checker.subject = "https://example.org"
        self.checker.query_status()

        expected_status = "SANE"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_negative_ipv4(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the IP of the given URL is not known to be malicious.
        """

        self.mock_query_tool.return_value = ["192.168.1.1"]

        self.checker.subject = "https://192.168.1.1"
        self.checker.query_status()

        expected_status = "SANE"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_negative_ipv6(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the IP of the given URL is not known to be malicious.
        """

        self.mock_query_tool.return_value = self.fake_query_a_record_not_known()

        self.checker.subject = "https://[2606:2800:220:1:248:1893:25c8:1946]"
        self.checker.query_status()

        expected_status = "SANE"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)


if __name__ == "__main__":
    unittest.main()
