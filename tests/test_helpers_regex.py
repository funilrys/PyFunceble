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

Tests of the PyFunceble.helpers.regex

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long

from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.helpers import Regex


class TestRegex(TestCase):
    """
    Tests of the PyFunceble.helpers.regex.
    """

    def setUp(self):
        """
        Setups everything needed for the test.
        """

        self.data_list = [
            "hello",
            "world",
            "funilrys",
            "funceble",
            "PyFunceble",
            "pyfunceble",
        ]
        self.data = "Hello, this is Fun Ilrys. I just wanted to know how things goes around the tests."  # pylint: disable=line-too-long

    def test_not_matching_list(self):
        """
        Tests the method which let us get a list of non
        matching strin from a given list of string.
        """

        regex = "fun"
        expected = ["hello", "world", "PyFunceble"]
        actual = Regex(regex).get_not_matching_list(self.data_list)

        self.assertEqual(expected, actual)

    def test_matching_list(self):
        """
        Tests the method which let us get a list of
        matchint string from a given list of string.
        """

        regex = "fun"
        expected = ["funilrys", "funceble", "pyfunceble"]
        actual = Regex(regex).get_matching_list(self.data_list)

        self.assertEqual(expected, actual)

    def test_match_rematch(self):
        """
        Tests the matching method for the case that we want to rematch
        the different groups.
        """

        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = "is"
        actual = Regex(regex).match(self.data, rematch=True, group=1)

        self.assertEqual(expected, actual)

    def test_match_get_group(self):
        """
        Tests the matching method for the case that we want
        a specific group.
        """

        regex = "e"
        expected = "e"
        actual = Regex(regex).match(self.data, group=0)

        self.assertEqual(expected, actual)

        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = "this"
        actual = Regex(regex).match(self.data, group=1)

        self.assertEqual(expected, actual)

    def test_replace_no_replacement(self):
        """
        Tests the replacement method for the case that we replacement
        is not given.
        """

        regex = "th"
        expected = self.data
        actual = Regex(regex).replace_match(self.data, None)

        self.assertEqual(expected, actual)

    def test_replace(self):
        """
        Tests the replacement method.
        """

        regex = "th"
        expected = "Hello, htis is Fun Ilrys. I just wanted to know how htings goes around hte tests."  # pylint: disable=line-too-long
        actual = Regex(regex).replace_match(self.data, "ht")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
