"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our domain checker base.

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


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

from PyFunceble.checker.syntax.domain_base import DomainSyntaxCheckerBase


class TestSDomainSyntaxCheckerBase(unittest.TestCase):
    """
    Tests of the base of all our domain syntax checker.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.checker = DomainSyntaxCheckerBase()

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        del self.checker

    def test_get_last_point_index(self) -> None:
        """
        Tests the method which let us get the position of the last point
        of a given subject.

        In this test, we test for a normal subject.
        """

        given = "example.org"

        # Just initizalize the whole this as usual.
        self.checker.subject = given

        expected = 7
        actual = self.checker.get_last_point_index(given)

        self.assertEqual(expected, actual)

    def test_get_last_point_index_ends_with_point(self) -> None:
        """
        Tests the method which let us get the position of the last point
        of a given subject.

        In this test, we test for a subject which ends with a point.
        """

        given = "example.org."

        # Just initizalize the whole this as usual.
        self.checker.subject = given

        expected = 7
        actual = self.checker.get_last_point_index(given)

        self.assertEqual(expected, actual)

    def test_get_last_point_index_no_point(self) -> None:
        """
        Tests the method which let us get the position of the last point
        of a given subject.

        In this test, we test for an INVALID subject (no point at all).
        """

        given = "example"

        # Just initizalize the whole this as usual.
        self.checker.subject = given

        expected = None
        actual = self.checker.get_last_point_index(given)

        self.assertEqual(expected, actual)

    def test_get_extension(self) -> None:
        """
        Tests the method which let us get the extension of the currently
        loaded subject.
        """

        given = "example.org"

        self.checker.subject = given

        expected = "org"
        actual = self.checker.get_extension()

        self.assertEqual(expected, actual)

    def test_get_extension_ends_with_point(self) -> None:
        """
        Tests the method which let us get the extension of the currently
        loaded subject.

        In this test, we give a subject which ends with a point.
        """

        given = "example.org."

        self.checker.subject = given

        expected = "org"
        actual = self.checker.get_extension()

        self.assertEqual(expected, actual)

    def test_get_extension_ends_no_point(self) -> None:
        """
        Tests the method which let us get the extension of the currently
        loaded subject.

        In this test, we give a subject which in INVALID (no point).
        """

        given = "example"

        self.checker.subject = given

        expected = None
        actual = self.checker.get_extension()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
