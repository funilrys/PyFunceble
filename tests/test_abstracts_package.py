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

Tests of PyFunceble.abstracts.package

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

from PyFunceble.abstracts import Version


class TestVersion(TestCase):
    """
    Tests of PyFunceble.abstracts.Version
    """

    def test_split_version(self):
        """
        Tests the case that we want to split the version.
        """

        given = "1.0.0.dev (Hello, World!)"
        expected = ["1", "0", "0"]
        actual = Version.split_versions(given)

        self.assertEqual(expected, actual)

    def test_split_version_with_non_digits(self):
        """
        Tests the case that we want to split the version
        but also have the code name.
        """

        given = "1.0.0.dev (Hello, World!)"
        expected = (["1", "0", "0"], "dev (Hello, World!)")
        actual = Version.split_versions(given, return_non_digits=True)

        self.assertEqual(expected, actual)

    def test_literal_comparison(self):
        """
        Tests the literal comparison.
        """

        given = "1.0.0.dev (Hello, World!)"
        expected = True
        actual = Version.literally_compare(given, given)

        self.assertEqual(expected, actual)

    def test_literal_comparison_different(self):
        """
        Tests the litaral comparison for the case that both given version are different.
        """

        given = "1.0.0.dev (Hello, World!)"
        expected = False
        actual = Version.literally_compare(given, given.replace(".", "_"))

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "1.0.0.dev (Hello, World)")
    def test_compare_local_version_is_same(self):
        """
        Tests the comparison for the case that the local version is older.
        """

        given = "1.0.0.dev (Hello, World)"
        expected = None
        actual = Version.compare(given)

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "1.50.0.dev (Hello, World)")
    def test_compare_local_version_is_older(self):
        """
        Tests the comparison for the case that the local version is older.
        """

        given = "2.34.0.dev (Hello, World)"
        expected = True
        actual = Version.compare(given)

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "2.10.0.dev (Hello, World)")
    def test_compare_local_version_is_newer(self):
        """
        Tests the comparison for the case that the local version is older.
        """

        given = "1.15.0.dev (Hello, World)"
        expected = False
        actual = Version.compare(given)

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "2.10.0.dev (Hello, World)")
    def test_is_local_dev(self):
        """
        Tests if the local version is the dev one.
        """

        expected = True
        actual = Version.is_local_dev()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "2.10.0. (Hello, World)")
    def test_is_not_local_dev(self):
        """
        Tests if the local version is the not the dev one.
        """

        expected = False
        actual = Version.is_local_dev()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
