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

Tests of PyFunceble.lookup.dns

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
from unittest.mock import Mock

from dns.resolver import NXDOMAIN, YXDOMAIN, NoAnswer, NoNameservers

from PyFunceble.lookup import Dns


class TestDNSLookup(TestCase):
    """
    Tests of the PyFunceble.lookup.dns.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()

    def test_custom_lifetime(self):
        """
        Tests the initiation of a custom lifetime.
        """

        dns_lookup = Dns(lifetime=5)

        expected = 2.0
        actual = dns_lookup.resolver.timeout

        self.assertEqual(expected, actual)

        expected = 5.0
        actual = dns_lookup.resolver.lifetime

        self.assertEqual(expected, actual)

    def test_custom_nameservers(self):
        """
        Tests the initiation of a custom nameserver.
        """

        dns_lookup = Dns(lifetime=5, dns_server="8.8.8.8")

        expected = ["8.8.8.8"]
        actual = dns_lookup.resolver.nameservers

        self.assertEqual(expected, actual)

        self.dns_lookup.update_nameserver("8.8.8.8")
        actual = dns_lookup.resolver.nameservers

        self.assertEqual(expected, actual)

    def test_custom_lifetime_same_as_timeout(self):
        """
        Tests the initiation of a custom lifetime which
        is equal to the default timeout.
        """

        dns_lookup = Dns(lifetime=2)

        expected = 2.0
        actual = dns_lookup.resolver.timeout

        self.assertEqual(expected, actual)

        expected = 4.0
        actual = dns_lookup.resolver.lifetime

        self.assertEqual(expected, actual)

    def test_custom_lifetime_not_int_nor_fload(self):
        """
        Tests the initiation of a custom lifetime which
        is not an integer nor a float.
        """

        dns_lookup = Dns(lifetime="Hello, World!")

        expected = 2.0
        actual = dns_lookup.resolver.timeout

        self.assertEqual(expected, actual)

        expected = 4.0
        actual = dns_lookup.resolver.lifetime

        self.assertEqual(expected, actual)

    def test_get_server_and_port_from(self):
        """
        Tests the methods which let us split
        a nameserver from its port.
        """

        expected_map = {
            "example.org": ("example.org", 53),
            "example.net:53": ("example.net", 53),
            "example.com:449": ("example.com", 449),
            " : :": (" : ", 53),
        }

        for inputted, expected in expected_map.items():
            # pylint: disable=protected-access
            actual = self.dns_lookup._get_server_and_port_from(inputted)

            self.assertEqual(expected, actual)

    def test_get_addr_info_not_str(self):
        """
        Tests the method which let us get an addrinfo for the case
        that we don't give a string.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.get_addr_info(123))

    def test_get_addr_info(self):
        """
        Tests the method which let us get an addrinfo.
        """

        actual = self.dns_lookup.get_addr_info("one.one.one.one")

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_is_present_in_result(self):
        """
        Tests the methos which let us check if a type of record
        is in the results for the case that the record is not present.
        """

        given = {"A": None}

        expected = False
        actual = self.dns_lookup.is_record_present_in_result("A", given)

        self.assertEqual(expected, actual)

        actual = self.dns_lookup.is_record_present_in_result(["A", "CNAME"], given)

        self.assertEqual(expected, actual)

        expected = True
        actual = self.dns_lookup.is_record_present_in_result(
            "A", given, allow_empty=True
        )

        actual = self.dns_lookup.is_record_present_in_result(
            ["A", "CNAME"], given, allow_empty=True
        )

        self.assertEqual(expected, actual)

        given["A"] = []

        actual = self.dns_lookup.is_record_present_in_result("A", given)
        expected = False

        self.assertEqual(expected, actual)

        expected = True
        actual = self.dns_lookup.is_record_present_in_result(
            "A", given, allow_empty=True
        )

        self.assertEqual(expected, actual)


class TestDNSLookupA(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    an A record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "github.com"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the A record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.a_record(123))

    def test_record(self):
        """
        Tests the method which let us query the A record.
        """

        side_effect = [["127.0.10.1", "127.0.10.2"]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the A record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the A record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the A record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the A record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)


class TestDNSLookupAAAA(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    an AAAA record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "example.com"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the AAAA record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.aaaa_record(123))

    def test_record(self):
        """
        Tests the method which let us query the AAAA record.
        """

        side_effect = [["::1", "::2"]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)


class TestDNSLookupCNAME(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    an CNAME record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "www.twitter.com"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the CNAME record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.cname_record(123))

    def test_record(self):
        """
        Tests the method which let us query the CNAME record.
        """

        side_effect = [["example.org"]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)


class TestDNSLookupMX(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    an MX record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "gmail.com"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the MX record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.mx_record(123))

    def test_record(self):
        """
        Tests the method which let us query the MX record.
        """

        side_effect = [["mail.example.org"]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)


class TestDNSLookupNS(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    a NS record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "example.net"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the NS record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.ns_record(123))

    def test_record(self):
        """
        Tests the method which let us query the NS record.
        """

        side_effect = [["ns1.example.org", "ns2.example.org"]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)


class TestDNSLookupTXT(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    a TXT record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "iana.org"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the NS record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.txt_record(123))

    def test_record(self):
        """
        Tests the method which let us query the TXT record.
        """

        side_effect = [["Hello, World!"]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)


class TestDNSLookupPTR(TestCase):
    """
    Tests of the PyFunceble.lookup.dns for the case we request
    a PTR record.
    """

    # pylint: disable=invalid-name

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dns_lookup = Dns()
        self.subject = "8.8.8.8"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the PTR record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.ptr_record(123))

    def test_record_wrong_format(self):
        """
        Tests the methods which let us query the PTR record
        for the case that the wrong format is given.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record(self):
        """
        Tests the method which let us query the PTR record.
        """

        side_effect = [["dns.google."]]
        expected = side_effect[0]
        self.dns_lookup.resolver.resolve = Mock(side_effect=side_effect)

        actual = self.dns_lookup.ptr_record("8.8.8.8.in-addr.arpa.", reverse_name=False)

        self.assertEqual(expected, actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.resolve = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
