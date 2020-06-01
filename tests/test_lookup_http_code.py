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

Tests of PyFunceble.lookup.http_code

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
from unittest.mock import patch

import PyFunceble
from PyFunceble.lookup import HTTPCode


class TestHTTPCode(TestCase):
    """
    Tests of PyFunceble.lookup.http_code
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        PyFunceble.load_config()

        self.subject = "example.org"
        self.subject_type = "domain"

    def test_get_not_activated(self):
        """
        Tests the case that the end-user don't want it.
        """

        PyFunceble.HTTP_CODE.active = False

        expected = PyFunceble.HTTP_CODE.not_found_default
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.lookup.http_code.HTTPCode._get_it", return_value=200)
    def test_get_known_code(self, _):
        """
        Tests the case that we got a known value.
        """

        PyFunceble.HTTP_CODE.active = True

        expected = 200
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.lookup.http_code.HTTPCode._get_it", return_value=850)
    def test_unknown_code(self, _):
        """
        Tests the case thwe got an unknown value.
        """

        PyFunceble.HTTP_CODE.active = True

        expected = PyFunceble.HTTP_CODE.not_found_default
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.lookup.http_code.HTTPCode._get_it", return_value=None)
    def test_not_found_or_timeout_output(self, _):
        """
        Tests the case that we could not find it.
        """

        PyFunceble.HTTP_CODE.active = True

        expected = PyFunceble.HTTP_CODE.not_found_default
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
