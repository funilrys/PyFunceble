"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our digit 2 digits converter.

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


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

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

from PyFunceble.query.whois.converter.digit2digits import Digit2Digits


class TestDigit2Digits(unittest.TestCase):
    """
    Tests the digit2digits converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = Digit2Digits()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.converter

    def test_set_data_to_convert_not_str(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that it's not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_data_to_convert(given))

    def test_get_converted_already_formatted(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given data is already converted.
        """

        expected = "21"

        actual = self.converter.set_data_to_convert("21").get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_more_than_two_digits(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given data has more that 2 digits.
        """

        expected = "211"
        actual = self.converter.set_data_to_convert("211").get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
