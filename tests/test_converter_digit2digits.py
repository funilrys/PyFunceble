# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.converters.digit2digits

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
# pylint: enable=line-too-long
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.converter.digit2digits import Digit2Digits


class TestDigit2Digits(TestCase):
    """
    Tests of PyFunceble.converters.digit2digits
    """

    def test_wrong_type(self):
        """
        Tests for the case that the wrong type is given.
        """

        self.assertRaises(
            PyFunceble.exceptions.WrongParameterType,
            lambda: Digit2Digits(["1"]).get_converted(),
        )

        self.assertRaises(
            PyFunceble.exceptions.WrongParameterType,
            lambda: Digit2Digits(1).get_converted(),
        )

    def test_simple_input(self):
        """
        Tests of the class.
        """

        expected = "01"
        actual = Digit2Digits("1").get_converted()

        self.assertEqual(expected, actual)

    def test_already_digits(self):
        """
        Tests of the class for the case that we already have 2 digits.
        """

        expected = "21"
        actual = Digit2Digits("21").get_converted()

        self.assertEqual(expected, actual)

    def test_more_than_two_digits(self):
        """
        Tests of the class for the case that we already have more than 2 digits.
        """

        expected = "211"
        actual = Digit2Digits("211").get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
