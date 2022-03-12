"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our hybrid (domain & IP) reputation checker.

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

from PyFunceble.checker.reputation.domain_and_ip import DomainAndIPReputationChecker
from PyFunceble.query.dns.query_tool import DNSQueryTool

try:
    import reputation_test_base
except ModuleNotFoundError:  # pragma: no cover
    from . import reputation_test_base


class TestDomainReputationChecker(reputation_test_base.ReputationCheckerTestBase):
    """
    Tests of the hybrid (domain & IP) reputation checker.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        upstream_result = super().setUp()

        self.checker = DomainAndIPReputationChecker()
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

    def test_query_status_domain(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the inputted subject is a domain.
        """

        self.mock_query_tool.return_value = self.fake_query_a_record()

        self.checker.subject = "example.org"
        self.checker.query_status()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_ip(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the inputted subject is an IP.
        """

        self.mock_query_tool.return_value = ["192.168.1.1"]

        self.checker.subject = "192.168.1.1"
        self.checker.query_status()

        expected_status = "SANE"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)


if __name__ == "__main__":
    unittest.main()
