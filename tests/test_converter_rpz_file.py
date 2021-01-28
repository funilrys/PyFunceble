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

Tests of PyFunceble.converters.rpr_file

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import PyFunceble
from PyFunceble.converter.rpz_file import RPZFile


class TestRPZFileLineConverter(TestCase):
    """
    Tests of PyFunceble.converter.rpz_file
    """

    SIMPLE_SUBJECTS = [
        (
            "32.53.0.0.127.rpz-ip",
            "  32.53.0.0.127.rpz-ip              CNAME rpz-drop.   ",
        ),
        (
            "24.0.0.0.127.rpz-client-ip",
            "  24.0.0.0.127.rpz-client-ip        CNAME rpz-drop.   ",
        ),
        ("32.2.3.4.10.rpz-ip", "  32.2.3.4.10.rpz-ip                CNAME .     "),
        (
            "48.zz.101.db8.2001.rpz-client-ip",
            " 48.zz.101.db8.2001.rpz-client-ip  CNAME rpz-passthru. ",
        ),
        (
            "rpz.example.org.",
            "rpz.example.org.       3600    IN      SOA     "
            "hello.world.example.world. knock.knock.knock.knock. "
            "2020091304 3600 60 604800 60",
        ),
        (None, "$TTL 3600"),
        (None, "@ IN SOA exampledns.mydns. root.mydns. ("),
        (None, "2020091801 ; serial number"),
        (None, "3600       ; refresh 1 hour"),
        (None, "600        ; retry 10 minutes"),
        (None, "86400      ; expiry 1 week"),
        (None, "600 )      ; min ttl 10 minutes"),
        (None, "@ IN NS exampledns.mydns."),
    ]

    COMMENTED_LINES = [" ; Hello, World!", "; World, Hello! ", "    ; Hello, World!"]

    def setUp(self):
        """
        Setups everything that is needed for the tests.
        """

        PyFunceble.load_config(generate_directory_structure=False)

    def tearDown(self):
        """
        Destroys everything initiated.
        """

        PyFunceble.CONFIGURATION = None
        PyFunceble.INTERN = None

    def test_comment(self):
        """
        Tests the RPZ file line for the case that the line is a comment
        line.
        """

        expected = None

        for line in self.COMMENTED_LINES:
            actual = RPZFile(line).get_converted()

            self.assertEqual(expected, actual)

    def test_simple_line(self):
        """
        Tests the RPZ file converter for the case that a simple line is given.
        """

        for expected, line in self.SIMPLE_SUBJECTS:
            actual = RPZFile(line).get_converted()

            self.assertEqual(expected, actual)

    def test_simple_line_ends_with_comment(self):
        """
        Tests the RPZ file converter for the case that a simple commented line
        is given.
        """

        for expected, line in self.SIMPLE_SUBJECTS:
            line = line + " ; Hello, World!  "
            actual = RPZFile(line).get_converted()

            self.assertEqual(expected, actual)

    def test_multiple_entries_at_one(self):
        """
        Tests the RPZ file converter for the case that we give it multiple
        entries at once.
        """

        given = [y for _, y in self.SIMPLE_SUBJECTS]
        expected = [x for x, _ in self.SIMPLE_SUBJECTS]

        actual = RPZFile(given).get_converted()

        self.assertEqual(expected, actual)

    def test_simple_domain(self):
        """
        Tests the RPZ file converter for the case that a simple domain is given.
        """

        given = ["example.com", "example.org"]

        expected = given.copy()

        actual = RPZFile(given).get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
