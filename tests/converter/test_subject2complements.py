"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of subject to complements converter.

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

from PyFunceble.converter.subject2complements import Subject2Complements


class TestRPZInputLine2Subject(unittest.TestCase):
    """
    Tests of our RPZ line 2 subject(s).
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = Subject2Complements()

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

    def test_set_include_given_return(self) -> None:
        """
        Tests the response from the method which let us activate the
        inclusion of the given subject into the result.
        """

        given = True

        actual = self.converter.set_include_given(given)

        self.assertIsInstance(actual, Subject2Complements)

    def test_set_include_given_method(self) -> None:
        """
        Tests the method which let us set activate the inclusion of the
        given subject into the result.
        """

        given = True
        expected = True

        self.converter.set_include_given(given)

        actual = self.converter.include_given

        self.assertEqual(expected, actual)

    def test_set_include_given_attribute(self) -> None:
        """
        Tests overwritting of the :code:`include_given` attribute.
        """

        given = True
        expected = True

        self.converter.include_given = given
        actual = self.converter.include_given

        self.assertEqual(expected, actual)

    def test_set_include_given_through_init(self) -> None:
        """
        Tests the activation of the inclusion of the given subject into the
        result through the class constructor.
        """

        given = True
        expected = True

        converter = Subject2Complements(include_given=given)
        actual = converter.include_given

        self.assertEqual(expected, actual)

    def test_set_include_given_not_bool(self) -> None:
        """
        Tests the response from the method which let us activate the inclusion
        of the given subject into the result for the case that the given
        value is not a boolean.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_include_given(given))

    def test_get_converted(self) -> None:
        """
        Tests the conversion for the case that a non-www subdomain is given.
        """

        given = "example.org"
        expected = ["www.example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_starts_with_www(self) -> None:
        """
        Tests the conversion for the case that a www subdomain is given.
        """

        given = "www.example.org"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_include_given(self) -> None:
        """
        Tests the conversion for the case that we want the given subject to
        be included in the result.
        """

        given = "www.example.org"
        # We expect the given to always be the first index.
        expected = ["www.example.org", "example.org"]

        self.converter.include_given = True
        self.converter.data_to_convert = given

        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
