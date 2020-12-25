"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the RPZ input line 2 subject converter.

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

import unittest
from typing import List, Optional, Tuple

from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject


class TestRPZInputLine2Subject(unittest.TestCase):
    """
    Tests of our RPZ line 2 subject(s).
    """

    TEST_SUBJECT_SIMPLE: List[Tuple[Optional[List[str]], str]] = [
        (
            ["32.53.0.0.127.rpz-ip"],
            "  32.53.0.0.127.rpz-ip              CNAME rpz-drop.   ",
        ),
        (
            ["24.0.0.0.127.rpz-client-ip"],
            "  24.0.0.0.127.rpz-client-ip        CNAME rpz-drop.   ",
        ),
        (["32.2.3.4.10.rpz-ip"], "  32.2.3.4.10.rpz-ip                CNAME .     "),
        (
            ["48.zz.101.db8.2001.rpz-client-ip"],
            " 48.zz.101.db8.2001.rpz-client-ip  CNAME rpz-passthru. ",
        ),
        (
            ["rpz.example.org."],
            "rpz.example.org.       3600    IN      SOA     "
            "hello.world.example.world. knock.knock.knock.knock. "
            "2020091304 3600 60 604800 60",
        ),
        ([], "$TTL 3600"),
        ([], "@ IN SOA exampledns.mydns. root.mydns. ("),
        ([], "2020091801 ; serial number"),
        ([], "3600       ; refresh 1 hour"),
        ([], "600        ; retry 10 minutes"),
        ([], "86400      ; expiry 1 week"),
        ([], "600 )      ; min ttl 10 minutes"),
        ([], "@ IN NS exampledns.mydns."),
    ]

    TEST_SUBJEC_COMMENTED_LINES: List[str] = [
        " ; Hello, World!",
        "; World, Hello! ",
        "    ; Hello, World!",
    ]

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = RPZInputLine2Subject()

    def tearDown(self) -> None:
        """
        Destroys everything previously created for the tests.
        """

        del self.converter

    def test_get_converted_comment(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given data is a comment line.
        """

        expected = []

        for line in self.TEST_SUBJEC_COMMENTED_LINES:
            self.converter.data_to_convert = line
            actual = self.converter.get_converted()

            self.assertEqual(expected, actual)

    def test_get_converted_simple_line(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given data is a simple understandable line.
        """

        for expected, line in self.TEST_SUBJECT_SIMPLE:
            self.converter.data_to_convert = line
            actual = self.converter.get_converted()

            self.assertEqual(expected, actual)

    def test_get_converted_simple_line_with_commend(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the given data is a simple line which ends with a commment.
        """

        for expected, line in self.TEST_SUBJECT_SIMPLE:
            self.converter.data_to_convert = f"{line} ; Hello, World!"
            actual = self.converter.get_converted()

            self.assertEqual(expected, actual)

    def test_get_converted_simple_domain(self) -> None:
        """
        Tests the method which let get the converted data for the case that the
        given data is a simple domain.
        """

        given = "example.com"
        expected = ["example.com"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
