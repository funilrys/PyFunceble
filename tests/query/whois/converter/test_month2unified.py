"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our month converter.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

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

from PyFunceble.query.whois.converter.month2unified import Month2Unified


class TestMonth2Unified(unittest.TestCase):
    """
    Tests our month converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = Month2Unified()

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

    def test_get_converted_no_month(self):
        """
        Tests the method which let us get the converted month for the case that
        no actual month is given.
        """

        given = "Hello, World!"

        expected = "Hello, World!"
        actual = self.converter.set_data_to_convert(given).get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_january(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the January month.
        """

        given = ["jan", "Jan", "January", "01", "1", "Jan.", "jan."]
        expected = "jan"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual)

    def test_get_converted_february(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the February month.
        """

        given = ["feb", "Feb", "February", "02", "2", "Feb.", "feb."]
        expected = "feb"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_march(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the March month.
        """

        given = ["mar", "Mar", "March", "03", "3", "Mar.", "mar."]
        expected = "mar"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_april(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the April month.
        """

        given = ["apr", "Apr", "April", "04", "4", "Apr.", "apr."]
        expected = "apr"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_may(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the May month.
        """

        given = ["may", "May", "05", "5"]
        expected = "may"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_june(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the June month.
        """

        given = ["jun", "Jun", "June", "06", "6", "Jun.", "jun."]
        expected = "jun"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_july(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the July month.
        """

        given = ["jul", "Jul", "July", "07", "7", "Jul.", "jul."]
        expected = "jul"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_august(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the August month.
        """

        given = ["aug", "Aug", "August", "08", "8", "Aug.", "aug."]
        expected = "aug"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_september(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the September month.
        """

        given = [
            "sep",
            "Sep",
            "sept",
            "Sept",
            "September",
            "09",
            "9",
            "Sept.",
            "sept.",
            "Sep.",
            "sep.",
        ]
        expected = "sep"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_october(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the October month.
        """

        given = ["oct", "Oct", "October", "10", "Oct.", "oct."]
        expected = "oct"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_november(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the November month.
        """

        given = ["nov", "Nov", "November", "11", "Nov.", "nov."]
        expected = "nov"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_get_converted_december(self):
        """
        Tests the method which let us get the converted month for the case that
        we give a representation of the December month.
        """

        given = ["dec", "Dec", "December", "12", "Dec.", "dec."]
        expected = "dec"

        for data in given:
            actual = self.converter.set_data_to_convert(data).get_converted()

            self.assertEqual(expected, actual, data)


if __name__ == "__main__":
    unittest.main()
