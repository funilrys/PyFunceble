"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our status syntax status handler.

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

from PyFunceble.checker.syntax.status import SyntaxCheckerStatus


class TestSyntaxCheckerStatus(unittest.TestCase):
    """
    Tests of our status handler.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.status = SyntaxCheckerStatus(subject="example.org")

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        del self.status

    def test_is_valid(self) -> None:
        """
        Tests the status method which let us fast check if it is describing
        a valid subject.
        """

        expected = True

        self.status.status = "VALID"

        actual = self.status.is_valid()

        self.assertEqual(expected, actual)

    def test_is_not_valid(self) -> None:
        """
        Tests the status method which let us fast check if it is describing
        a valid subject. But, for the case that it is not actually VALID.
        """

        expected = False

        self.status.status = "ACTIVE"

        actual = self.status.is_valid()

        self.assertEqual(expected, actual)

    def test_is_invalid(self) -> None:
        """
        Tests the status method which let us fast check if it is describing
        an invalid subject.
        """

        expected = True

        self.status.status = "INVALID"

        actual = self.status.is_invalid()

        self.assertEqual(expected, actual)

    def test_is_not_invalid(self) -> None:
        """
        Tests the status method which let us fast check if it is describing
        a valid subject. But, for the case that it is not actually INVALID.
        """

        expected = False

        self.status.status = "MALICIOUS"

        actual = self.status.is_invalid()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
