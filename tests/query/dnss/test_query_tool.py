"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our query tool.

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


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

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


import dataclasses
import secrets
import socket
import unittest
import unittest.mock

import dns.exception
import dns.name
import dns.query

from PyFunceble.config.loader import ConfigLoader
from PyFunceble.query.dns.query_tool import DNSQueryTool, DNSQueryToolRecord

# pylint: disable=protected-access, too-many-lines


class TestDNSQueryTool(unittest.TestCase):
    """
    Tests our DNS query tool.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        def fake_response(data: str) -> object:
            return dataclasses.make_dataclass(
                "FakeResponse", [("address", str, dataclasses.field(default=data))]
            )

        def fake_resolver(_: str, rqtype: str):
            if rqtype == "A":
                return [
                    fake_response("192.168.1.1"),
                    fake_response("10.47.91.9"),
                ]

            return [
                fake_response("fe80::6b01:9045:a42a:fb5f"),
                fake_response("fe80::6b01:9049:a42a:fb5f"),
            ]

        self.resolve_patch = unittest.mock.patch.object(
            dns.resolver.Resolver, "resolve"
        )
        self.udp_query_patch = unittest.mock.patch.object(dns.query, "udp")
        self.tcp_query_patch = unittest.mock.patch.object(dns.query, "tcp")
        self.https_query_patch = unittest.mock.patch.object(dns.query, "https")
        self.tls_query_patch = unittest.mock.patch.object(dns.query, "tls")

        self.mock_resolve = self.resolve_patch.start()
        self.mock_resolve.side_effect = fake_resolver

        self.mock_udp_query = self.udp_query_patch.start()
        self.mock_tcp_query = self.tcp_query_patch.start()
        self.mock_https_query = self.https_query_patch.start()
        self.mock_tls_query = self.tls_query_patch.start()

        self.query_tool = DNSQueryTool(nameservers=["example.org"])

        self.query_tool._get_result_from_response = lambda _: []

    def tearDown(self) -> None:
        """
        Destroys everything previously initiated for the tests.
        """

        self.resolve_patch.stop()
        self.udp_query_patch.stop()
        self.tcp_query_patch.stop()
        self.https_query_patch.stop()
        self.tls_query_patch.stop()

        del self.resolve_patch
        del self.udp_query_patch
        del self.tcp_query_patch
        del self.https_query_patch
        del self.tls_query_patch

        del self.mock_resolve
        del self.mock_udp_query
        del self.mock_tcp_query
        del self.mock_https_query
        del self.mock_tls_query

    @staticmethod
    def timout_response(*args, **kwargs) -> None:
        """
        Provides a response which raise a timeout error exception.
        """

        raise dns.exception.Timeout()

    @staticmethod
    def malformed_response(*args, **kwargs) -> None:
        """
        Provides a response which raises a malformed value error.
        """

        raise ValueError("Input malformed")

    @staticmethod
    def unexpected_source_response(*args, **kwargs) -> None:
        """
        Provides a response which raises an unexpected source exception.
        """

        raise dns.query.UnexpectedSource("got a response from XXX instead of XXX.")

    @staticmethod
    def bad_response_response(*args, **kwargs) -> None:
        """
        Provides a response which raises a bad response error.
        """

        raise dns.query.BadResponse(
            "A DNS query response does not respond to the question asked."
        )

    @staticmethod
    def socket_error(*args, **kwargs) -> None:
        """
        Provides a response which raises a socket error.
        """

        raise socket.gaierror("Socket Error.")

    def test_set_subject(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "example.net"

        expected_dns_name = None
        actual = self.query_tool.dns_name

        self.assertEqual(expected_dns_name, actual)

        expected = "example.net"
        self.query_tool.set_subject(given)

        actual = self.query_tool.subject

        self.assertEqual(expected, actual)

        self.assertIsInstance(self.query_tool.dns_name, dns.name.Name)

    def test_set_subject_absolute(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "example.net."

        expected_dns_name = None
        actual = self.query_tool.dns_name

        self.assertEqual(expected_dns_name, actual)

        expected = "example.net."
        self.query_tool.set_subject(given)

        actual = self.query_tool.subject

        self.assertEqual(expected, actual)

        self.assertIsInstance(self.query_tool.dns_name, dns.name.Name)

    def test_set_subject_not_str(self) -> None:
        """
        Tests the method which let us set the subject to work with for the case
        that the given subject is not a string.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_subject(given))

    def test_set_subject_empty_str(self) -> None:
        """
        Tests the method which let us set the subject to work with for the case
        that the given subject is an empty string.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.query_tool.set_subject(given))

    def test_set_follow_nameserver_order(self) -> None:
        """
        Tests the method which let us allow/disallow the shuffle of the list
        of nameserver.
        """

        given = True
        expected = True

        self.query_tool.set_follow_nameserver_order(given)

        actual = self.query_tool.follow_nameserver_order

        self.assertEqual(expected, actual)

    def test_set_follow_nameserver_order_not_bool(self) -> None:
        """
        Tests the method which let us allow/disallow the shuffle of the list
        of nameserver for the case that the given value is not a boolean
        """

        given = ["Hello", "World"]

        self.assertRaises(
            TypeError, lambda: self.query_tool.set_follow_nameserver_order(given)
        )

    def test_set_follow_nameserver_order_through_init(self) -> None:
        """
        Tests the overwritting of the `follow_nameserver_attribute` attribute
        through the class constructor.
        """

        given = False
        expected = False

        query_tool = DNSQueryTool(follow_nameserver_order=given)

        actual = query_tool.follow_nameserver_order

        self.assertEqual(expected, actual)

    def test_guess_and_set_follow_nameserver_order(self) -> None:
        """
        Tests the method which let us guess and set the order of the server.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"dns": {"follow_server_order": False}}).start()

        self.query_tool.guess_and_set_follow_nameserver_order()

        expected = False
        actual = self.query_tool.follow_nameserver_order

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_follow_nameserver_order_none(self) -> None:
        """
        Tests the method which let us guess and set the order of the server.

        In this test, we check the case that the given value is set to None.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"dns": {"follow_server_order": None}}).start()

        self.query_tool.guess_and_set_follow_nameserver_order()

        expected = self.query_tool.STD_FOLLOW_NAMESERVER_ORDER
        actual = self.query_tool.follow_nameserver_order

        self.assertEqual(expected, actual)

        del config_loader

    def test_set_query_record_type_from_name(self) -> None:
        """
        Tests the method which let us set the type of the record with for the
        case that the string representation of the record type is given.
        """

        given = "A"

        self.query_tool.set_query_record_type(given)

        expected = dns.rdatatype.RdataType.A
        actual = self.query_tool.query_record_type

        self.assertEqual(expected, actual)

        expected = "A"
        actual = self.query_tool.get_human_query_record_type()

        self.assertEqual(expected, actual)

    def test_set_query_record_type_from_value(self) -> None:
        """
        Tests the method which let us set the type of the record with for the
        case that the actual value (int) of the record type is given.
        """

        given = dns.rdatatype.RdataType.AAAA

        self.query_tool.set_query_record_type(given)

        expected = dns.rdatatype.RdataType.AAAA
        actual = self.query_tool.query_record_type

        self.assertEqual(expected, actual)

        expected = "AAAA"
        actual = self.query_tool.get_human_query_record_type()

        self.assertEqual(expected, actual)

    def test_set_query_record_type_unknown_value(self) -> None:
        """
        Tests the method which let us set the type of the record with for the
        case that the actual value is unknown
        """

        given = 1010101010110101

        self.assertRaises(
            ValueError, lambda: self.query_tool.set_query_record_type(given)
        )

    def test_get_dns_name_from_subject_and_query_type(self) -> None:
        """
        Tests themethod which let us us get the dns name that dnspython has to
        use base on the given subject and query type.
        """

        self.query_tool.subject = "example.org"
        self.query_tool.query_record_type = "A"

        expected = dns.name.from_text("example.org")
        actual = self.query_tool.get_dns_name_from_subject_and_query_type()

        self.assertEqual(expected, actual)

    def test_get_dns_name_from_subject_and_query_type_label_too_long(self) -> None:
        """
        Tests themethod which let us us get the dns name that dnspython has to
        use base on the given subject and query type.

        In this case we check that too long entries are handled correctly.
        """

        self.query_tool.subject = f"{secrets.token_urlsafe(300)}.org"
        self.query_tool.query_record_type = "A"

        expected = None
        actual = self.query_tool.get_dns_name_from_subject_and_query_type()

        self.assertEqual(expected, actual)

    def test_get_dns_name_from_subject_and_query_type_label_not_ptr_compliant(
        self,
    ) -> None:
        """
        Tests themethod which let us us get the dns name that dnspython has to
        use base on the given subject and query type.

        In this case we check the case that a non PTR compliant IP is given.
        """

        self.query_tool.subject = "93.184.216.34"
        self.query_tool.query_record_type = "PTR"

        expected = dns.name.from_text("34.216.184.93.in-addr.arpa")
        actual = self.query_tool.get_dns_name_from_subject_and_query_type()

        self.assertEqual(expected, actual)

    def test_get_dns_name_from_subject_and_query_type_label_ptr_compliant(
        self,
    ) -> None:
        """
        Tests themethod which let us us get the dns name that dnspython has to
        use base on the given subject and query type.

        In this case we check the case that a non PTR compliant IP is given.
        """

        self.query_tool.subject = "34.216.184.93.in-addr.arpa"
        self.query_tool.query_record_type = "PTR"

        expected = dns.name.from_text("34.216.184.93.in-addr.arpa")
        actual = self.query_tool.get_dns_name_from_subject_and_query_type()

        self.assertEqual(expected, actual)

    def test_set_query_record_type_not_str_nor_int(self) -> None:
        """
        Tests the method which let us set the type of the record with for the
        case that the given value is not a string nor integer.
        """

        given = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: self.query_tool.set_query_record_type(given)
        )

    def test_set_timeout(self) -> None:
        """
        Tests the method which let us set the timeout to apply.
        """

        given = 5.0
        expected = 5.0

        self.query_tool.set_timeout(given)
        actual = self.query_tool.query_timeout

        self.assertEqual(expected, actual)

    def test_set_timeout_not_int_nor_float(self) -> None:
        """
        Tests the method which let us set the timeout to apply for the case that
        the given timeout is not a float nor a integer.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_timeout(given))

    def test_guess_and_set_timeout(self) -> None:
        """
        Tests the method which let us guess and set the timeout from the
        configuration file.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"lookup": {"timeout": 10.0}}).start()

        self.query_tool.guess_and_set_timeout()

        expected = 10.0
        actual = self.query_tool.query_timeout

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_timeout_none(self) -> None:
        """
        Tests the method which let us guess and set the timeout from the
        configuration file.

        In this test, we check the case the None is given.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"lookup": {"timeout": None}}).start()

        self.query_tool.guess_and_set_timeout()

        expected = self.query_tool.STD_TIMEOUT
        actual = self.query_tool.query_timeout

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_timeout_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the timeout from the
        configuration file.

        In this test, we check the case the config was not loader yet.
        """

        self.query_tool.guess_and_set_timeout()

        expected = self.query_tool.STD_TIMEOUT
        actual = self.query_tool.query_timeout

        self.assertEqual(expected, actual)

    def test_set_trust_server(self) -> None:
        """
        Tests the method which let us trust all the given server.
        """

        given = True
        expected = True

        self.query_tool.set_trust_server(given)
        actual = self.query_tool.trust_server

        self.assertEqual(expected, actual)

    def test_set_trust_server_not_bool(self) -> None:
        """
        Tests the method which let us trust all the given server.

        In this test we check the case that a non-boolean value is given.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_trust_server(given))

    def test_set_trust_server_through_init(self) -> None:
        """
        Tests the overwritting of the `trust_server` attribute through the class
        constructor.
        """

        given = True
        expected = True

        query_tool = DNSQueryTool(trust_server=given)

        actual = query_tool.trust_server

        self.assertEqual(expected, actual)

    def test_guess_and_set_trust_server(self) -> None:
        """
        Tests the method which let us guess and set the trust flag from the
        configuration file.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"dns": {"trust_server": True}}).start()

        self.query_tool.guess_and_set_trust_server()

        expected = True
        actual = self.query_tool.trust_server

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_trust_server_none(self) -> None:
        """
        Tests the method which let us guess and set the trust flag from the
        configuration file.

        In this case, we test the case that None or implicitly a non boolean
        value is given.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"dns": {"trust_server": None}}).start()

        self.query_tool.guess_and_set_trust_server()

        expected = self.query_tool.STD_TRUST_SERVER
        actual = self.query_tool.trust_server

        self.assertEqual(expected, actual)

        del config_loader

    def test_set_preferred_protocol(self) -> None:
        """
        Tests the method which let us set the preferred protocol.
        """

        given = "TCP"
        expected = "TCP"

        self.query_tool.set_preferred_protocol(given)
        actual = self.query_tool.preferred_protocol

        self.assertEqual(expected, actual)

    def test_set_preferred_protocol_through_init(self) -> None:
        """
        Tests the method which let us set the preferred protocol.

        In this test we check that the transfert of the preferred protocol
        through the constructor is working.
        """

        given = "TCP"

        query_tool = DNSQueryTool(preferred_protocol=given)

        expected = "TCP"
        actual = query_tool.preferred_protocol

        self.assertEqual(expected, actual)

    def test_set_preferred_protocol_not_str(self) -> None:
        """
        Tests the method which let us set the preferred protocol for the case
        that the given protocol is not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(
            TypeError, lambda: self.query_tool.set_preferred_protocol(given)
        )

    def test_set_preferred_protocol_not_supported(self) -> None:
        """
        Tests the method which let us set the preferred protocol for the case
        that the given protocol is not supported.
        """

        given = "SNMP"

        self.assertRaises(
            ValueError,
            lambda: self.query_tool.set_preferred_protocol(given),
        )

    def test_guess_and_set_preferred_protocol(self) -> None:
        """
        Tests the method which let us guess and set the preferred protocol.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"dns": {"protocol": "HTTPS"}}).start()

        self.query_tool.guess_and_set_preferred_protocol()

        expected = "HTTPS"
        actual = self.query_tool.preferred_protocol

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_preferred_protocol_none(self) -> None:
        """
        Tests the method which let us guess and set the preferred protocol.

        In this test, we check the case that the given protocol is set to None.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"dns": {"protocol": None}}).start()

        self.query_tool.guess_and_set_preferred_protocol()

        expected = self.query_tool.STD_PROTOCOL
        actual = self.query_tool.preferred_protocol

        self.assertEqual(expected, actual)

    def test_get_lookup_record(self) -> None:
        """
        Tests the method which let us get the lookup record.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        _ = self.query_tool.query()

        actual = self.query_tool.get_lookup_record()

        self.assertIsInstance(actual, DNSQueryToolRecord)

        expected = "example.org"
        self.assertEqual(expected, actual.subject)

    def test_udp_query(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        _ = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_no_info(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this test, we check the case that we don't give any information.
        """

        # pylint: disable=unnecessary-lambda
        self.assertRaises(TypeError, lambda: self.query_tool.query())

        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_timeout(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case, we check the case that a timeout exception is raised.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_udp_query.side_effect = self.timout_response

        _ = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_malformed_input(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case, we check the case that a ValueError is raised.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_udp_query.side_effect = self.malformed_response

        _ = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_unexpected_source(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case, we check the case that an UnexpectedSource exception
        is raised.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_udp_query.side_effect = self.unexpected_source_response

        _ = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_bad_response(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case, we check the case that an BadResponse exception
        is raised.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_udp_query.side_effect = self.bad_response_response

        _ = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_socket_error(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case, we check the case that a socket error is raised.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_udp_query.side_effect = self.socket_error

        _ = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_udp_query_with_result(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case we check that the response is is properly parsed to the
        lookup record.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.query_tool._get_result_from_response = lambda _: ["93.184.216.34"]

        actual = self.query_tool.query()

        self.mock_udp_query.assert_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()

        # pragma: no cover ## Let's trust upstream
        expected = ["93.184.216.34"]

        self.assertEqual(expected, actual)

        self.assertEqual(expected, self.query_tool.lookup_record.response)

    def test_udp_query_bad_escape(self) -> None:
        """
        Tests the method which let us query through the UDP protocol.

        In this case we check the case that a subject has some bad escape
        character.
        """

        self.query_tool.preferred_protocol = "UDP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org\\"

        _ = self.query_tool.query()

        # Not called because inputted is invalid.
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()

    def test_tcp_query(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        _ = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tcp_query_timeout(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case, we assume that a timeout was given.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tcp_query.side_effect = self.timout_response

        _ = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tcp_query_malformed_input(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case, we check the case that a ValueError is raised.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tcp_query.side_effect = self.malformed_response

        _ = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tcp_query_unexpected_source(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case, we check the case that an UnexpectedSource exception
        is raised.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tcp_query.side_effect = self.unexpected_source_response

        _ = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tcp_query_bad_response(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case, we check the case that an BadResponse exception
        is raised.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tcp_query.side_effect = self.bad_response_response

        _ = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tcp_query_socket_error(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case, we check the case that a socket error is raised.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tcp_query.side_effect = self.socket_error

        _ = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tcp_query_with_result(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case we check that the response is is properly parsed to the
        lookup record.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.query_tool._get_result_from_response = lambda _: ["93.184.216.34"]

        actual = self.query_tool.query()

        self.mock_tcp_query.assert_called()
        self.mock_tls_query.assert_not_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

        # pragma: no cover ## Let's trust upstream
        expected = ["93.184.216.34"]

        self.assertEqual(expected, actual)

        self.assertEqual(expected, self.query_tool.lookup_record.response)

    def test_tcp_query_bad_escape(self) -> None:
        """
        Tests the method which let us query through the TCP protocol.

        In this case we check the case that a subject has some bad escape
        character.
        """

        self.query_tool.preferred_protocol = "TCP"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org\\"

        _ = self.query_tool.query()

        # Not called because inputted is invalid.
        self.mock_tcp_query.assert_not_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        _ = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query_timeout(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case we check the case that a timeout exception is raised.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_https_query.side_effect = self.timout_response

        _ = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query_malformed_input(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case, we check the case that a ValueError is raised.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_https_query.side_effect = self.malformed_response

        _ = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query_socket_error(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case, we check the case that a socket error is raised.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_https_query.side_effect = self.socket_error

        _ = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query_unexpected_source(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case, we check the case that an UnexpectedSource exception
        is raised.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_https_query.side_effect = self.unexpected_source_response

        _ = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query_bad_response(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case, we check the case that an BadResponse exception
        is raised.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_https_query.side_effect = self.bad_response_response

        _ = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_https_query_with_result(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case we check that the response is is properly parsed to the
        lookup record.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.query_tool._get_result_from_response = lambda _: ["93.184.216.34"]

        actual = self.query_tool.query()

        self.mock_https_query.assert_called()
        self.mock_tls_query.assert_not_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()

        # pragma: no cover ## Let's trust upstream
        expected = ["93.184.216.34"]

        self.assertEqual(expected, actual)

        self.assertEqual(expected, self.query_tool.lookup_record.response)

    def test_https_query_bad_escape(self) -> None:
        """
        Tests the method which let us query through the HTTPS protocol.

        In this case we check the case that a subject has some bad escape
        character.
        """

        self.query_tool.preferred_protocol = "HTTPS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org\\"

        self.query_tool._get_result_from_response = lambda _: ["93.184.216.34"]

        _ = self.query_tool.query()

        # Not called because inputted is invalid.
        self.mock_https_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tls_query.assert_not_called()

    def test_tls_query(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        _ = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

    def test_tls_query_timeout(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case we check the case that a timeout exception is raised.Is
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tls_query.side_effect = self.timout_response

        _ = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

    def test_tls_query_malformed_input(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case, we check the case that a ValueError is raised.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tls_query.side_effect = self.malformed_response

        _ = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

    def test_tls_query_socket_error(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case, we check the case that a socket error is raised.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tls_query.side_effect = self.socket_error

        _ = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

    def test_tls_query_unexpected_source(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case, we check the case that an UnexpectedSource exception
        is raised.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tls_query.side_effect = self.unexpected_source_response

        _ = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

    def test_tls_query_bad_response(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case, we check the case that an BadResponse exception
        is raised.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.mock_tls_query.side_effect = self.bad_response_response

        _ = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

    def test_tls_query_with_result(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case we check that the response is is properly parsed to the
        lookup record.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org"

        self.query_tool._get_result_from_response = lambda _: ["93.184.216.34"]

        actual = self.query_tool.query()

        self.mock_tls_query.assert_called()
        self.mock_udp_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_https_query.assert_not_called()

        # pragma: no cover ## Let's trust upstream
        expected = ["93.184.216.34"]

        self.assertEqual(expected, actual)

        self.assertEqual(expected, self.query_tool.lookup_record.response)

    def test_tls_query_bad_escape(self) -> None:
        """
        Tests the method which let us query through the TLS protocol.

        In this case we check the case that a subject has some bad escape
        character.
        """

        self.query_tool.preferred_protocol = "TLS"
        self.query_tool.query_record_type = "A"
        self.query_tool.subject = "example.org\\"

        _ = self.query_tool.query()

        # Not called because inputted is invalid.
        self.mock_tls_query.assert_not_called()
        self.mock_tcp_query.assert_not_called()
        self.mock_udp_query.assert_not_called()
        self.mock_https_query.assert_not_called()


class TestDNSQueryToolRecord(unittest.TestCase):
    """
    Tests of our record class.
    """

    def test_getitem(self) -> None:
        """
        Tests the method which let us get an item.
        """

        our_record = DNSQueryToolRecord(nameserver="hello.world", subject="world.hello")

        expected = "hello.world"
        actual = our_record.nameserver

        self.assertEqual(expected, actual)

        expected = "world.hello"
        actual = our_record["subject"]

        self.assertEqual(expected, actual)

    def test_to_dict(self) -> None:
        """
        Tests the method which let us get the dict representation of the dataset.
        """

        our_record = DNSQueryToolRecord(nameserver="hello.world", subject="world.hello")

        expected = {"nameserver": "hello.world", "subject": "world.hello"}
        actual = our_record.to_dict()

        expected_dataset = dict(actual, **expected)
        self.assertEqual(expected_dataset, our_record.to_dict())


if __name__ == "__main__":
    unittest.main()
