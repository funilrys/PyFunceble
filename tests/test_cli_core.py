# pylint:disable=line-too-long, ungrouped-imports
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.cli_core.

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
import sys
from unittest import main as launch_tests

import PyFunceble

# pylint: enable=line-too-long
from helpers import BaseStdout
from PyFunceble.cli_core import CLICore


class TestsColoredLogo(BaseStdout):
    """
    Test that the colored logo is correctly printed.
    """

    def setUp(self):
        """
        Setup everything needed.
        """

        PyFunceble.initiate_colorama(True)
        PyFunceble.load_config(generate_directory_structure=False)

        BaseStdout.setUp(self)
        logo = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
"""

        self.logo_green = "\n".join(
            [
                PyFunceble.Fore.GREEN + line + PyFunceble.Fore.RESET
                for line in logo.split("\n")
            ]
        )
        self.logo_red = "\n".join(
            [
                PyFunceble.Fore.RED + line + PyFunceble.Fore.RESET
                for line in logo.split("\n")
            ]
        )

        self.logo_home = "\n".join(
            [
                PyFunceble.Fore.YELLOW + line + PyFunceble.Fore.RESET
                for line in logo.split("\n")
            ]
        )

    def tests_colored_logo_home(self):
        """
        Test if the logo is yellow colored.
        """

        CLICore.colorify_logo(home=True)

        expected = self.logo_home + "\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

    def tests_colored_logo_red(self):
        """
        Test if the logo is red colored.
        """

        PyFunceble.INTERN["counter"]["percentage"]["up"] = 1

        CLICore.colorify_logo()

        expected = self.logo_red + "\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.INTERN["counter"]["percentage"]["up"] = 0

    def tests_colored_logo_green(self):
        """
        Test if the logo is green colored.
        """

        PyFunceble.INTERN["counter"]["percentage"]["up"] = 51

        CLICore.colorify_logo()

        expected = self.logo_green + "\n"
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        PyFunceble.INTERN["counter"]["percentage"]["up"] = 0

    def tests_quiet_colored_logo(self):
        """
        Test if the logo is not printed when quiet is activated.
        """

        PyFunceble.CONFIGURATION["quiet"] = True

        CLICore.colorify_logo()

        expected = ""
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["quiet"]


class TestNothing(BaseStdout):
    """
    Test the case that there is nothing to test.
    """

    def setUp(self):
        """
        Setup everything needed for the test.
        """

        PyFunceble.initiate_colorama(True)
        BaseStdout.setUp(self)

    def test_nothing_to_test(self):
        """
        Test what we stupidly print.
        """

        expected = (
            PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT + "Nothing to test." + "\n"
        )
        CLICore.print_nothing_to_test()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
