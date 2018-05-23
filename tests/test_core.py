#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.core


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
# pylint: disable=protected-access, import-error, ungrouped-imports
import unittest.mock as mock
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout, sys
from PyFunceble import Fore, initiate
from PyFunceble.config import Load
from PyFunceble.core import Core


class TestsResetCounters(TestCase):
    """
    This class with test PyFunceble.reset_counters
    """

    def setUp(self):
        """
        This method setup everything that is needed for the test.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)
        self.types = ["up", "down", "invalid", "tested"]

    def set_counter(self):
        """
        This method set every counter to 15.
        """

        for string in self.types:
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: 15})

    def tests_counter_set(self):
        """
        This method will test if the counter is really set.
        """

        self.set_counter()

        for string in self.types:
            expected = 15
            actual = PyFunceble.CONFIGURATION["counter"]["number"][string]
            self.assertEqual(expected, actual)

    def tests_reset_counters(self):
        """
        This method will test if the counter is reseted.
        """

        Core.reset_counters()

        for string in self.types:
            expected = 0
            actual = PyFunceble.CONFIGURATION["counter"]["number"][string]
            self.assertEqual(expected, actual)


class TestsColoredLogo(BaseStdout):
    """
    This class will test that the colored logo is hown correctly.
    """

    def setUp(self):
        """
        This method setup everything needed.
        """

        initiate(True)
        Load(PyFunceble.CURRENT_DIRECTORY)

        BaseStdout.setUp(self)
        logo = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

"""

        self.logo_green = Fore.GREEN + logo
        self.logo_red = Fore.RED + logo

    def tests_colored_logo_red(self):
        """
        This method test if the logo is red colored.
        """

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 1

        Core.colored_logo()

        expected = self.logo_red
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 0

    def tests_colored_logo_green(self):
        """
        This method test if the logo is green colored.
        """

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 51

        Core.colored_logo()

        expected = self.logo_green
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] = 1

    def tests_quiet_colored_logo(self):
        """
        This method test if the logo is not printed when quiet is activated.
        """

        PyFunceble.CONFIGURATION["quiet"] = True

        Core.colored_logo()

        expected = ""
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)


class TestsFormatDomain(TestCase):
    """
    This class will test PyFunceble._format_domain()
    """

    def setUp(self):
        """
        This method setup everything that is needed for the tests.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)
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
        This method test the case that we encouter a simple line without decorator.
        """

        for domain in self.domains:
            expected = domain
            actual = Core._format_domain(domain)

            self.assertEqual(expected, actual)

    def tests_comment(self):
        """
        This method test the case that we encouter a commented line.
        """

        for domain in self.domains:
            expected = ""

            data = "# %s" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

    def tests_ends_with_comment(self):
        """
        This method test the case that a line has a comment at the end of its line.
        """

        for domain in self.domains:
            expected = domain

            data = "%s # hello world" % domain
            actual = Core._format_domain(data)

            self.assertEqual(expected, actual)

    def tests_with_prefix(self):
        """
        This method test the case that a line has a decorator.

        For example:
        ```
        127.0.0.1 google.com
        ```
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
        This method test the case that we have multiple space as sparator between
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
        This method test the case that we have a single tab as sparator between
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
        This method test the case that we have multiple tabs as sparator between
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


class TestAdblockDecode(TestCase):
    """
    This class will test if the adblock decoder works.
    """

    def setUp(self):
        """
        This method setup everything needed for the test.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)
        self.lines = [
            "||google.com$script,image",
            "||twitter.com^",
            "||api.google.com/papi/action$popup",
            "facebook.com###player-above-2",
            "~github.com,hello.world##.wrapper",
            "@@||cnn.com/*ad.xml",
            "!||world.hello/*ad.xml",
            "bing.com,bingo.com#@##adBanner",
            "!@@||funceble.world/js",
            "yahoo.com,msn.com,api.hello.world#@#awesomeWorld",
            "!funilrys.com##body",
            "hello#@#badads",
            "hubgit.com|oohay.com|ipa.elloh.dlorw#@#awesomeWorld",
        ]

        self.expected = [
            "google.com",
            "twitter.com",
            "api.google.com",
            "facebook.com",
            "github.com",
            "hello.world",
            "cnn.com",
            "world.hello",
            "bing.com",
            "bingo.com",
            "funceble.world",
            "api.hello.world",
            "msn.com",
            "yahoo.com",
            "funilrys.com",
            "hubgit.com",
            "ipa.elloh.dlorw",
            "oohay.com",
        ]

    def test_adblock_decode(self):
        """
        This method test that the adblock decoding system is working proprely
        """

        actual = Core.adblock_decode(Core, self.lines)

        self.assertEqual(self.expected, actual)


class TestExtractDomain(TestCase):
    """
    This class is in charge of testing the extraction system
    """

    def setUp(self):
        """
        This method setup everything that is needed for the test.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)

    def test_file_does_not_exist(self):
        """
        This method test the case that the given fiel does not exist.
        """

        PyFunceble.CONFIGURATION["file_to_test"] = "this_file_does_not_exit"

        self.assertRaises(FileNotFoundError, Core._extract_domain_from_file)

        del PyFunceble.CONFIGURATION["file_to_test"]

    @mock.patch("PyFunceble.path.isfile")
    def test_extracting_from_file(self, mock_isfile):
        """
        This method test the extraction.
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
    This class test the switching system.
    """

    def setUp(self):
        """
        This method setup everything that is needed.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)
        self.exception_message = "Impossible to switch %s. Please post an issue to https://github.com/funilrys/PyFunceble/issues."  # pylint:disable=line-too-long

    def test_index_not_exist(self):
        """
        This method test the case that the switched data does not exist into
        the system.
        """

        to_switch = "helloworld"

        self.assertRaisesRegex(
            Exception,
            self.exception_message % repr(to_switch),
            lambda: Core.switch(to_switch),
        )

    def test_switch_true(self):
        """
        This method test the case that we want to switch a switch which is set
        to True.
        """

        PyFunceble.CONFIGURATION["helloworld"] = True

        expected = False
        actual = Core.switch("helloworld")

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["helloworld"]

    def test_switch_false(self):
        """
        This method test the case that we want to switch a switch which is set
        to False.
        """

        PyFunceble.CONFIGURATION["helloworld"] = False

        expected = True
        actual = Core.switch("helloworld")

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["helloworld"]

    def test_switch_value_is_not_bool(self):
        """
        This method test the case that we want to switch a switch which is not
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
