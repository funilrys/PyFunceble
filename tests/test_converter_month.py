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

Tests of PyFunceble.converters.month

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
from PyFunceble.converter.month import Month


class TestMonth(TestCase):
    """
    Tests of PyFunceble.converters.month
    """

    def test_wrong_type(self):
        """
        Tests for the case that the wrong type is given.
        """

        self.assertRaises(
            PyFunceble.exceptions.WrongParameterType,
            lambda: Month(["January"]).get_converted(),
        )

        self.assertRaises(
            PyFunceble.exceptions.WrongParameterType, lambda: Month(1).get_converted()
        )

    def test_january(self):
        """
        Tests for the case that we given a representation of the January month.
        """

        given = ["jan", "Jan", "January", "01", "1", "Jan.", "jan."]
        expected = "jan"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_february(self):
        """
        Tests for the case that we given a representation of the February month.
        """

        given = ["feb", "Feb", "February", "02", "2", "Feb.", "feb."]
        expected = "feb"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_march(self):
        """
        Tests for the case that we given a representation of the March month.
        """

        given = ["mar", "Mar", "March", "03", "3", "Mar.", "mar."]
        expected = "mar"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_april(self):
        """
        Tests for the case that we given a representation of the April month.
        """

        given = ["apr", "Apr", "April", "04", "4", "Apr.", "apr."]
        expected = "apr"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_may(self):
        """
        Tests for the case that we given a representation of the May month.
        """

        given = ["may", "May", "05", "5"]
        expected = "may"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_june(self):
        """
        Tests for the case that we given a representation of the June month.
        """

        given = ["jun", "Jun", "June", "06", "6", "Jun.", "jun."]
        expected = "jun"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_july(self):
        """
        Tests for the case that we given a representation of the July month.
        """

        given = ["jul", "Jul", "July", "07", "7", "Jul.", "jul."]
        expected = "jul"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_august(self):
        """
        Tests for the case that we given a representation of the August month.
        """

        given = ["aug", "Aug", "August", "08", "8", "Aug.", "aug."]
        expected = "aug"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_september(self):
        """
        Tests for the case that we given a representation of the September month.
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
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_october(self):
        """
        Tests for the case that we given a representation of the October month.
        """

        given = ["oct", "Oct", "October", "10", "Oct.", "oct."]
        expected = "oct"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_november(self):
        """
        Tests for the case that we given a representation of the November month.
        """

        given = ["nov", "Nov", "November", "11", "Nov.", "nov."]
        expected = "nov"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)

    def test_december(self):
        """
        Tests for the case that we given a representation of the December month.
        """

        given = ["dec", "Dec", "December", "12", "Dec.", "dec."]
        expected = "dec"

        for data in given:
            actual = Month(data).get_converted()

            self.assertEqual(expected, actual, data)


if __name__ == "__main__":
    launch_tests()
