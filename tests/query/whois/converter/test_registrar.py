"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our registrar extractor.

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

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import unittest
from typing import List

from PyFunceble.query.whois.converter.registrar import RegistarExtractor


class TestRegistrarExtractor(unittest.TestCase):
    """
    Tests the interface for the extration of expiration date.
    """

    REGISTRAR_SAMPLES: List[str] = [
        "Hello, Inc.",
        "Alphabet, Inc.",
        "Example, Inc.",
        "Google, Inc.",
    ]

    REGISTRAR_MARKERS: List[str] = [
        "Authorized Agency    :",
        "Domain Support:",
        "Registrar:",
        "Registrar       :",
        "Registrar...........:",
        "Registration Service Provider      :",
        "Sponsoring Registrar :",
        "Sponsoring Registrar Organization :",
    ]

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = RegistarExtractor()

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

    def test_set_data_to_convert_empty_str(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that it's an empty string.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.converter.set_data_to_convert(given))

    def test_get_converted(self) -> None:
        """
        Tests the method that let us get the registrar part.
        """

        for marker in self.REGISTRAR_MARKERS:
            for sample in self.REGISTRAR_SAMPLES:
                expected = sample

                test_line = f"{marker} {sample}"

                self.converter.data_to_convert = test_line
                actual = self.converter.get_converted()

                self.assertEqual(expected, actual, test_line)

    def test_get_converted_no_pattern(self) -> None:
        """
        Tests the method that let us get the registrar part.
        """

        given = "Hello, World!"
        expected = None

        self.converter.data_to_convert = given

        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_empty_registrar(self) -> None:
        """
        Tests the method that let us get the registrar part for the case that
        the registrar is empty.
        """

        expected = None

        for marker in self.REGISTRAR_MARKERS:
            test_line = f"{marker}     "

            self.converter.data_to_convert = test_line
            actual = self.converter.get_converted()

            self.assertEqual(expected, actual, test_line)


if __name__ == "__main__":
    unittest.main()
