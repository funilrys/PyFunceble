"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the input line 2 subject converter.

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

from PyFunceble.converter.input_line2subject import InputLine2Subject


class TestInputLine2Subject(unittest.TestCase):
    """
    Tests our input line 2 subject converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = InputLine2Subject()

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

    def test_get_converted_simple_line(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        simple line is given.
        """

        given = "example.org"
        expected = [given]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_comment(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        commented line is given.
        """

        given = "# example.org"
        expected = list()

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_end_with_comment(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        comment at the end of a line is given.
        """

        given = "example.org # Hello, World!"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_hosts_line(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        hosts (file) line is given.
        """

        given = "0.0.0.0 example.org"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_hosts_line_multiple_subject(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        compressed hosts (file) line is given.
        """

        given = "0.0.0.0 example.org example.net example.de example.co.uk"
        expected = ["example.org", "example.net", "example.de", "example.co.uk"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_hosts_line_spaces(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        hosts (file) line with spaces as separator is given.
        """

        given = "0.0.0.0        example.org"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_hosts_line_tab(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        hosts (file) line with tab as separator is given.
        """

        given = "0.0.0.0\texample.org"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_hosts_line_tabs(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        hosts (file) line with tabs as separator is given.
        """

        given = "0.0.0.0\t\t\t\t\texample.org"
        expected = ["example.org"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_multiple_entries(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a line with multiple entries (not hosts file format) are given.
        """

        given = "example.org example.net example.de example.co.uk"
        expected = ["example.org", "example.net", "example.de", "example.co.uk"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_rfc_6367(self) -> None:
        """
        Tests the method which let us get the converted data for the case that a
        line with :code:`\032` as separator is given.
        """

        given = "0.0.0.0\t\t\t\t\texample.org\\032example.net"
        expected = ["example.org", "example.net"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
