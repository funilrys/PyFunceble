"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our availability checker base.

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

# pylint: disable=too-many-lines

import unittest
import unittest.mock

from PyFunceble.checker.availability.base import AvailabilityCheckerBase
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.checker.base import CheckerBase
from PyFunceble.config.loader import ConfigLoader
from PyFunceble.query.dns.query_tool import DNSQueryTool


class TestAvailabilityCheckerBase(unittest.TestCase):
    """
    The tests of our availability checker base.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.checker = AvailabilityCheckerBase()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.checker

    def test_set_use_extra_rules_return(self) -> None:
        """
        Tests the response of the method which let us activate the special
        rules filtering.
        """

        given = False

        actual = self.checker.set_use_extra_rules(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_extra_rules_method(self) -> None:
        """
        Tests the method which let us activate the special rules filtering.
        """

        given = False
        expected = False

        self.checker.set_use_extra_rules(given)

        actual = self.checker.use_extra_rules

        self.assertEqual(expected, actual)

    def test_set_use_extra_rules_attribute(self) -> None:
        """
        Tests the method which let us activate the special rules filtering
        through the attribute.
        """

        given = False
        expected = False

        self.checker.use_extra_rules = given
        actual = self.checker.use_extra_rules

        self.assertEqual(expected, actual)

    def test_set_use_extra_rules_init(self) -> None:
        """
        Tests the method which let us activate the special rules filtering
        through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_extra_rules=False)

        expected = False
        actual = checker.use_extra_rules

        self.assertEqual(expected, actual)

    def test_set_use_extra_rules_not_bool(self) -> None:
        """
        Tests the method which let us activate the special rules filtering
        through the attribute.

        In this use case we check the case that the inputted value is not a
        :py:class:`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_use_extra_rules(given))

    def test_guess_and_set_use_extra_rules(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_extra_rules` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"lookup": {"special": False}}

        config_loader.start()

        self.checker.guess_and_set_use_extra_rules()

        expected = False
        actual = self.checker.use_extra_rules

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_extra_rules_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_extra_rules` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_use_extra_rules()

        expected = self.checker.STD_USE_EXTRA_RULES
        actual = self.checker.use_extra_rules

        self.assertEqual(expected, actual)

    def test_set_use_whois_lookup_return(self) -> None:
        """
        Tests the response of the method which let us activate the usage of
        the WHOIS lookup method.
        """

        given = False

        actual = self.checker.set_use_whois_lookup(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_whois_lookup_method(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS lookup
        method.
        """

        given = False
        expected = False

        self.checker.set_use_whois_lookup(given)

        actual = self.checker.use_whois_lookup

        self.assertEqual(expected, actual)

    def test_set_use_whois_lookup_attribute(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS lookup
        method through the attribute.
        """

        given = False
        expected = False

        self.checker.use_whois_lookup = given

        actual = self.checker.use_whois_lookup

        self.assertEqual(expected, actual)

    def test_set_use_whois_lookup_init(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS lookup
        method through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_whois_lookup=False)

        expected = False
        actual = checker.use_whois_lookup

        self.assertEqual(expected, actual)

    def test_set_use_whois_lookup_not_bool(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS lookup
        method.

        In this case, we check the case that the inputted value is not a
        :py:class:`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_use_whois_lookup(given))

    def test_guess_and_set_use_whois_lookup(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_whois_lookup` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"lookup": {"whois": False}}

        config_loader.start()

        self.checker.guess_and_set_use_whois_lookup()

        expected = False
        actual = self.checker.use_whois_lookup

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_whois_lookup_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_whois_lookup` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_use_extra_rules()

        expected = self.checker.STD_USE_WHOIS_LOOKUP
        actual = self.checker.use_whois_lookup

        self.assertEqual(expected, actual)

    def test_set_use_dns_lookup_return(self) -> None:
        """
        Tests the response of the method which let us activate the usage of
        the DNS lookup method.
        """

        given = False

        actual = self.checker.set_use_dns_lookup(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_dns_lookup_method(self) -> None:
        """
        Tests the method which let us activate the usage of the DNS lookup
        method.
        """

        given = False
        expected = False

        self.checker.set_use_dns_lookup(given)

        actual = self.checker.use_dns_lookup

        self.assertEqual(expected, actual)

    def test_set_dns_lookup_attribute(self) -> None:
        """
        Tests the method which let us activate the usage of the DNS lookup
        method through the attribute.
        """

        given = False
        expected = False

        self.checker.use_dns_lookup = given

        actual = self.checker.use_dns_lookup

        self.assertEqual(expected, actual)

    def test_set_use_dns_lookup_init(self) -> None:
        """
        Tests the method which let us activate the usage of the DNS lookup
        method through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_dns_lookup=False)

        expected = False
        actual = checker.use_dns_lookup

        self.assertEqual(expected, actual)

    def test_set_dns_lookup_not_bool(self) -> None:
        """
        Tests the method which let us activate the usage of the DNS lookup
        method.

        Here we check the case that the inputted value is not a :py:class:`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_use_dns_lookup(given))

    def test_guess_and_set_use_dns_lookup(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_dns_lookup` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"lookup": {"dns": False}}

        config_loader.start()

        self.checker.guess_and_set_dns_lookup()

        expected = False
        actual = self.checker.use_dns_lookup

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_dns_lookup_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_dns_lookup` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_dns_lookup()

        expected = self.checker.STD_USE_DNS_LOOKUP
        actual = self.checker.use_dns_lookup

        self.assertEqual(expected, actual)

    def test_set_use_netinfo_lookup_return(self) -> None:
        """
        Tests the response of the method which let us activate the usage of
        the NETINFO lookup method.
        """

        given = False

        actual = self.checker.set_use_netinfo_lookup(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_netinfo_lookup_method(self) -> None:
        """
        Tests the method which let us activate the usage of the NETINFO lookup
        method.
        """

        given = False
        expected = False

        self.checker.set_use_netinfo_lookup(given)

        actual = self.checker.use_netinfo_lookup

        self.assertEqual(expected, actual)

    def test_set_netinfo_lookup_attribute(self) -> None:
        """
        Tests the method which let us activate the usage of the NETINFO lookup
        method through the attribute.
        """

        given = False
        expected = False

        self.checker.use_netinfo_lookup = given

        actual = self.checker.use_netinfo_lookup

        self.assertEqual(expected, actual)

    def test_set_use_netinfo_lookup_init(self) -> None:
        """
        Tests the method which let us activate the usage of the NETINFO lookup
        method through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_netinfo_lookup=False)

        expected = False
        actual = checker.use_netinfo_lookup

        self.assertEqual(expected, actual)

    def test_set_netinfo_lookup_not_bool(self) -> None:
        """
        Tests the method which let us activate the usage of the NETINFO lookup
        method.

        Here we check the case that the inputted value is not a bool.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_use_netinfo_lookup(given))

    def test_guess_and_set_use_netinfo_lookup(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_netinfo_lookup` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"lookup": {"netinfo": False}}

        config_loader.start()

        self.checker.guess_and_set_use_netinfo_lookup()

        expected = False
        actual = self.checker.use_netinfo_lookup

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_netinfo_lookup_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_netinfo_lookup` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_use_netinfo_lookup()

        expected = self.checker.STD_USE_NETINFO_LOOKUP
        actual = self.checker.use_netinfo_lookup

        self.assertEqual(expected, actual)

    def test_set_use_http_code_lookup_return(self) -> None:
        """
        Tests the response of the method which let us activate the usage of
        the HTTP Code lookup method.
        """

        given = False

        actual = self.checker.set_use_http_code_lookup(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_http_code_lookup_method(self) -> None:
        """
        Tests the method which let us activate the usage of the HTTP Code lookup
        method.
        """

        given = False
        expected = False

        self.checker.set_use_http_code_lookup(given)

        actual = self.checker.use_http_code_lookup

        self.assertEqual(expected, actual)

    def test_set_use_http_code_lookup_attribute(self) -> None:
        """
        Tests the method which let us activate the usage of the HTTP Code lookup
        method through the attribute.
        """

        given = False
        expected = False

        self.checker.use_http_code_lookup = given

        actual = self.checker.use_http_code_lookup

        self.assertEqual(expected, actual)

    def test_set_use_http_code_lookup_init(self) -> None:
        """
        Tests the method which let us activate the usage of the HTTP Code lookup
        method through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_http_code_lookup=False)

        expected = False
        actual = checker.use_http_code_lookup

        self.assertEqual(expected, actual)

    def test_set_use_http_code_lookup_not_bool(self) -> None:
        """
        Tests the method which let us activate the usage of the HTTP Code lookup
        method.

        Here we check the case that the inputted value is not a:py:class`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: self.checker.set_use_http_code_lookup(given)
        )

    def test_guess_and_set_use_http_code_lookup(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_http_code_lookup` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"lookup": {"http_status_code": False}}

        config_loader.start()

        self.checker.guess_and_set_use_http_code_lookup()

        expected = False
        actual = self.checker.use_http_code_lookup

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_http_code_lookup_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_http_code_lookup` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_use_http_code_lookup()

        expected = self.checker.STD_USE_HTTP_CODE_LOOKUP
        actual = self.checker.use_netinfo_lookup

        self.assertEqual(expected, actual)

    def test_set_use_reputation_lookup_return(self) -> None:
        """
        Tests the response of the method which let us activate the usage of
        the reputation lookup method.
        """

        given = True

        actual = self.checker.set_use_reputation_lookup(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_reputation_lookup_method(self) -> None:
        """
        Tests the method which let us activate the usage of the reputation
        lookup method.
        """

        given = True
        expected = True

        self.checker.set_use_reputation_lookup(given)

        actual = self.checker.use_reputation_lookup

        self.assertEqual(expected, actual)

    def test_set_use_reputation_lookup_attribute(self) -> None:
        """
        Tests the method which let us activate the usage of the reputation
        lookup method through the attribute.
        """

        given = True
        expected = True

        self.checker.use_reputation_lookup = given

        actual = self.checker.use_reputation_lookup

        self.assertEqual(expected, actual)

    def test_set_use_reputation_lookup_init(self) -> None:
        """
        Tests the method which let us activate the usage of the reputation
        lookup method through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_reputation_lookup=True)

        expected = True
        actual = checker.use_reputation_lookup

        self.assertEqual(expected, actual)

    def test_set_use_reputation_lookup_not_bool(self) -> None:
        """
        Tests the method which let us activate the usage of the reputation
        lookup method through.

        Here we check the case that the inputted value is not a:py:class`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: self.checker.set_use_reputation_lookup(given)
        )

    def test_guess_and_set_use_reputation_lookup(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_reputation_lookup` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"lookup": {"reputation": True}}

        config_loader.start()

        self.checker.guess_and_set_use_reputation_lookup()

        expected = True
        actual = self.checker.use_reputation_lookup

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_reputation_lookup_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_reputation_lookup` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_use_reputation_lookup()

        expected = self.checker.STD_USE_REPUTATION_LOOKUP
        actual = self.checker.use_reputation_lookup

        self.assertEqual(expected, actual)

    def test_set_use_whois_db_return(self) -> None:
        """
        Tests the response of the method which let us activate the usage of
        the WHOIS DB.
        """

        given = False

        actual = self.checker.set_use_whois_db(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_use_whois_db_method(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS DB.
        """

        given = False
        expected = False

        self.checker.set_use_whois_db(given)

        actual = self.checker.use_whois_db

        self.assertEqual(expected, actual)

    def test_set_use_whois_db_attribute(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS DB
        through the attribute.
        """

        given = False
        expected = False

        self.checker.use_whois_db = given

        actual = self.checker.use_whois_db

        self.assertEqual(expected, actual)

    def test_set_use_whois_db_init(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS DB
        through the class constructor.
        """

        checker = AvailabilityCheckerBase(use_whois_db=False)

        expected = False
        actual = checker.use_whois_db

        self.assertEqual(expected, actual)

    def test_set_use_whois_db_not_bool(self) -> None:
        """
        Tests the method which let us activate the usage of the WHOIS DB.

        Here we check the case that the inputted value is not a :py:class:`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_use_whois_db(given))

    def test_guess_and_set_use_whois_db(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code`use_whois_db` attribute.
        """

        config_loader = ConfigLoader()
        config_loader.custom_config = {"cli_testing": {"whois_db": False}}

        config_loader.start()

        self.checker.guess_and_set_use_whois_db()

        expected = False
        actual = self.checker.use_whois_db

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_use_whois_db_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the value of the
        :code:`use_whois_db` attribute; but for the case that the
        configuration is not loaded.
        """

        self.checker.guess_and_set_use_whois_db()

        expected = self.checker.STD_USE_WHOIS_DB
        actual = self.checker.use_whois_db

        self.assertEqual(expected, actual)

    def test_subject_propagator(self) -> None:
        """
        Tests that the subjects and its IDNA counterpart are correctly
        propagated.
        """

        given = "äxample.org"
        expected_subject = "äxample.org"
        expected_idna_subject = "xn--xample-9ta.org"

        self.checker.subject = given

        actual_subject = self.checker.status.subject
        actual_idna_propagated = [
            self.checker.dns_query_tool.subject,
            self.checker.whois_query_tool.subject,
            self.checker.addressinfo_query_tool.subject,
            self.checker.hostbyaddr_query_tool.subject,
            self.checker.http_status_code_query_tool.subject,
            self.checker.domain_syntax_checker.subject,
            self.checker.ip_syntax_checker.subject,
            self.checker.url_syntax_checker.subject,
            self.checker.status.idna_subject,
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

        actual = self.checker.status.subject

        actual_idna_propagated = [
            self.checker.dns_query_tool.subject,
            self.checker.whois_query_tool.subject,
            self.checker.addressinfo_query_tool.subject,
            self.checker.hostbyaddr_query_tool.subject,
            self.checker.http_status_code_query_tool.subject,
            self.checker.domain_syntax_checker.subject,
            self.checker.ip_syntax_checker.subject,
            self.checker.url_syntax_checker.subject,
            self.checker.status.idna_subject,
        ]

        self.assertEqual(expected_subject, actual)

        for actual in actual_idna_propagated:
            self.assertEqual(expected_idna_subject, actual)

    def test_should_we_continue_test_positive(self) -> None:
        """
        Tests the method which let us check if we should continue to another
        test method.
        """

        given = "INVALID"
        self.checker.status.status = "INACTIVE"

        expected = True
        actual = self.checker.should_we_continue_test(given)

        self.assertEqual(expected, actual)

    def test_should_we_continue_test_negative(self) -> None:
        """
        Tests the method which let us check if we should continue to another
        test method.
        """

        given = "VALID"
        self.checker.status.status = "INACTIVE"

        expected = False
        actual = self.checker.should_we_continue_test(given)

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(DNSQueryTool, "query")
    def test_query_dns_record(self, dns_query_patch: unittest.mock.MagicMock) -> None:
        """
        Tests the method that let us query the (right) DNS record of the given
        subject.
        """

        dns_query_patch.return_value = ["192.168.1.1"]
        given = "example.org"
        expected = {"NS": ["192.168.1.1"]}

        self.checker.subject = given

        actual = self.checker.query_dns_record()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(DNSQueryTool, "query")
    def test_query_dns_record_no_response(
        self, dns_query_patch: unittest.mock.MagicMock
    ) -> None:
        """
        Tests the method that let us query the (right) DNS record of the given
        subject.

        Here we test the case that there is systematically no (valid) response.
        """

        dns_query_patch.return_value = []
        given = "example.net"
        expected = dict()  # pylint: disable=use-dict-literal

        self.checker.subject = given

        actual = self.checker.query_dns_record()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(DNSQueryTool, "query")
    def test_query_dns_record_subdomain(
        self, dns_query_patch: unittest.mock.MagicMock
    ) -> None:
        """
        Tests the method that let us query the (right) DNS record of the given
        subject.
        """

        dns_query_patch.return_value = ["192.168.1.2"]
        given = "test.example.org"
        expected = {"NS": ["192.168.1.2"]}

        self.checker.subject = given

        actual = self.checker.query_dns_record()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(DNSQueryTool, "query")
    def test_query_dns_record_ptr(
        self, dns_query_patch: unittest.mock.MagicMock
    ) -> None:
        """
        Tests the method that let us query the (right) DNS record of the given
        subject.
        """

        dns_query_patch.return_value = ["example.org"]
        given = "192.168.1.1"
        expected = {"PTR": ["example.org"]}

        self.checker.subject = given

        actual = self.checker.query_dns_record()

        self.assertEqual(expected, actual)

    def test_query_dns_record_no_subject(self) -> None:
        """
        Tests the method that let us query the (right) DNS record of the given
        subject.

        In this case we test the case that the subject is not set.
        """

        # pylint: disable=unnecessary-lambda
        self.assertRaises(TypeError, lambda: self.checker.query_dns_record())

    @unittest.mock.patch.object(DNSQueryTool, "query")
    def test_query_dns_record_not_valid_subject(
        self, dns_query_patch: unittest.mock.MagicMock
    ) -> None:
        """
        Tests the method that let us query the (right) DNS record of the given
        subject.

        Here we test the case that the given subject is not correct.
        """

        dns_query_patch.return_value = []
        given = "a1"
        expected = dict()  # pylint: disable=use-dict-literal

        self.checker.subject = given

        actual = self.checker.query_dns_record()

        self.assertEqual(expected, actual)

    def test_try_to_query_status_from_whois(self) -> None:
        """
        Tests the method which tries to define the status from the WHOIS record.
        """

        # In this test, we don't care about the database.
        self.checker.use_whois_db = False
        self.checker.subject = "example.org"

        # Let's test the case that no expiration date is found.
        self.checker.whois_query_tool.get_expiration_date = lambda: None
        self.checker.whois_query_tool.lookup_record.record = None

        self.checker.try_to_query_status_from_whois()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_whois_record = None
        actual_whois_record = self.checker.status.whois_record

        self.assertEqual(expected_whois_record, actual_whois_record)

        # Let's test the case that an expiration date is actually given.
        self.checker.whois_query_tool.get_expiration_date = lambda: "10-nov-1971"
        self.checker.whois_query_tool.lookup_record.record = "Hello, World!"

        self.checker.try_to_query_status_from_whois()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "WHOIS"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

        expected_whois_record = "Hello, World!"
        actual_whois_record = self.checker.status.whois_record

        self.assertEqual(expected_whois_record, actual_whois_record)

    def test_try_to_query_status_from_dns(self) -> None:
        """
        Tests the method that tries to define the status from the DNS lookup.
        """

        # Let's test the case that no answer is given back.
        # pylint: disable=unnecessary-lambda
        self.checker.subject = "example.org"
        self.checker.query_dns_record = (
            lambda: dict()
        )  # pylint: disable=use-dict-literal

        self.checker.try_to_query_status_from_dns()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Let's test the case that an answer is given back.
        self.checker.query_dns_record = lambda: {"NS": ["ns1.example.org"]}

        self.checker.try_to_query_status_from_dns()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "DNSLOOKUP"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_status_from_netinfo(self) -> None:
        """
        Tests the method that tries to define the status from the NETINFO
        lookup.
        """

        # Let's test the case that nothing is given back.
        self.checker.subject = "example.org"
        self.checker.addressinfo_query_tool.get_info = lambda: None

        self.checker.try_to_query_status_from_netinfo()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Let's test the case that an answer is given back.
        self.checker.addressinfo_query_tool.get_info = lambda: ["192.168.1.1"]

        self.checker.try_to_query_status_from_netinfo()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "NETINFO"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

        # Now the same test but with an IP.
        self.checker.subject = "192.168.1.1"
        self.checker.hostbyaddr_query_tool.get_info = lambda: None

        self.checker.try_to_query_status_from_netinfo()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Let's test the case that an answer is given back.
        self.checker.hostbyaddr_query_tool.get_info = lambda: ["example.org"]

        self.checker.try_to_query_status_from_netinfo()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "NETINFO"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

        # Now a test with a digit string.
        # This test exists because we shouldn't produce false positive.
        self.checker.subject = "192"

        self.checker.try_to_query_status_from_netinfo()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Now the same test as before but for everything that may not exists
        # publicly but in the local network.
        #
        # Let's test the case that nothing is given back.
        self.checker.subject = "example"
        self.checker.addressinfo_query_tool.get_info = lambda: None

        self.checker.try_to_query_status_from_netinfo()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Let's test the case that an answer is given back.
        self.checker.addressinfo_query_tool.get_info = lambda: ["192.168.1.19"]

        self.checker.try_to_query_status_from_netinfo()

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "NETINFO"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_status_from_http_status_code(self) -> None:
        """
        Tests of the method that tries to define a status from the HTTP status
        code.
        """

        # Let's test the strange case that we meet mailto:xxx@yyy.de
        self.checker.subject = "mailto:hello@world.de"

        self.checker.http_status_code_query_tool.get_status_code = (
            lambda: self.checker.http_status_code_query_tool.STD_UNKNOWN_STATUS_CODE
        )

        self.checker.try_to_query_status_from_http_status_code()

        expected_subject = "mailto:hello@world.de"
        actual_subject = self.checker.http_status_code_query_tool.subject

        self.assertEqual(expected_subject, actual_subject)

        expected_status = None
        actual_status = None

        self.assertEqual(expected_status, actual_status)

        expected_status_code = None
        actual_status_code = self.checker.status.http_status_code

        self.assertEqual(expected_status_code, actual_status_code)

        # Now, let's test a normal domain.
        self.checker.subject = "example.org"

        self.checker.http_status_code_query_tool.get_status_code = lambda: 200

        self.checker.try_to_query_status_from_http_status_code()

        expected_subject = "http://example.org:80"
        actual_subject = self.checker.http_status_code_query_tool.subject

        self.assertEqual(expected_subject, actual_subject)

        expected_status = "ACTIVE"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "HTTP CODE"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

    def test_try_to_query_status_from_syntax_lookup(self) -> None:
        """
        Tests the method that tries to define the status from the syntax lookup.
        """

        # Let's check the case that the subject is a valid domain.
        self.checker.subject = "example.com"

        self.checker.try_to_query_status_from_syntax_lookup()

        expected_status = None
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        # Let's check the case that the subject is an invalid one.
        self.checker.subject = "102117110105108114121115"

        self.checker.try_to_query_status_from_syntax_lookup()

        expected_status = "INVALID"
        actual_status = self.checker.status.status

        self.assertEqual(expected_status, actual_status)

        expected_source = "SYNTAX"
        actual_source = self.checker.status.status_source

        self.assertEqual(expected_source, actual_source)

    def test_get_status(self) -> None:
        """
        Tests the method that let us get the whole status object.
        """

        self.test_try_to_query_status_from_syntax_lookup()

        actual = self.checker.get_status()

        self.assertIsInstance(actual, AvailabilityCheckerStatus)


if __name__ == "__main__":
    unittest.main()
