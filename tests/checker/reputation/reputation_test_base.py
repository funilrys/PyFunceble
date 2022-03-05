"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

A module that provides some abstract class for the reputation tests.

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


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

import os
import tempfile
import unittest
from typing import List, Optional

from PyFunceble.checker.reputation.base import ReputationCheckerBase


class ReputationCheckerTestBase(unittest.TestCase):
    """
    Tests of the base of all our reputation checker.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.checker = ReputationCheckerBase()

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

        self.checker.ipv4_reputation_query_tool.source_file = self.tempfile.name

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        self.tempfile.close()

        os.unlink(self.tempfile.name)

        del self.checker

    @staticmethod
    def fake_query_a_record(*args, **kwargs) -> Optional[List[str]]:
        """
        A fake method which provides a fake IP for the testing.
        """

        _ = args
        _ = kwargs

        return ["127.176.134.253"]

    @staticmethod
    def fake_query_a_record_none(*args, **kwargs) -> Optional[List[str]]:
        """
        A fake method which provides a fake IP for the testing.
        """

        _ = args
        _ = kwargs

    @staticmethod
    def fake_query_a_record_not_known(*args, **kwargs) -> Optional[List[str]]:
        """
        A fake method which provides a fake IP for the testing.
        """

        _ = args
        _ = kwargs

        return ["93.184.216.34"]
