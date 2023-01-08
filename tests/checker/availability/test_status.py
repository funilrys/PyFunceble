"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our availability checker status handler.

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

from PyFunceble.checker.availability.status import AvailabilityCheckerStatus


class TestAvailabilityCheckerStatus(unittest.TestCase):
    """
    Tests of our availability status handler.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.status = AvailabilityCheckerStatus(subject="example.org")

    def tearDown(self) -> None:
        """
        Destroys everything we need.
        """

        del self.status

    def test_is_special(self) -> None:
        """
        Tests the method which let us check if the current status is a special
        one.
        """

        self.status.status_after_extra_rules = "ACTIVE"
        self.status.status_before_extra_rules = "INACTIVE"

        self.status.status = "ACTIVE"
        self.status.status_source = "SPECIAL"

        expected = True
        actual = self.status.is_special()

        self.assertEqual(expected, actual)

    def test_is_not_special(self) -> None:
        """
        Tests the method which let us check if the current status is a not a
        special one.
        """

        self.status.status = "ACTIVE"
        self.status.status_source = "DNSLOOKUP"

        expected = False
        actual = self.status.is_special()

        self.assertEqual(expected, actual)

    def test_is_available(self) -> None:
        """
        Tests the method which let us check if the current status represent
        an available status.
        """

        self.status.status = "ACTIVE"
        self.status.status_source = "HTTP CODE"

        expected = True
        actual = self.status.is_available()

        self.assertEqual(expected, actual)

    def test_is_not_available(self) -> None:
        """
        Tests the method which let us check if the current represent a non-
        available status.
        """

        self.status.status = "INACTIVE"
        self.status.status_source = "STDLOOKUP"

        expected = False
        actual = self.status.is_available()

        self.assertEqual(expected, actual)

    def test_is_active(self) -> None:
        """
        Tests the method which let us check if the current status represent
        an active status.
        """

        self.status.status = "ACTIVE"
        self.status.status_source = "DNSLOOKUP"

        expected = True
        actual = self.status.is_active()

        self.assertEqual(expected, actual)

    def test_is_not_active(self) -> None:
        """
        Tests the method which let us check if the current represent a non-
        active status.
        """

        self.status.status = "INACTIVE"
        self.status.status_source = "DNSLOOKUP"

        expected = False
        actual = self.status.is_active()

        self.assertEqual(expected, actual)

    def test_is_inactive(self) -> None:
        """
        Tests the method which let us check if the current status represent
        an inactive status.
        """

        self.status.status = "INACTIVE"
        self.status.status_source = "DNSLOOKUP"

        expected = True
        actual = self.status.is_inactive()

        self.assertEqual(expected, actual)

    def test_is_not_inactive(self) -> None:
        """
        Tests the method which let us check if the current represent a non-
        inactive status.
        """

        self.status.status = "ACTIVE"
        self.status.status_source = "NETINFO"

        expected = False
        actual = self.status.is_inactive()

        self.assertEqual(expected, actual)

    def test_is_invalid(self) -> None:
        """
        Tests the method which let us check if the current status represent
        an invalid status.
        """

        self.status.status = "INVALID"
        self.status.status_source = "SYNTAX"

        expected = True
        actual = self.status.is_invalid()

        self.assertEqual(expected, actual)

    def test_is_not_invalid(self) -> None:
        """
        Tests the method which let us check if the current represent a non-
        invalid status.
        """

        self.status.status = "ACTIVE"
        self.status.status_source = "DNSLOOKUP"

        expected = False
        actual = self.status.is_invalid()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
