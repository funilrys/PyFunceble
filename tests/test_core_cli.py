# pylint:disable=line-too-long,invalid-name,import-error
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the PyFunceble.core.cli

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
# pylint: enable=line-too-long

import sys
from datetime import datetime
from unittest import main as launch_tests
from unittest.mock import Mock, patch

from colorama import Fore, Style
from colorama import init as init_colorama

import PyFunceble
from PyFunceble.core import CLI
from stdout_base import StdoutBase
from time_zone import TZ


class TestCLICore(StdoutBase):
    """
    Tests of the PyFunceble.core.cli.
    """

    # pylint: disable=unsubscriptable-object

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        init_colorama(autoreset=True)

        PyFunceble.load_config()

        StdoutBase.setUp(self)

        self.green_ascii = "\n".join(
            [
                f"{Fore.GREEN}{x}{Fore.RESET}"
                for x in PyFunceble.ASCII_PYFUNCEBLE.split("\n")
            ]
        )
        self.red_ascii = "\n".join(
            [
                f"{Fore.RED}{x}{Fore.RESET}"
                for x in PyFunceble.ASCII_PYFUNCEBLE.split("\n")
            ]
        )
        self.home_ascii = "\n".join(
            [
                f"{Fore.YELLOW}{x}{Fore.RESET}"
                for x in PyFunceble.ASCII_PYFUNCEBLE.split("\n")
            ]
        )

        self.cli_core = CLI()

    def test_get_coloration(self):
        """
        Tests the method which give use the right coloration from a given status.
        """

        colors = {
            f"{Fore.GREEN}{Style.BRIGHT}": [
                PyFunceble.STATUS.official.up,
                PyFunceble.STATUS.official.valid,
            ],
            f"{Fore.RED}{Style.BRIGHT}": [PyFunceble.STATUS.official.down],
        }

        expected = f"{Fore.CYAN}{Style.BRIGHT}"
        actual = self.cli_core.get_simple_coloration(PyFunceble.STATUS.official.invalid)

        self.assertEqual(expected, actual)

        for expected, statuses in colors.items():
            for status in statuses:
                actual = self.cli_core.get_simple_coloration(status)

                self.assertEqual(expected, actual)

    def test_colored_ascii_home(self):
        """
        Tests the method which colors the ASCII representation of PyFunceble
        for the case that we want the home representation.
        """

        self.cli_core.colorify_logo(home=True)

        expected = f"{self.home_ascii}\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

    def test_colored_ascii_error(self):
        """
        Tests the method which colors the ASCII representation of PyFunceble
        for the case that we want the error representation.
        """

        PyFunceble.INTERN["counter"]["percentage"]["down"] = 55

        self.cli_core.colorify_logo()

        expected = f"{self.red_ascii}\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.INTERN["counter"]["percentage"]["down"] = 0

    def test_colored_ascii_success(self):
        """
        Tests the method which colors the ASCII representation of PyFunceble
        for the case that we want the success representation.
        """

        PyFunceble.INTERN["counter"]["percentage"]["up"] = 55

        self.cli_core.colorify_logo()

        expected = f"{self.green_ascii}\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.INTERN["counter"]["percentage"]["up"] = 0

    def test_colored_ascii_success_syntax(self):
        """
        Tests the method which colors the ASCII representation of PyFunceble
        for the case that we want the success representation for the case
        that we are testing for syntax.
        """

        PyFunceble.INTERN["counter"]["percentage"]["valid"] = 55

        self.cli_core.colorify_logo()

        expected = f"{self.green_ascii}\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.INTERN["counter"]["percentage"]["valid"] = 0

    def test_nothing_to_test(self):
        """
        Tests the correctness of the desired message.
        """

        expected = f"{Fore.CYAN}{Style.BRIGHT}Nothing to test.\n"
        self.cli_core.print_nothing_to_test()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

    @patch("datetime.datetime")
    def test_stay_safe(self, datetime_patch):
        """
        Tests the correctness of the desired message.
        """

        self.tearDown()
        self.setUp()

        expected = f"""
{Fore.GREEN}{Style.BRIGHT}Thanks for using PyFunceble!
"""

        datetime_patch = Mock(wraps=datetime)
        datetime_patch.now = Mock(
            return_value=datetime(1970, 1, 1, 1, 0, 2, 0, tzinfo=TZ("+", hours=1).get())
        )
        patch("PyFunceble.core.cli.datetime", new=datetime_patch).start()

        CLI().stay_safe()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

    @patch("datetime.datetime")
    def test_stay_safe_share_experiance(self, datetime_patch):
        """
        Tests the correctness of the desired message.
        """

        self.tearDown()
        self.setUp()

        expected = f"""
{Fore.GREEN}{Style.BRIGHT}Thanks for using PyFunceble!
{Fore.YELLOW}{Style.BRIGHT}Share your experience on {Fore.CYAN}Twitter{Fore.YELLOW} with {Fore.CYAN}#PyFunceble{Fore.YELLOW}!
{Fore.GREEN}{Style.BRIGHT}Have a feedback, an issue or an improvement idea?
{Fore.YELLOW}{Style.BRIGHT}Let us know on {Fore.CYAN}GitHub{Fore.YELLOW}!
"""

        datetime_patch = Mock(wraps=datetime)
        datetime_patch.now = Mock(
            return_value=datetime(1970, 1, 1, 1, 0, 3, 0, tzinfo=TZ("+", hours=1).get())
        )
        patch("PyFunceble.core.cli.datetime", new=datetime_patch).start()

        CLI().stay_safe()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

    def test_log_sharing(self):
        """
        Tests the correctness of the desired message.
        """

        PyFunceble.CONFIGURATION.share_logs = True

        expected = f"""{Fore.GREEN}{Style.BRIGHT}You are sharing your logs!
{Fore.MAGENTA}{Style.BRIGHT}Please find more about it at https://pyfunceble.readthedocs.io/en/dev/logs-sharing.html !
"""
        self.cli_core.logs_sharing()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
