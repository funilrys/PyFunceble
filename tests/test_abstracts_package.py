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
