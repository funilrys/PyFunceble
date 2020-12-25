"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our wildcard to subject converter.

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

from PyFunceble.converter.wildcard2subject import Wildcard2Subject


class TestWildcard2Subject(unittest.TestCase):
    """
    Tests our wildcard 2 subject converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = Wildcard2Subject()

    def tearDown(self) -> None:
        """
        Destroys everything previously created for the tests.
        """

        del self.converter

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
        expected = None

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted(self) -> None:
        """
        Tests the method which let us get the converted data.
        """

        given = "*.example.org"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_not_wildcard(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given subject is not a wildcard.
        """

        given = "example.org"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_wildcard_at_end(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the wildcard is located at the end.
        """

        given = "example.org.*"
        expected = "example.org.*"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_wildcard_both_end(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the wildcard is located at the both end.
        """

        given = "*.example.org.*"
        expected = "example.org.*"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
