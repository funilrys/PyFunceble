"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of ipv4 reputation dataset.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

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

import tempfile
import unittest
import unittest.mock

from PyFunceble.dataset.ipv4_reputation import IPV4ReputationDataset


class TestIPV4ReputationDataset(unittest.TestCase):
    """
    Tests the reputation dataset interaction.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.tempfile = tempfile.NamedTemporaryFile("wb", delete=False)

        self.our_dataset = """
127.176.134.253#4#3#Malicious Host
127.34.113.192#4#2#Malicious Host
127.34.107.238#4#2#Malicious Host
127.166.193.125#4#2#Malicious Host
127.179.153.18#4#2#Malicious Host
127.89.243.30#4#2#Malicious Host
127.147.142.53#4#2#Malicious Host
127.35.150.233#4#3#Malicious Host
127.97.172.196#4#2#Malicious Host
127.24.78.18#4#2#Malicious Host
"""

        self.tempfile.write(self.our_dataset.encode())
        self.tempfile.seek(0)

        self.ipv4_reputation_dataset = IPV4ReputationDataset()
        self.ipv4_reputation_dataset.source_file = self.tempfile.name

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.tempfile
        del self.our_dataset
        del self.ipv4_reputation_dataset

    def test_contains(self) -> None:
        """
        Tests of the method which let us check if a given IP is into the
        dataset.
        """

        given = "127.24.78.18"

        expected = True
        actual = given in self.ipv4_reputation_dataset

        self.assertEqual(expected, actual)

    def test_not_contains(self) -> None:
        """
        Tests of the method which let us check if a given IP is into the
        dataset.

        In this case, we check against something which does not exists.
        """

        given = "192.168.78.1"

        expected = False
        actual = given in self.ipv4_reputation_dataset

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
