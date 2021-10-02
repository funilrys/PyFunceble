"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our reputation checker base.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/latest/

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

import unittest

from PyFunceble.checker.reputation.base import ReputationCheckerStatus

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset


try:
    import reputation_test_base
except ModuleNotFoundError:  # pragma: no cover
    from . import reputation_test_base


class TestReputationCheckerBase(reputation_test_base.ReputationCheckerTestBase):
    """
    Tests of the base of all our reputation checker.
    """

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
        actual_idna_propagated = [
            self.checker.status.idna_subject,
            self.checker.dns_query_tool.subject,
            self.checker.domain_syntax_checker.subject,
            self.checker.ip_syntax_checker.subject,
            self.checker.url_syntax_checker.subject,
        ]

        self.assertEqual(expected_subject, actual_subject)

        for actual in actual_idna_propagated:
            self.assertEqual(expected_idna_subject, actual)

        # Now, just make sure that when overwrite, the status get changed
        # propagated too.

        given = "äxample.net"
        expected_subject = "äxample.net"
        expected_idna_subject = "xn--xample-9ta.net"

        self.checker.subject = given

        actual_subject = self.checker.status.subject

        actual_idna_propagated = [
            self.checker.status.idna_subject,
            self.checker.dns_query_tool.subject,
            self.checker.domain_syntax_checker.subject,
            self.checker.ip_syntax_checker.subject,
            self.checker.url_syntax_checker.subject,
        ]

        self.assertEqual(expected_subject, actual_subject)

        for actual in actual_idna_propagated:
            self.assertEqual(expected_idna_subject, actual)

    def test_should_we_continue_test_negative(self) -> None:
        """
        Tests the method which let us know if we need to continue to the next
        test method.
        """

        given = "VALID"

        self.checker.status.status = "INACTIVE"

        expected = False
        actual = self.checker.should_we_continue_test(given)

        self.assertEqual(expected, actual)

    def test_should_we_continue_test_positive(self) -> None:
        """
        Tests the method which let us know if we need to continue to the next
        test method.
        """

        given = "INVALID"

        self.checker.status.status = "INACTIVE"

        expected = True
        actual = self.checker.should_we_continue_test(given)

        self.assertEqual(expected, actual)

    def test_query_syntax_checker(self) -> None:
        """
        Tests the method which check and share the syntax check.
        """

        # We are just checking that the key are present and that they have a
        # plausible value. We actually don't really care about the value as
        # we completely test the syntax checker.

        for subject in pyf_test_dataset.VALID_SECOND_LVL_DOMAINS:
            self.checker.subject = subject

            self.checker.query_syntax_checker()

            # pylint: disable=line-too-long
            expected_true = {
                "status.second_level_domain_syntax": self.checker.status.second_level_domain_syntax,
                "status.domain_syntax": self.checker.status.domain_syntax,
            }

            expected_false = {
                "status.subdomain_syntax": self.checker.status.subdomain_syntax,
                "status.ipv4_syntax": self.checker.status.ipv4_syntax,
                "status.ipv6_syntax": self.checker.status.ipv6_syntax,
                "status.ipv4_range_syntax": self.checker.status.ipv4_range_syntax,
                "status.ipv6_range_syntax": self.checker.status.ipv6_range_syntax,
                "status.ip_syntax": self.checker.status.ip_syntax,
                "status.url_syntax": self.checker.status.url_syntax,
            }

            for key, value in expected_true.items():
                self.assertTrue(value, key)

            for key, value in expected_false.items():
                self.assertFalse(value, key)

    def test_try_to_query_from_dns_lookup(self) -> None:
        """
        Tests the method which let us perform the test through the DNS method.

        In this case, we check what happens a malicious IP is given.
        """

        self.checker.query_a_record = self.fake_query_a_record

        self.checker.subject = "127.24.78.18"

        self.checker.try_to_query_status_from_dns_lookup()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_from_dns_lookup_domain(self) -> None:
        """
        Tests the method which let us perform the test through the DNS method.

        In this case, we check what happens a malicious domain is found.
        """

        self.checker.query_a_record = self.fake_query_a_record

        self.checker.subject = "example.org"

        self.checker.try_to_query_status_from_dns_lookup()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_from_dns_lookup_no_dns_record(self) -> None:
        """
        Tests the method which let us perform the test through the DNS method.

        In this case, we check what happens when no DNS record is found.
        """

        self.checker.query_a_record = self.fake_query_a_record_none

        self.checker.subject = "example.org"

        self.checker.try_to_query_status_from_dns_lookup()

        # None is because nothing was actually changed by the current method.
        expected_status = None
        expected_source = None

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_from_syntax_lookup(self) -> None:
        """
        Tests the method which let us perform the test through the syntax check
        method.
        """

        self.checker.subject = "example.org"

        self.checker.status.domain_syntax = True
        self.checker.status.ip_syntax = False
        self.checker.status.url_syntax = False

        self.checker.try_to_query_status_from_syntax_lookup()

        # None is because nothing was actually changed by the current method.
        expected_status = None
        expected_source = None

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_from_syntax_lookup_only_ip_valid(self) -> None:
        """
        Tests the method which let us perform the test through the syntax check
        method.
        """

        self.checker.subject = "example.org"

        self.checker.status.domain_syntax = False
        self.checker.status.ip_syntax = True
        self.checker.status.url_syntax = False

        self.checker.try_to_query_status_from_syntax_lookup()

        # None is because nothing was actually changed by the current method.
        expected_status = None
        expected_source = None

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_from_syntax_lookup_only_url_valid(self) -> None:
        """
        Tests the method which let us perform the test through the syntax check
        method.
        """

        self.checker.subject = "example.org"

        self.checker.status.domain_syntax = False
        self.checker.status.ip_syntax = False
        self.checker.status.url_syntax = True

        self.checker.try_to_query_status_from_syntax_lookup()

        # None is because nothing was actually changed by the current method.
        expected_status = None
        expected_source = None

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_from_syntax_lookup_invalid(self) -> None:
        """
        Tests the method which let us perform the test through the syntax check
        method.
        """

        self.checker.subject = "example.org"

        self.checker.status.domain_syntax = False
        self.checker.status.ip_syntax = False
        self.checker.status.url_syntax = False

        self.checker.try_to_query_status_from_syntax_lookup()

        # None is because nothing was actually changed by the current method.
        expected_status = "INVALID"
        expected_source = "SYNTAX"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_from_syntax(self) -> None:
        """
        Tests the method which let us query the status of the given subject.
        """

        def fake_try_to_query_status_from_syntax_lookup():
            self.checker.status.status = "INVALID"
            self.checker.status.status_source = "SYNTAX"

        def fake_try_to_query_status_from_dns_lookup():
            ...

        self.checker.do_syntax_check_first = True
        self.checker.subject = pyf_test_dataset.NOT_VALID_DOMAINS[0]

        self.checker.query_a_record = self.fake_query_a_record
        self.checker.try_to_query_status_from_syntax_lookup = (
            fake_try_to_query_status_from_syntax_lookup
        )
        self.checker.try_to_query_status_from_dns_lookup = (
            fake_try_to_query_status_from_dns_lookup
        )

        self.checker.query_status()

        expected_status = "INVALID"
        expected_source = "SYNTAX"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_from_dns_lookup(self) -> None:
        """
        Tests the method which let us query the status of the given subject.
        """

        def fake_try_to_query_status_from_syntax_lookup():
            ...

        def fake_try_to_query_status_from_dns_lookup():
            self.checker.status.status = "MALICIOUS"
            self.checker.status.status_source = "REPUTATION"

        self.checker.do_syntax_check_first = True
        self.checker.subject = pyf_test_dataset.NOT_VALID_DOMAINS[0]

        self.checker.query_a_record = self.fake_query_a_record
        self.checker.try_to_query_status_from_syntax_lookup = (
            fake_try_to_query_status_from_syntax_lookup
        )
        self.checker.try_to_query_status_from_dns_lookup = (
            fake_try_to_query_status_from_dns_lookup
        )

        self.checker.query_status()

        expected_status = "MALICIOUS"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_query_status_negative(self) -> None:
        """
        Tests the method which let us query the status of the given subject.
        """

        def fake_try_to_query_status_from_syntax_lookup():
            ...

        def fake_try_to_query_status_from_dns_lookup():
            ...

        self.checker.do_syntax_check_first = True
        self.checker.subject = pyf_test_dataset.NOT_VALID_DOMAINS[0]

        self.checker.query_a_record = self.fake_query_a_record
        self.checker.try_to_query_status_from_syntax_lookup = (
            fake_try_to_query_status_from_syntax_lookup
        )
        self.checker.try_to_query_status_from_dns_lookup = (
            fake_try_to_query_status_from_dns_lookup
        )

        self.checker.query_status()

        expected_status = "SANE"
        expected_source = "REPUTATION"

        actual_status = self.checker.status.status
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_status, actual_status)
        self.assertEqual(expected_source, actual_source)

    def test_get_status(self) -> None:
        """
        Tests the method which let us query the status to interact with.
        """

        self.test_query_status_negative()

        actual = self.checker.get_status()

        self.assertIsInstance(actual, ReputationCheckerStatus)


if __name__ == "__main__":
    unittest.main()
