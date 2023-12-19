"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our reputation status handler.

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

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import unittest
import unittest.mock

from PyFunceble.checker.reputation.status import ReputationCheckerStatus


class TestReputationCheckerStatus(unittest.TestCase):
    """
    Tests of our reputation status handler.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.status = ReputationCheckerStatus(subject="example.org")

    def tearDown(self) -> None:
        """
        Destroys everything previously initiated for the tests.
        """

        del self.status

    def test_is_malicious(self) -> None:
        """
        Tests the method which let us check if the current status is a
        malicious one.
        """

        self.status.status = "MALICIOUS"

        expected = True
        actual = self.status.is_malicious()

        self.assertEqual(expected, actual)

    def test_is_not_malicious(self) -> None:
        """
        Tests the method which let us check if the current status is a
        malicious one.

        In this test we check the case that the status is actually not malicious.
        """

        self.status.status = "SANE"

        expected = False
        actual = self.status.is_malicious()

        self.assertEqual(expected, actual)

    def test_is_sane(self) -> None:
        """
        Tests the method which let us check if the current status is a
        sane one.
        """

        self.status.status = "SANE"

        expected = True
        actual = self.status.is_sane()

        self.assertEqual(expected, actual)

    def test_is_not_sane(self) -> None:
        """
        Tests the method which let us check if the current status is a
        sane one.

        In this test we check the case that the status is actually not sane.
        """

        self.status.status = "MALICIOUS"

        expected = False
        actual = self.status.is_sane()

        self.assertEqual(expected, actual)

    def test_has_bad_reputation(self) -> None:
        """
        Tests the method which let us check if the current status is a
        bad one.
        """

        self.status.status = "MALICIOUS"

        expected = True
        actual = self.status.has_bad_reputation()

        self.assertEqual(expected, actual)

    def test_has_not_bad_reputation(self) -> None:
        """
        Tests the method which let us check if the current status is a
        bad one.

        In this test we check the case that the status is actually a good one
        """

        self.status.status = "SANE"

        expected = False
        actual = self.status.has_bad_reputation()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
