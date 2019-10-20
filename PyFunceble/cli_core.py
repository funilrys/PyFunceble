# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

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

        if not PyFunceble.CONFIGURATION.quiet:
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
            not PyFunceble.CONFIGURATION.quiet
            and not PyFunceble.CONFIGURATION.header_printed
        ):
            # * The quiet mode is not activated.
            # and
            # * The header has not been already printed.

            # We print a new line.
            print("\n")

            if PyFunceble.CONFIGURATION.less:
                # We have to show less informations on screen.

                # We print the `Less` header.
                Prints(None, "Less").header()
            else:
                # We have to show every informations on screen.

                # We print the `Generic` header.
                Prints(None, "Generic").header()

            # The header was printed.

            # We initiate the variable which say that the header has been printed to True.
            PyFunceble.CONFIGURATION.header_printed = True

    @classmethod
    def print_nothing_to_test(cls):  # pragma: no cover
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

        if not PyFunceble.CONFIGURATION.quiet:
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

        if PyFunceble.CONFIGURATION.share_logs:
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

    @classmethod
    def get_upstream_version_file(cls):  # pragma: no cover
        """
        Provides the upstream version file.
        """

        # We initiate the link to the upstream version file.
        # It is hard coded because we may not have the chance to have the
        # configuration file everytime we need it.
        upstream_link = (
            "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/version.yaml"
        )  # pylint: disable=line-too-long

        upstream_link = PyFunceble.converters.InternalUrl(upstream_link).get_converted()

        return PyFunceble.helpers.Dict().from_yaml(
            PyFunceble.helpers.Download(upstream_link).text()
        )

    @classmethod
    def __check_force_update(cls, upstream_version):  # pragma: no cover
        """
        Checks if we need to force the update.

        If it's the case, we will stop the tool.
        """

        if upstream_version["force_update"]["status"]:
            for minimal in upstream_version["force_update"]["minimal_version"]:
                # We loop through the list of minimal version which trigger the
                # the force update message.

                # We compare the local with the currently read minimal version.
                checked = PyFunceble.abstracts.Version.compare(minimal)

                if not PyFunceble.CONFIGURATION.quiet:
                    # The quiet mode is not activated.

                    if checked or checked is not False and not checked:
                        # The current version is less or equal to
                        # the minimal version.

                        # We initiate the message we are going to return to
                        # the user.
                        message = (
                            PyFunceble.Style.BRIGHT
                            + PyFunceble.Fore.RED
                            + "A critical issue has been fixed.\n"
                            + PyFunceble.Style.RESET_ALL
                        )  # pylint:disable=line-too-long
                        message += (
                            PyFunceble.Style.BRIGHT
                            + PyFunceble.Fore.GREEN
                            + "Please take the time to update PyFunceble!\n"
                            + PyFunceble.Style.RESET_ALL
                        )  # pylint:disable=line-too-long

                        # We print the message on screen.
                        print(message)

                        # We exit PyFunceble with the code 1.
                        PyFunceble.sys.exit(1)
                elif checked or checked is not False and not checked:
                    # The quiet mode is activated and the current version
                    # is less or equal to the minimal version.

                    # We raise an exception telling the user to update their
                    # instance of PyFunceble.
                    raise PyFunceble.exceptions.PleaseUpdatePyFunceble(
                        "A critical issue has been fixed. Please take the time to update PyFunceble!"  # pylint:disable=line-too-long
                    )

    @classmethod
    def __check_deprecated(cls, upstream_version):  # pragma: no cover
        """
        Checks if the local version is deprecated.
        """

        for version in reversed(upstream_version["deprecated"]):
            # We loop through the list of deprecated versions.

            # We compare the local with the currently read deprecated version.
            checked = PyFunceble.abstracts.Version.compare(version)

            if (
                not PyFunceble.CONFIGURATION.quiet
                and checked
                or checked is not False
                and not checked
            ):
                # The quiet mode is not activated and the local version is
                # less or equal to the currently read deprecated version.

                # We initiate the message we are going to return to the user.
                message = (
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.RED
                    + "Your current version is considered as deprecated.\n"
                    + PyFunceble.Style.RESET_ALL
                )  # pylint:disable=line-too-long
                message += (
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.GREEN
                    + "Please take the time to update PyFunceble!\n"
                    + PyFunceble.Style.RESET_ALL
                )  # pylint:disable=line-too-long

                # We print the message.
                print(message)

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return False

            # The quiet mode is activated.

            if checked or checked is not False and not checked:
                # The local version is  less or equal to the currently
                # read deprecated version.
                print("Version deprecated.")

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return False
        return True

    @classmethod
    def __print_messages(cls, upstream_version):  # pragma: no cover
        """
        Look at the messages and print the one that needs to be
        printed.
        """

        if (
            "messages" in upstream_version
            and not PyFunceble.CONFIGURATION.simple
            and not PyFunceble.CONFIGURATION.quiet
        ):
            messages = upstream_version["messages"]

            for minimal_version, data in messages.items():
                comparison = PyFunceble.abstracts.Version.compare(minimal_version)

                for single_message in data:
                    if "until" in single_message:
                        until_comparison = (
                            PyFunceble.abstracts.Version.compare(
                                single_message["until"]
                            ),
                        )
                    else:
                        until_comparison = True

                    if "type" in single_message:
                        if single_message["type"] == "info":
                            coloration = (
                                PyFunceble.Fore.YELLOW + PyFunceble.Style.BRIGHT
                            )
                        elif single_message["type"] == "warning":
                            coloration = (
                                PyFunceble.Fore.MAGENTA + PyFunceble.Style.BRIGHT
                            )
                        else:
                            coloration = PyFunceble.Fore.BLUE + PyFunceble.Style.BRIGHT
                    else:
                        coloration = PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT

                    if (
                        comparison is False or comparison is None
                    ) and until_comparison is True:

                        print(f"{coloration}{single_message['message']}")

    @classmethod
    def compare_version_and_print_messages(cls):  # pragma: no cover
        """
        Compares the local with the upstream version.
        """

        upstream_version = cls.get_upstream_version_file()

        cls.__check_force_update(upstream_version)

        if cls.__check_deprecated(upstream_version):
            # We compare the local version with the upstream version.
            status = PyFunceble.abstracts.Version.compare(
                upstream_version["current_version"]
            )

            if status is not None and not status and not PyFunceble.CONFIGURATION.quiet:
                # The quiet mode is not activate and the current version is greater than
                # the upstream version.

                # We initiate the message we are going to return to the user.
                message = (
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.CYAN
                    + "Your version is more recent!\nYou should really think about sharing your changes with the community!\n"  # pylint:disable=line-too-long
                    + PyFunceble.Style.RESET_ALL
                )
                message += (
                    PyFunceble.Style.BRIGHT
                    + "Your version: "
                    + PyFunceble.Style.RESET_ALL
                    + PyFunceble.VERSION
                    + "\n"
                )
                message += (
                    PyFunceble.Style.BRIGHT
                    + "Upstream version: "
                    + PyFunceble.Style.RESET_ALL
                    + upstream_version["current_version"]
                    + "\n"
                )

                # We print the message.
                print(message)
            elif status:
                # The current version is less that the upstream version.

                if not PyFunceble.CONFIGURATION.quiet:
                    # The quiet mode is not activated.

                    # We initiate the message we are going to return to the user.
                    message = (
                        PyFunceble.Style.BRIGHT
                        + PyFunceble.Fore.YELLOW
                        + "Please take the time to update PyFunceble!\n"
                        + PyFunceble.Style.RESET_ALL
                    )  # pylint:disable=line-too-long
                    message += (
                        PyFunceble.Style.BRIGHT
                        + "Your version: "
                        + PyFunceble.Style.RESET_ALL
                        + PyFunceble.VERSION
                        + "\n"
                    )  # pylint:disable=line-too-long
                    message += (
                        PyFunceble.Style.BRIGHT
                        + "Upstream version: "
                        + PyFunceble.Style.RESET_ALL
                        + upstream_version[  # pylint:disable=line-too-long
                            "current_version"
                        ]
                        + "\n"
                    )

                    # We print the message.
                    print(message)
                else:
                    # The quiet mode is activated.

                    # We print the message.
                    print("New version available.")

        cls.__print_messages(upstream_version)
