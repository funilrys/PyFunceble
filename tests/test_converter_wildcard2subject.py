# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.converters.wildcard2subject

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

from PyFunceble.converter.wildcard2subject import Wildcard2Subject


class TestWildcard2Subject(TestCase):
    """
    Tests of PyFunceble.converter.wildcard2subject
    """

    def test_empty_string(self):
        """
        Tests of Wildcard2Subject for the case that an empty string is given.
        """

        given = ""
        expected = None
        actual = Wildcard2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_wildcard(self):
        """
        Test of Wildcard2Subject for the case that a wildcard is given.
        """

        given = "*.example.org"
        expected = "example.org"
        actual = Wildcard2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_wildcard_at_the_end(self):
        """
        Test of Wildcard2Subject for the case that the wildcard is at the end
        of the given string.
        """

        given = "example.org.*"
        expected = "example.org.*"
        actual = Wildcard2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_wildcard_on_both_end(self):
        """
        Test of Wildcard2Subject for the case that the wildcard is at both
        end of the given string.
        """

        given = "*.example.org.*"
        expected = "example.org.*"
        actual = Wildcard2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_no_wildcard(self):
        """
        Test of Wildcard2Subject for the case that no wildcard is given.
        """

        given = "example.org"
        expected = "example.org"
        actual = Wildcard2Subject(given).get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
