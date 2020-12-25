"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the base of all our converters.

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

from PyFunceble.converter.base import ConverterBase


class TestConverterBase(unittest.TestCase):
    """
    Tests the base of all our converters.
    """

    def setUp(self) -> None:
        """
        Setups everything needed.
        """

        self.converter = ConverterBase()

    def tearDown(self) -> None:
        """
        Destroys everything that was needed.
        """

        del self.converter

    def test_set_data_to_convert_return(self) -> None:
        """
        Tests the response from the method which let us set the data to work with.
        """

        given = "example.com"

        actual = self.converter.set_data_to_convert(given)

        self.assertIsInstance(actual, ConverterBase)

    def test_set_data_to_convert_method(self) -> None:
        """
        Tests the method which let us set the data to work with.
        """

        given = "example.com"
        expected = "example.com"

        self.converter.set_data_to_convert(given)

        actual = self.converter.data_to_convert

        self.assertEqual(expected, actual)

    def test_set_data_to_convert_attribute(self) -> None:
        """
        Tests overwritting of the :code:`data_to_convert` attribute.
        """

        given = "example.com"
        expected = "example.com"

        self.converter.data_to_convert = given
        actual = self.converter.data_to_convert

        self.assertEqual(expected, actual)

    def test_set_data_to_convert_through_init(self) -> None:
        """
        Tests the overwritting of the data to work through the class constructor.
        """

        given = "example.com"
        expected = "example.com"

        converter = ConverterBase(given)
        actual = converter.data_to_convert

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
