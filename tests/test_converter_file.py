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

Tests of PyFunceble.converters.file

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

import PyFunceble
from PyFunceble.converter.file import File


class TestFileLineConverter(TestCase):
    """
    Tests of PyFunceble.converter.file
    """

    def setUp(self):
        """
        Setups everything that is needed for the tests.
        """

        PyFunceble.load_config(generate_directory_structure=False)

        self.domains = [
            "google.com",
            "twitter.com",
            "github.com",
            "facebook.com",
            "hello.world",
            "world.hello",
        ]

    def tests_simple_line(self):
        """
        Tests the case that we encouter a simple line.
        """

        for domain in self.domains:
            expected = domain
            actual = File(domain).get_converted()

            self.assertEqual(expected, actual)

    def tests_comment(self):
        """
        Tests the case that we encouter a commented line.
        """

        for domain in self.domains:
            expected = None

            data = f"# {domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_ends_with_comment(self):
        """
        Tests the case that a line has a comment at the end of its line.
        """

        for domain in self.domains:
            expected = domain

            data = f"{domain} # hello world"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_with_prefix(self):
        """
        Tests the case that a line has a decorator.

        For example:
        ::

            127.0.0.1 google.com
        """

        for domain in self.domains:
            expected = domain

            data = f"0.0.0.0 {domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = f"127.0.0.1 {domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_with_prefix_and_multiple_subjects(self):
        """
        Tests the case that a line has a decorator and multiple subjects.

        For example:
        ::

            127.0.0.1 google.com example.com example.net
        """

        for domain in self.domains:
            expected = [domain, "example.com", "example.net"]

            data = f"0.0.0.0 {domain} example.com\t\texample.net"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = [domain, "example.com", "example.net"]

            data = f"127.0.0.1 {domain} example.com\t\texample.net"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_multiple_spaces(self):
        """
        Tests the case that we have multiple space as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = f"0.0.0.0                {domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = f"127.0.0.1                {domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_with_tabs(self):
        """
        Tests the case that we have a single tab as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = f"0.0.0.0\t{domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = f"127.0.0.1\t{domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_with_multiple_tabs(self):
        """
        Tests the case that we have multiple tabs as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = f"0.0.0.0\t\t\t\t\t\t\t\t\t\t{domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = f"127.0.0.1\t\t\t\t\t\t\t\t\t\t\t{domain}"
            actual = File(data).get_converted()

            self.assertEqual(expected, actual)

    def tests_with_list_of_entries(self):
        """
        Tests the case that we give multiple entries
        """

        given = [f"0.0.0.0\t\t\t\t\t\t\t\t\t\t{domain}" for domain in self.domains]
        expected = self.domains
        actual = File(given).get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
