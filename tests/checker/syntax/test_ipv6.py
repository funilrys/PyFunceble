"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our IPv6 syntax checker.

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

from PyFunceble.checker.syntax.ipv6 import IPv6SyntaxChecker

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset


class TestIPv6SyntaxChecker(unittest.TestCase):
    """
    Tests of our IPv6 syntax checker.
    """

    def test_is_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid.
        """

        ipv6_checker = IPv6SyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV6:
            actual = ipv6_checker.set_subject(subject).is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not valid.
        """

        ipv6_checker = IPv6SyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_IPV6:
            ipv6_checker.subject = subject
            actual = ipv6_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_valid_range(self) -> None:
        """
        Tests the method which let us check if the given subject is valid range.
        """

        ipv6_checker = IPv6SyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV6_RANGES:
            ipv6_checker.subject = subject
            actual = ipv6_checker.is_valid_range()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_range(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not a valid range.
        """

        ipv6_checker = IPv6SyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_IPV6_RANGES:
            ipv6_checker.subject = subject
            actual = ipv6_checker.is_valid_range()

            self.assertEqual(expected, actual, subject)

    def test_is_reserved(self) -> None:
        """
        Tests the method which let us check if the given subject is reserved.
        """

        ipv6_checker = IPv6SyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.RESERVED_IPV6:
            ipv6_checker.subject = subject
            actual = ipv6_checker.is_reserved()

            self.assertEqual(expected, actual, subject)

    def test_is_not_reserved(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not reserved.
        """

        ipv6_checker = IPv6SyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_RESERVED_IPV6:
            ipv6_checker.subject = subject
            actual = ipv6_checker.is_reserved()

            self.assertEqual(expected, actual, subject)


if __name__ == "__main__":
    unittest.main()
