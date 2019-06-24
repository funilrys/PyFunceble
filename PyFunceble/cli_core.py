# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provide some functions which are specific to the CLI usage.

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

from random import choice

import PyFunceble
from PyFunceble.prints import Prints


class CLICore:
    """
    Provide some methods which are dedicated for the CLI.
    """

    @classmethod
    def colorify_logo(cls, home=False):
        """
        Print the colored logo based on global results.

        :param bool home: Tell us if we have to print the initial coloration.
        """

        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            to_print = []

            if home:
                # We have to print the initial logo.

                for line in PyFunceble.ASCII_PYFUNCEBLE.split("\n"):
                    # We loop through each lines of the ASCII representation
                    # of PyFunceble.

                    # And we append to the data to print the currently read
                    # line with the right coloration.
                    to_print.append(
                        PyFunceble.Fore.YELLOW + line + PyFunceble.Fore.RESET
                    )

            elif PyFunceble.INTERN["counter"]["percentage"]["up"] >= 50:
                # The percentage of up is greater or equal to 50%.

                for line in PyFunceble.ASCII_PYFUNCEBLE.split("\n"):
                    # We loop through each lines of the ASCII representation
                    # of PyFunceble.

                    # And we append to the data to print the currently read
                    # line with the right coloration.
                    to_print.append(
                        PyFunceble.Fore.GREEN + line + PyFunceble.Fore.RESET
                    )
            else:
                # The percentage of up is less than 50%.

                for line in PyFunceble.ASCII_PYFUNCEBLE.split("\n"):
                    # We loop through each lines of the ASCII representation
                    # of PyFunceble.

                    # And we append to the data to print the currently read
                    # line with the right coloration.
                    to_print.append(PyFunceble.Fore.RED + line + PyFunceble.Fore.RESET)

            print("\n".join(to_print))

    @classmethod
    def print_header(cls):  # pragma: no cover
        """
        Print the header if needed.
        """

        if (
            not PyFunceble.CONFIGURATION["quiet"]
            and not PyFunceble.CONFIGURATION["header_printed"]
        ):
            # * The quiet mode is not activated.
            # and
            # * The header has not been already printed.

            # We print a new line.
            print("\n")

            if PyFunceble.CONFIGURATION["less"]:
                # We have to show less informations on screen.

                # We print the `Less` header.
                Prints(None, "Less").header()
            else:
                # We have to show every informations on screen.

                # We print the `Generic` header.
                Prints(None, "Generic").header()

            # The header was printed.

            # We initiate the variable which say that the header has been printed to True.
            PyFunceble.CONFIGURATION["header_printed"] = True

    @classmethod
    def print_nothing_to_test(cls):
        """
        Print the nothing to test message.
        """

        print(PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT + "Nothing to test.")

    @classmethod
    def stay_safe(cls):  # pragma: no cover
        """
        Print a friendly message.
        """

        random = int(choice(str(int(PyFunceble.time()))))

        if not PyFunceble.CONFIGURATION["quiet"]:
            print(
                "\n"
                + PyFunceble.Fore.GREEN
                + PyFunceble.Style.BRIGHT
                + "Thanks for using PyFunceble!"
            )

            if random % 3 == 0:
                print(
                    PyFunceble.Fore.YELLOW
                    + PyFunceble.Style.BRIGHT
                    + "Share your experience on "
                    + PyFunceble.Fore.CYAN
                    + "Twitter"
                    + PyFunceble.Fore.YELLOW
                    + " with "
                    + PyFunceble.Fore.CYAN
                    + "#PyFunceble"
                    + PyFunceble.Fore.YELLOW
                    + "!"
                )
                print(
                    PyFunceble.Fore.GREEN
                    + PyFunceble.Style.BRIGHT
                    + "Have a feedback, an issue or an improvement idea ?"
                )
                print(
                    PyFunceble.Fore.YELLOW
                    + PyFunceble.Style.BRIGHT
                    + "Let us know on "
                    + PyFunceble.Fore.CYAN
                    + "GitHub"
                    + PyFunceble.Fore.YELLOW
                    + "!"
                )

    @classmethod
    def logs_sharing(cls):  # pragma: no cover
        """
        Print an information message when the logs sharing
        is activated.
        """

        if PyFunceble.CONFIGURATION["share_logs"]:
            print(
                PyFunceble.Fore.GREEN
                + PyFunceble.Style.BRIGHT
                + "You are sharing your logs!"
            )
            print(
                PyFunceble.Fore.MAGENTA
                + PyFunceble.Style.BRIGHT
                + "Please find more about it at "
                "https://pyfunceble.readthedocs.io/en/dev/logs-sharing.html !"
            )
