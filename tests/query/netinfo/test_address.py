"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our address info class.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

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

import socket
import unittest
import unittest.mock

from PyFunceble.query.netinfo.address import AddressInfo


class TestAddressInfo(unittest.TestCase):
    """
    Tests the of the interface which let us get the information about an
    address.
    """

    @unittest.mock.patch.object(socket, "getaddrinfo")
    def test_get_info(self, addrinfo_path: unittest.mock.MagicMock) -> None:
        """
        Tests the method which let us get the information to work with.
        """

        def fake_getattrinfo(*args, **kwargs):
            _ = args
            _ = kwargs
            return [("192.169.1.1", "10.20.30.40", ["10.55.0.32"])]

        addrinfo_path.side_effect = fake_getattrinfo

        given = "example.org"

        expected = ["10.55.0.32"]
        actual = AddressInfo(given).get_info()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(socket, "getaddrinfo")
    def test_get_info_gaierror(self, addrinfo_path: unittest.mock.MagicMock) -> None:
        """
        Tests the method which let us get the information to work with for the
        case that we get an gaierror exception.
        """

        def fake_getattrinfo(*args, **kwargs):
            raise socket.gaierror("This is a test :-)")

        addrinfo_path.side_effect = fake_getattrinfo

        given = "example.org"

        expected = []
        actual = AddressInfo(given).get_info()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(socket, "getaddrinfo")
    def test_get_info_herror(self, addrinfo_path: unittest.mock.MagicMock) -> None:
        """
        Tests the method which let us get the information to work with for the
        case that we get an herror exception.
        """

        def fake_getattrinfo(*args, **kwargs):
            raise socket.herror("This is a test :-)")

        addrinfo_path.side_effect = fake_getattrinfo

        given = "example.org"

        expected = []
        actual = AddressInfo(given).get_info()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
