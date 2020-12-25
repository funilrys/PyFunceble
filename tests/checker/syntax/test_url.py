"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our url syntax checker.

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

from PyFunceble.checker.syntax.url import URLSyntaxChecker

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset


class TestURLSyntaxChecker(unittest.TestCase):
    """
    Tests of our URL syntax checker.
    """

    def test_is_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid.
        """

        url_checker = URLSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_DOMAINS:
            url_checker.subject = f"https://{subject}/?is_admin=true"

            actual = url_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_valid_subdomain(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that a subdomain is given.
        """

        url_checker = URLSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_SUBDOMAINS:
            url_checker.subject = f"https://{subject}/?is_admin=true"
            actual = url_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not valid.
        """

        url_checker = URLSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_DOMAINS:
            url_checker.subject = f"{subject}/?is_admin=true"
            actual = url_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_not_extension(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject has no valid extension.
        """

        expected = False

        given = "http://example"
        actual = URLSyntaxChecker(given).is_valid()

        self.assertEqual(expected, actual)

    def test_is_not_valid_not_rfc_compliant(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not RFC compliant.
        """

        expected = False

        given = "http://example.hello_world.org"
        actual = URLSyntaxChecker(given).is_valid()

        self.assertEqual(expected, actual)

    def test_is_not_valid_no_scheme(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that no scheme is given.
        """

        url_checker = URLSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.VALID_DOMAINS:
            subject = f"{subject}/?is_admin=true"
            actual = url_checker.set_subject(subject).is_valid()

            self.assertEqual(expected, actual, subject)


if __name__ == "__main__":
    unittest.main()
