# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.converters.rpz2subject

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import pyf_test_dataset
import pyf_test_helpers

from PyFunceble.converter.rpz2subject import RPZ2Subject


class TestRPZ2Subject(TestCase):
    """
    Tests of PyFunceble.converter.rpz2subject
    """

    def test_empty_string(self):
        """
        Tests of RPZ2Subject for the case that an empty string is given.
        """

        given = ""
        expected = None
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_simple_domain(self):
        """
        Tests of RPZ2Subject for the case that a simple domain is given.
        """

        given = "example.org"
        expected = "example.org"
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_comment(self):
        """
        Tests of RPZ2Subject for the case that a comment is given.
        """

        given = "; Hello, World!"
        expected = None
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_simple_commented_domain(self):
        """
        Tests of RPZ2Subject for the case that a domain along with a comment
        is given.
        """

        given = "example.org. ; Hello, World!"
        expected = "example.org."
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_wildcard(self):
        """
        Tests of RPZ2subject for the case that a wildcard entry is given.
        """

        given = "*.example.org"
        expected = "example.org"
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_rpz_nsdname(self):
        """
        Tests of RPZ2subject for the case that the :code:`.rpz-nsdname` policy
        is given.
        """

        given = "example.org.rpz-nsdname"
        expected = "example.org"
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_wildcard_rpz_nsdname(self):
        """
        Tests of RPZ2Subject for the case that the :code:`.rpz-nsdname` policy
        is given along with a wildcard.
        """

        given = "*.example.org.rpz-nsdname"
        expected = "example.org"
        actual = RPZ2Subject(given).get_converted()

        self.assertEqual(expected, actual)

    def test_rpz_client_ip_ipv4(self):
        """
        Tests of a RPZ2Subject for the case that the :code:`rpz-client-ip`
        policy is given along with an IPv4.
        """

        for valid_ip in pyf_test_dataset.VALID_IPV4:
            given = f"{pyf_test_helpers.convert_ipv4_to_rpz(valid_ip)}.rpz-client-ip"
            expected = valid_ip

            actual = RPZ2Subject(given).get_converted()

            self.assertEqual(
                expected,
                actual,
                msg=f"expected: {expected!r} "
                f"| given: {given!r} "
                f"| got: {actual!r}",
            )

    def test_rpz_client_ip_ipv6(self):
        """
        Tests of a RPZ2Subject for the case that the :code:`rpz-client-ip`
        policy is given along with an IPv6.
        """

        for valid_ip in pyf_test_dataset.VALID_IPV6:

            given = f"{pyf_test_helpers.convert_ipv6_to_rpz(valid_ip)}.rpz-client-ip"
            expected = valid_ip

            actual = RPZ2Subject(given).get_converted()

            self.assertEqual(
                expected,
                actual,
                msg=f"expected: {expected!r} "
                f"| given: {given!r} "
                f"| got: {actual!r}",
            )


if __name__ == "__main__":
    launch_tests()
