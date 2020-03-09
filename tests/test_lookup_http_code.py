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
