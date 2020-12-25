"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our subdomain checker.

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

from PyFunceble.checker.syntax.subdomain import SubDomainSyntaxChecker

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset


class TestSubSubDomainSyntaxChecker(unittest.TestCase):
    """
    Tests of our subdomain syntax checker.
    """

    def test_is_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid.
        """

        subdomain_checker = SubDomainSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_SUBDOMAINS:
            actual = subdomain_checker.set_subject(subject).is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_valid_ends_with_point(self) -> None:
        """
        Tests the method which let us check if the given subject is valid.
        """

        subdomain_checker = SubDomainSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_SUBDOMAINS:
            subdomain_checker.subject = f"{subject}."
            actual = subdomain_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not valid.
        """

        subdomain_checker = SubDomainSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_SUBDOMAINS:
            subdomain_checker.subject = subject
            actual = subdomain_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_not_extension(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject has no valid extension.
        """

        expected = False

        given = "example"
        actual = SubDomainSyntaxChecker(given).is_valid()

        self.assertEqual(expected, actual)

    def test_is_not_valid_not_rfc_compliant(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not RFC compliant.
        """

        expected = False

        given = "example.hello_world.org"
        actual = SubDomainSyntaxChecker(given).is_valid()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
