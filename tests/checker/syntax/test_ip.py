"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our IP (v4 and v6) syntax checker.

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

from PyFunceble.checker.syntax.ip import IPSyntaxChecker

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset


class TestIPSyntaxChecker(unittest.TestCase):
    """
    Tests of our IP (v4 and v6) syntax checker.
    """

    def test_is_valid_v4(self) -> None:
        """
        Tests the method which let us check if the given subject is valid.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV4:
            actual = ip_checker.set_subject(subject).is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_valid_v6(self) -> None:
        """
        Tests the method which let us check if the given subject is valid.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV6:
            ip_checker.subject = subject
            actual = ip_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_v4(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not valid.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_IPV4:
            ip_checker.subject = subject
            actual = ip_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_v6(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not valid.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_IPV6:
            ip_checker.subject = subject
            actual = ip_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_valid_range_v4(self) -> None:
        """
        Tests the method which let us check if the given subject is valid range.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV4_RANGES:
            ip_checker.subject = subject
            actual = ip_checker.is_valid_range()

            self.assertEqual(expected, actual, subject)

    def test_is_valid_range_v6(self) -> None:
        """
        Tests the method which let us check if the given subject is valid range.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV6_RANGES:
            ip_checker.subject = subject
            actual = ip_checker.is_valid_range()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_range_v4(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not a valid range.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_IPV4_RANGES:
            ip_checker.subject = subject
            actual = ip_checker.is_valid_range()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid_range(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not a valid range.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_VALID_IPV6_RANGES:
            ip_checker.subject = subject
            actual = ip_checker.is_valid_range()

            self.assertEqual(expected, actual, subject)

    def test_is_reserved_v4(self) -> None:
        """
        Tests the method which let us check if the given subject is reserved.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.RESERVED_IPV4:
            ip_checker.subject = subject
            actual = ip_checker.is_reserved()

            self.assertEqual(expected, actual, subject)

    def test_is_reserved_v6(self) -> None:
        """
        Tests the method which let us check if the given subject is reserved.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.RESERVED_IPV6:
            ip_checker.subject = subject
            actual = ip_checker.is_reserved()

            self.assertEqual(expected, actual, subject)

    def test_is_not_reserved_v4(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not reserved.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_RESERVED_IPV4:
            ip_checker.subject = subject
            actual = ip_checker.is_reserved()

            self.assertEqual(expected, actual, subject)

    def test_is_not_reserved_v6(self) -> None:
        """
        Tests the method which let us check if the given subject is valid for
        the case that the given subject is not reserved.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in pyf_test_dataset.NOT_RESERVED_IPV6:
            ip_checker.subject = subject
            actual = ip_checker.is_reserved()

            self.assertEqual(expected, actual, subject)

    def test_is_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid
        IPv4 or IPv6.
        """

        ip_checker = IPSyntaxChecker()

        expected = True

        for subject in pyf_test_dataset.VALID_IPV4 + pyf_test_dataset.VALID_IPV6:
            ip_checker.subject = subject
            actual = ip_checker.is_valid()

            self.assertEqual(expected, actual, subject)

    def test_is_not_valid(self) -> None:
        """
        Tests the method which let us check if the given subject is valid
        IPv4 or IPv6 for the case that is not a valid IPv4 or IPv6.
        """

        ip_checker = IPSyntaxChecker()

        expected = False

        for subject in (
            pyf_test_dataset.NOT_VALID_IPV4 + pyf_test_dataset.NOT_VALID_IPV6
        ):
            ip_checker.subject = subject
            actual = ip_checker.is_valid()

            self.assertEqual(expected, actual, subject)


if __name__ == "__main__":
    unittest.main()
