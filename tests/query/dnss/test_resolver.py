"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our resolver provider.

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
import unittest
import unittest.mock

import dns.resolver

from PyFunceble.config.loader import ConfigLoader
from PyFunceble.query.dns.resolver import Resolver


class TestResolver(unittest.TestCase):
    """
    Provides the tests of our resolver configurator.
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

        self.mock_resolve = self.resolve_patch.start()
        self.mock_resolve.side_effect = fake_resolver

        self.resolver_provider = Resolver()

    def tearDown(self) -> None:
        """
        Destroys everything previously initiated for the tests.
        """

        self.resolve_patch.stop()

        del self.resolve_patch
        del self.mock_resolve

        del self.resolver_provider

    def test_set_nameservers(self) -> None:
        """
        Tests the method which let us set the nameservers to work with.
        """

        given = ["example.org"]

        self.resolver_provider.set_nameservers(given)

        expected = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        actual = self.resolver_provider.get_nameservers()

        self.assertEqual(expected, actual)

        expected = {
            "192.168.1.1": 53,
            "10.47.91.9": 53,
            "fe80::6b01:9045:a42a:fb5f": 53,
            "fe80::6b01:9049:a42a:fb5f": 53,
        }
        actual = self.resolver_provider.get_nameserver_ports()

        self.assertEqual(expected, actual)

    def test_set_nameservers_through_init(self) -> None:
        """
        Tests the method which let us set the nameservers to work with.

        Here we check the case that the nameservers are given through the
        constructor.
        """

        given = ["example.org"]

        resolver_provider = Resolver(nameservers=given)

        expected = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        actual = resolver_provider.get_nameservers()

        self.assertEqual(expected, actual)

        expected = {
            "192.168.1.1": 53,
            "10.47.91.9": 53,
            "fe80::6b01:9045:a42a:fb5f": 53,
            "fe80::6b01:9049:a42a:fb5f": 53,
        }
        actual = resolver_provider.get_nameserver_ports()

        self.assertEqual(expected, actual)

    def test_set_timeout(self) -> None:
        """
        Tests the method which let us set the timeout to apply.
        """

        given = 4.0

        self.resolver_provider.set_timeout(given)

        expected = 4.0
        actual = self.resolver_provider.get_timeout()

        self.assertEqual(expected, actual)

    def test_set_timeout_though_init(self) -> None:
        """
        Tests the method which let us set the timeout to apply.

        Here we check the case that the timeout is given through the
        constructor.
        """

        given = 4.0

        resolver_provider = Resolver(timeout=given)

        expected = 4.0
        actual = resolver_provider.get_timeout()

        self.assertEqual(expected, actual)

    def test_set_timeout_not_float_nor_int(self) -> None:
        """
        Tests the method which let us set the timeout to apply for the case that
        it's not an int nor a float.
        """

        given = "Hello, World!"

        self.assertRaises(TypeError, lambda: self.resolver_provider.set_timeout(given))

    def test_guess_and_set_timeout(self) -> None:
        """
        Tests the method which let us guess the timeout to use.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"lookup": {"timeout": 10.0}}).start()

        self.resolver_provider.guess_and_set_timeout()

        expected = 10.0
        actual = self.resolver_provider.get_timeout()

        self.assertEqual(expected, actual)

    def test_get_resolver(self) -> None:
        """
        Tests the method which let us get the configured resolver.
        """

        self.resolver_provider.set_nameservers(["example.org"])
        self.resolver_provider.set_timeout(5.0)

        the_resolver = self.resolver_provider.get_resolver()

        expected_timeout = 5.0
        expected_lifetime = 7.0
        expected_nameservers = [
            "192.168.1.1",
            "10.47.91.9",
            "fe80::6b01:9045:a42a:fb5f",
            "fe80::6b01:9049:a42a:fb5f",
        ]
        expected_nameserver_ports = {
            "192.168.1.1": 53,
            "10.47.91.9": 53,
            "fe80::6b01:9045:a42a:fb5f": 53,
            "fe80::6b01:9049:a42a:fb5f": 53,
        }

        self.assertEqual(expected_timeout, the_resolver.timeout)
        self.assertEqual(expected_lifetime, the_resolver.lifetime)
        self.assertEqual(expected_nameservers, the_resolver.nameservers)
        self.assertEqual(expected_nameserver_ports, the_resolver.nameserver_ports)

        # Let's test the recall :-)

        the_second_resolver = self.resolver_provider.get_resolver()

        self.assertEqual(id(the_resolver), id(the_second_resolver))


if __name__ == "__main__":
    unittest.main()
