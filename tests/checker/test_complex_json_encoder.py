"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our URL availability checker.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025 Nissar Chababy

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
import datetime
import json
import unittest

import dns.name

from PyFunceble.checker.complex_json_encoder import ComplexJsonEncoder


@dataclasses.dataclass
class SampleDataClass:
    """
    A sample dataclass for testing.
    """

    field1: int
    field2: str


class TestComplexJsonEncoder(unittest.TestCase):
    """
    Tests of our complex JSON encoder.
    """

    def test_encode_dataclass(self):
        """
        Tests the case that we encode a dataclass.
        """

        data = SampleDataClass(field1=1, field2="test")
        expected = '{"field1": 1, "field2": "test"}'
        actual = json.dumps(data, cls=ComplexJsonEncoder)

        self.assertEqual(expected, actual)

    def test_encode_dns_name(self):
        """
        Tests the case that we encode a dns.name object.
        """

        dns_name = dns.name.from_text("example.com")
        expected = '"example.com."'
        actual = json.dumps(dns_name, cls=ComplexJsonEncoder)

        self.assertEqual(expected, actual)

    def test_encode_datetime(self):
        """
        Tests the case that we encode a datetime object.
        """

        timestamp = datetime.datetime(2023, 10, 5, 12, 30, 45)
        expected = '"2023-10-05T12:30:45"'
        actual = json.dumps(timestamp, cls=ComplexJsonEncoder)
        self.assertEqual(expected, actual)

    def test_encode_default(self):
        """
        Tests the case that we encode any other object.
        """

        data = {"key": "value"}
        expected = '{"key": "value"}'
        actual = json.dumps(data, cls=ComplexJsonEncoder)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
