"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our syntax checker base.

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

from PyFunceble.checker.syntax.base import SyntaxCheckerBase


class TestSyntaxCheckerBase(unittest.TestCase):
    """
    Tests of the base of all our syntax checker.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.checker = SyntaxCheckerBase()

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        del self.checker

    def test_subject_propagator(self) -> None:
        """
        Tests that the subject subjects and it's IDNA counterpart are correctly
        propagated.
        """

        given = "äxample.org"
        expected_subject = "äxample.org"
        expected_idna_subject = "xn--xample-9ta.org"

        self.checker.subject = given

        actual_subject = self.checker.status.subject
        actual_idna_subject = self.checker.status.idna_subject

        self.assertEqual(expected_subject, actual_subject)
        self.assertEqual(expected_idna_subject, actual_idna_subject)

        # Now, just make sure that when overwrite, the status get changed
        # propagated too.

        given = "äxample.net"
        expected_subject = "äxample.net"
        expected_idna_subject = "xn--xample-9ta.net"

        self.checker.subject = given

        actual_subject = self.checker.status.subject
        actual_idna_subject = self.checker.status.idna_subject

        self.assertEqual(expected_subject, actual_subject)
        self.assertEqual(expected_idna_subject, actual_idna_subject)

    def test_query_status_invalid(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the given dataset is invalid.
        """

        given = "äxample.org"
        self.checker.subject = given

        # The validator always return False.
        self.checker.is_valid = lambda: False

        expected_default_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_default_status, actual_status)

        self.checker.query_status()

        expected_status = "INVALID"
        expected_status_source = "SYNTAX"

        actual_status = self.checker.status.status
        actual_status_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_status_source, actual_status_source)

    def test_query_status_valid(self) -> None:
        """
        Tests the method which let us query the status for the case that
        the given dataset is valid.
        """

        given = "äxample.org"
        self.checker.subject = given

        # The validator always return True.
        self.checker.is_valid = lambda: True

        expected_default_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_default_status, actual_status)

        self.checker.query_status()

        expected_status = "VALID"
        expected_status_source = "SYNTAX"

        actual_status = self.checker.status.status
        actual_status_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_status_source, actual_status_source)


if __name__ == "__main__":
    unittest.main()
