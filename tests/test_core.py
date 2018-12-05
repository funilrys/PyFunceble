# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.core

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
# pylint: disable=protected-access, import-error, ungrouped-imports
import unittest.mock as mock  # pylint: disable=useless-import-alias
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout, sys
from PyFunceble.core import Core


class TestsResetCounters(TestCase):
    """
    Test of PyFunceble.Core.reset_counters
    """

    def setUp(self):
        """
        Setup everything that is needed for the test.
        """

        PyFunceble.load_config(True)

        self.types = ["up", "down", "invalid", "tested"]

    def set_counter(self):
        """
        Set every counter to 15.
        """

        for string in self.types:
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: 15})

    def tests_counter_set(self):
        """
        Test if the counter is really set.
        """

        self.set_counter()

        for string in self.types:
            expected = 15
            actual = PyFunceble.CONFIGURATION["counter"]["number"][string]

            self.assertEqual(expected, actual)

    def tests_reset_counters(self):
        """
        Test if the counter is reseted.
        """

        Core.reset_counters()

        for string in self.types:
            expected = 0
            actual = PyFunceble.CONFIGURATION["counter"]["number"][string]

            self.assertEqual(expected, actual)


class TestsColoredLogo(BaseStdout):
    """
    Test that the colored logo is hown correctly.
    """

    def setUp(self):
        """
        Setup everything needed.
        """

        PyFunceble.initiate(True)
        PyFunceble.load_config(True)

        BaseStdout.setUp(self)
        logo = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

"""

        self.logo_green = PyFunceble.Fore.GREEN + logo
        self.logo_red = PyFunceble.Fore.RED + logo

    def tests_colored_logo_red(self):
        """
        Test if the logo is red colored.
        """

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 1

        Core.colorify_logo()

        expected = self.logo_red
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 0

    def tests_colored_logo_green(self):
        """
        Test if the logo is green colored.
        """

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 51

        Core.colorify_logo()

        expected = self.logo_green
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 0

    def tests_quiet_colored_logo(self):
        """
        Test if the logo is not printed when quiet is activated.
        """

        PyFunceble.CONFIGURATION["quiet"] = True

        Core.colorify_logo()

        expected = ""
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["quiet"]


class TestsFormatDomain(TestCase):
    """
    Test PyFunceble.Code._format_domain()
    """

    def setUp(self):
        """
        Setup everything that is needed for the tests.
        """

        PyFunceble.load_config(True)
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
            actual = Core._format_domain(domain)

            self.assertEqual(expected, actual)

    def tests_comment(self):
        """
        Test the case that we encouter a commented line.
        """

        for domain in self.domains:
            expected = ""

            data = "# %s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

    def tests_ends_with_comment(self):
        """
        Test the case that a line has a comment at the end of its line.
        """

        for domain in self.domains:
            expected = domain

            data = "%s # hello world" % domain
            actual = Core._format_domain(data)

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
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1 %s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

    def tests_multiple_spaces(self):
        """
        Test the case that we have multiple space as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0                %s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1                %s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

    def tests_with_tabs(self):
        """
        Test the case that we have a single tab as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0\t%s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1\t%s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

    def tests_with_multiple_tabs(self):
        """
        Test the case that we have multiple tabs as sparator between
        our domain end its prefix.
        """

        for domain in self.domains:
            expected = domain

            data = "0.0.0.0\t\t\t\t\t\t\t\t\t\t%s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

        for domain in self.domains:
            expected = domain

            data = "127.0.0.1\t\t\t\t\t\t\t\t\t\t\t%s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)


class TestExtractDomain(TestCase):
    """
    Testing of the expiration date extraction subsystem.
    """

    def setUp(self):
        """
        Setup everything that is needed for the test.
        """

        PyFunceble.load_config(True)

    def test_file_does_not_exist(self):
        """
        Test the case that the given fiel does not exist.
        """

        PyFunceble.CONFIGURATION["file_to_test"] = "this_file_does_not_exit"

        self.assertRaises(FileNotFoundError, Core._extract_domain_from_file)

        del PyFunceble.CONFIGURATION["file_to_test"]

    @mock.patch("PyFunceble.path.isfile")
    def test_extracting_from_file(self, mock_isfile):
        """
        Test the extraction.
        """

        mock_isfile.return_value = True

        actual = [
            "google.com # Leaked ?",
            "facebook.com # Was it a breach or not ?",
            "#This should be ignored",
        ]
        expected = ["google.com # Leaked ?", "facebook.com # Was it a breach or not ?"]

        with mock.patch("builtins.open") as mock_open:
            mock_open.return_value.__enter__ = mock_open
            mock_open.return_value.__iter__ = mock.Mock(return_value=iter(actual))

            PyFunceble.CONFIGURATION["file_to_test"] = mock_open

            self.assertEqual(expected, Core._extract_domain_from_file())

        del PyFunceble.CONFIGURATION["file_to_test"]


class TestSwitch(TestCase):
    """
    Test the switching subsystem.
    """

    def setUp(self):
        """
        Setup everything that is needed.
        """

        PyFunceble.load_config(True)

        self.exception_message = "Impossible to switch %s. Please post an issue to https://github.com/funilrys/PyFunceble/issues."  # pylint:disable=line-too-long

    def test_index_not_exist(self):
        """
        Test the case that the switched data does not exist into
        the configuration system.
        """

        to_switch = "helloworld"

        self.assertRaisesRegex(
            Exception,
            self.exception_message % repr(to_switch),
            lambda: Core.switch(to_switch),
        )

    def test_switch_true(self):
        """
        Test the case that we want to switch a switch which is set
        to True.
        """

        PyFunceble.CONFIGURATION["helloworld"] = True

        expected = False
        actual = Core.switch("helloworld")

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["helloworld"]

    def test_switch_false(self):
        """
        Test the case that we want to switch a switch which is set
        to False.
        """

        PyFunceble.CONFIGURATION["helloworld"] = False

        expected = True
        actual = Core.switch("helloworld")

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["helloworld"]

    def test_switch_value_is_not_bool(self):
        """
        Test the case that we want to switch a switch which is not
        in bool format.
        """
        PyFunceble.CONFIGURATION["helloworld"] = "Hello, World!"

        to_switch = "helloworld"

        self.assertRaisesRegex(
            Exception,
            self.exception_message % repr(to_switch),
            lambda: Core.switch(to_switch),
        )

        del PyFunceble.CONFIGURATION["helloworld"]


if __name__ == "__main__":
    launch_tests()
