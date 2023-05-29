"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our CIDR to subject converter.

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
from collections import Counter

from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.converter.cidr2subject import CIDR2Subject


class TestCIDR2Subject(unittest.TestCase):
    """
    Tests our CIDR 2 subject converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = CIDR2Subject()

    def tearDown(self) -> None:
        """
        Destroys everything previously created for the tests.
        """

        del self.converter

    def test_init_with_helper(self) -> None:
        """
        Tests the initialization with our own helpers.
        """

        ip_syntax_checker = IPSyntaxChecker()
        self.converter = CIDR2Subject(ip_syntax_checker=ip_syntax_checker)

        self.assertIsInstance(self.converter.ip_syntax_checker, IPSyntaxChecker)
        self.assertEqual(id(ip_syntax_checker), id(self.converter.ip_syntax_checker))

    def test_set_data_to_convert_no_string(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that a non-string value is given.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_data_to_convert(given))

    def test_get_converted_empty(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        it's an empty string is given.
        """

        given = ""
        expected = []

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted(self) -> None:
        """
        Tests the method which let us get the converted data.
        """

        given = "127.0.30.0/28"
        expected = [f"127.0.30.{x}" for x in range(0, 15 + 1)]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertTrue(Counter(expected) == Counter(actual))

    def test_get_converted_not_cidr(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given subject is not a CIDR address.
        """

        given = "example.org"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_not_cidr_bis(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given subject is not a CIDR address (bis).
        """

        given = "127.0.0.1"
        expected = ["127.0.0.1"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_not_correct(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given subject is not a correct CIDR address.
        """

        given = "127.0.0.0/3"
        expected = ["127.0.0.0/3"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_ipv6(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given subject is an IPv6.

        In this case, we check that no conversion is actually made.
        """

        given = "2001:4860:4860::/64"
        expected = ["2001:4860:4860::/64"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
