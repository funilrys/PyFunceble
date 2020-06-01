"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some test of PyFunceble.

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

from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble


class TestUs(TestCase):
    """
    Tests of PyFunceble.
    """

    def test_get_complements(self):
        """
        Tests of the method which is supposed to give us complements.
        """

        given = [
            "hello.example.com",
            "example.net",
            "hello.example.org",
            "www.example.org",
        ]

        expected = ["www.example.net", "example.org"]

        actual = PyFunceble.get_complements(given)

        self.assertEqual(expected, actual)

    def test_get_complements_include_given(self):
        """
        Tests of the method which is supposed to give us complements for the
        case that we want the given one in the result.
        """

        given = [
            "hello.example.com",
            "example.net",
            "hello.example.org",
            "www.example.org",
        ]

        expected = [
            "hello.example.com",
            "example.net",
            "www.example.net",
            "hello.example.org",
            "www.example.org",
            "example.org",
        ]

        actual = PyFunceble.get_complements(given, include_given=True)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
