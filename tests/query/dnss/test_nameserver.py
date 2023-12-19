"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our nameserver manager.

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

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import dataclasses
import unittest
import unittest.mock

import dns.exception
import dns.resolver

from PyFunceble.config.loader import ConfigLoader
from PyFunceble.query.dns.nameserver import Nameservers

try:
    import pyf_test_dataset
except (ModuleNotFoundError, ImportError):  # pragma: no cover
    try:
        from .. import pyf_test_dataset
    except (ModuleNotFoundError, ImportError):
        from ... import pyf_test_dataset

# pylint: disable=invalid-field-call


class TestNameserver(unittest.TestCase):
    """
    Tests our nameserver "manager".
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.config_loader = ConfigLoader()
        self.config_loader.start()

        self.nameserver_provider = Nameservers()

    def tearDown(self) -> None:
        """
        Destroys everything previously initiated.
        """

        del self.config_loader

    @staticmethod
    def fake_resolve_response(
        data: str,
    ) -> object:
        """
        Provides a fake resolve response to use.
        """

        return dataclasses.make_dataclass(
            "FakeResponse", [("address", str, dataclasses.field(default=data))]
        )

    @staticmethod
    def fake_resolver(_: str, rqtype: str):
        """
        Provides a fake resolution.
        """

        if rqtype == "A":
            return [
                TestNameserver.fake_resolve_response("192.168.1.1"),
                TestNameserver.fake_resolve_response("10.47.91.9"),
            ]

        return [
            TestNameserver.fake_resolve_response("fe80::6b01:9045:a42a:fb5f"),
            TestNameserver.fake_resolve_response("fe80::6b01:9049:a42a:fb5f"),
        ]

    def test_split_nameserver_from_port(self) -> None:
        """
        Tests the method which let us split the nameserver from the port.
        """

        given = "example.org:45"

        expected = ("example.org", 45)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    def test_split_nameserver_from_port_no_port(self) -> None:
        """
        Tests the method which let us split the nameserver from the port for the
        case that no port is given.
        """

        given = "example.org"

        expected = ("example.org", 53)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    def test_split_nameserver_from_port_not_correct(self) -> None:
        """
        Tests the method which let us split the nameserver from the port for the
        case that the port is incorrectly given.
        """

        given = "10.0.0.1:ed"

        expected = ("10.0.0.1", 53)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    def test_split_nameserver_from_port_ipv6_no_port(self) -> None:
        """
        Tests the method which let us split the nameserver from the port for the
        case that an IPv6 is given and no port.
        """

        given = pyf_test_dataset.VALID_IPV6[0]

        expected = (pyf_test_dataset.VALID_IPV6[0], 53)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    def test_split_nameserver_from_port_ipv6_with_port(self) -> None:
        """
        Tests the method which let us split the nameserver from the port for the
        case that an IPv6 is given and no port.
        """

        given = f"{pyf_test_dataset.VALID_IPV6[1]}:55"

        expected = (f"{pyf_test_dataset.VALID_IPV6[1]}:55", 53)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    def test_split_nameserver_from_port_ipv6_convention(self) -> None:
        """
        Tests the method which let us split the nameserver from the port.

        In this case we are trying to follow the :code:`[ip]:port` convention.
        """

        given = f"[{pyf_test_dataset.VALID_IPV6[1]}]:55"

        expected = (pyf_test_dataset.VALID_IPV6[1], 55)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    def test_split_nameserver_from_port_ipv6_convention_port_not_digit(self) -> None:
        """
        Tests the method which let us split the nameserver from the port.

        In this case we are trying to follow the :code:`[ip]:port` convention
        but the port is not a correct one..
        """

        given = f"[{pyf_test_dataset.VALID_IPV6[1]}]:ef"

        expected = (pyf_test_dataset.VALID_IPV6[1], 53)
        actual = self.nameserver_provider.split_nameserver_from_port(given)

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(dns.resolver.Resolver, "resolve")
    def test_get_ip_from_nameserver(self, resolver_patch) -> None:
        """
        Tests the method which let us get the IP from a nameserver.
        """

        resolver_patch.side_effect = self.fake_resolver

        given = "example.org"

        expected = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        actual = self.nameserver_provider.get_ip_from_nameserver(given)

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(dns.resolver.Resolver, "resolve")
    def test_get_ip_from_nameserver_exceptions(self, resolver_patch) -> None:
        """
        Tests the method which let us get the IP from a nameserver for the
        case that only exceptions are given back.
        """

        resolver_patch.side_effect = dns.exception.DNSException("This is a test :-)")

        given = "example.org"

        expected = []
        actual = self.nameserver_provider.get_ip_from_nameserver(given)

        self.assertEqual(expected, actual)

    def test_get_ip_from_nameserver_not_valid_domain(self) -> None:
        """
        Tests the method which let us get the IP from a nameserver for the
        case that a private domain is given.
        """

        given = "example.funilrys"

        expected = ["example.funilrys"]
        actual = self.nameserver_provider.get_ip_from_nameserver(given)

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(dns.resolver.Resolver, "resolve")
    def test_set_nameservers(self, resolver_patch) -> None:
        """
        Tests the method which let us set the nameserver to work with.
        """

        resolver_patch.side_effect = self.fake_resolver

        given = ["example.org:53"]

        expected_nameserver = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        expected_nameserver_port = {
            "192.168.1.1": 53,
            "10.47.91.9": 53,
            "fe80::6b01:9045:a42a:fb5f": 53,
            "fe80::6b01:9049:a42a:fb5f": 53,
        }

        self.nameserver_provider.set_nameservers(given)

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

    @unittest.mock.patch.object(dns.resolver.Resolver, "resolve")
    def test_set_nameservers_through_init(self, resolver_patch) -> None:
        """
        Tests the method which let us set the nameserver from the contributor
        method.
        """

        resolver_patch.side_effect = self.fake_resolver

        given = ["example.org:53"]

        expected_nameserver = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        expected_nameserver_port = {
            "192.168.1.1": 53,
            "10.47.91.9": 53,
            "fe80::6b01:9045:a42a:fb5f": 53,
            "fe80::6b01:9049:a42a:fb5f": 53,
        }

        nameserver_obj = Nameservers(nameserver=given)

        actual = nameserver_obj.get_nameservers()
        actual_nameserver_port = nameserver_obj.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

    def test_set_nameservers_https(self) -> None:
        """
        Tests the method which let us set the nameserver to work with for the
        case that a URL is given.
        """

        given = ["https://example.org/dns-query", "https://example.net/dns-query"]

        expected_nameserver = [
            "https://example.org/dns-query",
            "https://example.net/dns-query",
        ]
        expected_nameserver_port = {
            "https://example.org/dns-query": 443,
            "https://example.net/dns-query": 443,
        }

        self.nameserver_provider.protocol = "HTTPS"
        self.nameserver_provider.set_nameservers(given)

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

    def test_set_nameservers_https_no_scheme(self) -> None:
        """
        Tests the method which let us set the nameserver to work with for the
        case that a URL is given.

        Now, we test for the case that no scheme is provided.
        """

        given = ["example.org/dns-query", "example.net/dns-query"]

        expected_nameserver = [
            "https://example.org/dns-query",
            "https://example.net/dns-query",
        ]
        expected_nameserver_port = {
            "https://example.org/dns-query": 443,
            "https://example.net/dns-query": 443,
        }

        self.nameserver_provider.protocol = "HTTPS"
        self.nameserver_provider.set_nameservers(given)

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

    def test_set_nameservers_https_no_scheme_and_path(self) -> None:
        """
        Tests the method which let us set the nameserver to work with for the
        case that a URL is given.

        Now, we test for the case that no scheme and explicit path is provided.
        """

        given = ["example.org", "example.net"]

        expected_nameserver = [
            "https://example.org",
            "https://example.net",
        ]
        expected_nameserver_port = {
            "https://example.org": 443,
            "https://example.net": 443,
        }

        self.nameserver_provider.protocol = "HTTPS"
        self.nameserver_provider.set_nameservers(given)

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

    def test_set_nameservers_not_list(self) -> None:
        """
        Tests the method which let us set the nameserver to work with for the
        case that the given value is not a list.
        """

        given = "Hello, World!"

        self.assertRaises(
            TypeError, lambda: self.nameserver_provider.set_nameservers(given)
        )

    def test_set_nameservers_empty_list(self) -> None:
        """
        Tests the method which let us set the nameserver to work with for the
        case that the given value is an empty list.
        """

        given = []

        self.assertRaises(ValueError, lambda: Nameservers().set_nameservers(given))

    @unittest.mock.patch.object(dns.resolver.Resolver, "resolve")
    def test_guess_and_set_nameservers(self, resolver_patch) -> None:
        """
        Tests the method which let us guess the nameserver to use.
        """

        resolver_patch.side_effect = self.fake_resolver

        given = ["example.org:53"]

        expected_nameserver = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        expected_nameserver_port = {
            "192.168.1.1": 53,
            "10.47.91.9": 53,
            "fe80::6b01:9045:a42a:fb5f": 53,
            "fe80::6b01:9049:a42a:fb5f": 53,
        }

        self.config_loader.set_custom_config({"dns": {"server": given}}).start()

        self.nameserver_provider.guess_and_set_nameservers()

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

        self.config_loader.set_custom_config({"dns": {"server": given[0]}}).start()

        self.nameserver_provider.guess_and_set_nameservers()

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)

    @unittest.mock.patch.object(dns.resolver, "get_default_resolver")
    def test_guess_and_set_nameservers_no_default_resolver(
        self, get_default_resolver_patch
    ) -> None:
        """
        Tests the method which let us guess the nameserver to use for the case that
        no resolver has been found.
        """

        def fake_get_default_resolver(*args, **kwargs):
            raise dns.resolver.dns.resolver.NoResolverConfiguration("no nameservers")

        get_default_resolver_patch.side_effect = fake_get_default_resolver

        expected_nameserver = [
            "9.9.9.10",
            "149.112.112.10",
            "2620:fe::10",
            "2620:fe::fe:10",
        ]
        expected_nameserver_port = {
            "9.9.9.10": 53,
            "149.112.112.10": 53,
            "2620:fe::10": 53,
            "2620:fe::fe:10": 53,
        }

        self.config_loader.set_custom_config({"dns": {"server": []}}).start()

        self.nameserver_provider.guess_and_set_nameservers()

        actual = self.nameserver_provider.get_nameservers()
        actual_nameserver_port = self.nameserver_provider.get_nameserver_ports()

        self.assertEqual(expected_nameserver, actual)
        self.assertEqual(expected_nameserver_port, actual_nameserver_port)


if __name__ == "__main__":
    unittest.main()
