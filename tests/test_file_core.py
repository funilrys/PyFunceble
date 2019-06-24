# pylint:disable=line-too-long, protected-access
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.file_core.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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
from PyFunceble.file_core import FileCore


class TestsFormatLine(TestCase):
    """
    Test PyFunceble.file_core.FileCore._format_line()
    """

    def setUp(self):
        """
        Setup everything that is needed for the tests.
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
        Test the case that we encouter a simple line without decorator.
        """

        for domain in self.domains:
            expected = domain
            actual = FileCore._format_line(domain)

            self.assertEqual(expected, actual)

    def tests_comment(self):
        """
        Test the case that we encouter a commented line.
        """

        for domain in self.domains:
            expected = ""

            data = "# %s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

    def tests_ends_with_comment(self):
        """
        Test the case that a line has a comment at the end of its line.
        """

        for domain in self.domains:
            expected = domain

            data = "%s # hello world" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

    def tests_with_prefix(self):
        """
        Test the case that a line has a decorator.

        For example:
        ::

            127.0.0.1 google.com
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0 %s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1 %s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

    def tests_multiple_spaces(self):
        """
        Test the case that we have multiple space as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0                %s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1                %s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

    def tests_with_tabs(self):
        """
        Test the case that we have a single tab as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0\t%s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1\t%s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

    def tests_with_multiple_tabs(self):
        """
        Test the case that we have multiple tabs as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0\t\t\t\t\t\t\t\t\t\t%s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1\t\t\t\t\t\t\t\t\t\t\t%s" % domain
            actual = FileCore._format_line(data)

            self.assertEqual(expected, actual)


class TestSimpleColoration(TestCase):
    """
    Test PyFunceble.file_core.__get_simple_coloration().
    """

    def setUp(self):
        """
        Setup everything that is needed for the tests.
        """

        PyFunceble.load_config(generate_directory_structure=False)

    def test_green_up(self):
        """
        Test the case that we give the UP status.
        """

        expected = PyFunceble.Fore.GREEN + PyFunceble.Style.BRIGHT
        actual = FileCore.get_simple_coloration(PyFunceble.STATUS["official"]["up"])

        self.assertEqual(expected, actual)

    def test_green_valid(self):
        """
        Test the case that we give the VALID status.
        """

        expected = PyFunceble.Fore.GREEN + PyFunceble.Style.BRIGHT
        actual = FileCore.get_simple_coloration(PyFunceble.STATUS["official"]["up"])

        self.assertEqual(expected, actual)

    def test_red_inactive(self):
        """
        Test the case that we give the INACTIVE status.
        """

        expected = PyFunceble.Fore.RED + PyFunceble.Style.BRIGHT
        actual = FileCore.get_simple_coloration(PyFunceble.STATUS["official"]["down"])

        self.assertEqual(expected, actual)

    def test_cyan_invalid(self):
        """
        Test the case that we give the INVALID status.
        """

        expected = PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT
        actual = FileCore.get_simple_coloration(
            PyFunceble.STATUS["official"]["invalid"]
        )

        self.assertEqual(expected, actual)

    def test_cyan_other(self):
        """
        Test the case that we give something ellse status.
        """

        expected = PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT
        actual = FileCore.get_simple_coloration("funilrys")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
