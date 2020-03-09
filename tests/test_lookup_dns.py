# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

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
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
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

        dns_lookup = Dns(lifetime=5, dns_server="1.1.1.1")

        expected = ["1.1.1.1"]
        actual = dns_lookup.resolver.nameservers

        self.assertEqual(expected, actual)

        self.dns_lookup.update_nameserver("1.1.1.1")
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
        self.subject = "example.org"

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

        actual = self.dns_lookup.a_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the A record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the A record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the A record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.a_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the A record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

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

        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.aaaa_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the AAAA record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

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

        actual = self.dns_lookup.cname_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.cname_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the CNAME record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

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

        actual = self.dns_lookup.mx_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.mx_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the MX record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

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

        actual = self.dns_lookup.ns_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.ns_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the NS record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

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

        actual = self.dns_lookup.txt_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.txt_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the TXT record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

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
        self.subject = "1.1.1.1"

    def test_record_given_not_str(self):
        """
        Tests the method which let us query the PTR record for the case
        that a non string is given.
        """

        self.assertRaises(ValueError, lambda: self.dns_lookup.ptr_record(123))

    def test_record(self):
        """
        Tests the method which let us query the PTR record.
        """

        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

        actual = self.dns_lookup.ptr_record("1.1.1.1.in-addr.arpa.", reverse_name=False)

        self.assertIsInstance(actual, list)
        self.assertNotEqual([], actual)

    def test_record_NXDOMAIN(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a NXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NXDOMAIN())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_YXDOMAIN(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a YXDOMAIN exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=YXDOMAIN())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoAnswer(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a NoAnswer exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoAnswer())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)

    def test_record_NoNameservers(self):
        """
        Tests the method which let us get the PTR record for the case that
        we get a NoNameservers exception.
        """

        self.dns_lookup.resolver.query = Mock(side_effect=NoNameservers())

        expected = None
        actual = self.dns_lookup.ptr_record(self.subject)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
