#!/usr/bin/env python3

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

This module is half of the brain of PyFunceble.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://funilrys.github.io/PyFunceble/

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
# pylint:disable=bad-continuation

from random import choice

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble.check import Check
from PyFunceble.database import Inactive
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.execution_time import ExecutionTime
from PyFunceble.generate import Generate
from PyFunceble.helpers import Download, Regex
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints
from PyFunceble.status import Status, SyntaxStatus, URLStatus


class Preset:
    """
    Check or update the global configuration based on some events.
    """

    def __init__(self):
        if PyFunceble.CONFIGURATION["syntax"]:
            # We are checking for syntax.

            # We deactivate the http status code.
            PyFunceble.HTTP_CODE["active"] = False

    @classmethod
    def switch(
        cls, variable, custom=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Switch PyFunceble.CONFIGURATION variables to their opposite.

        :param variable:
            The variable name to switch.
            The variable should be an index our configuration system.
            If we want to switch a bool variable, we should parse
            it here.
        :type variable: str|bool

        :param custom:
            Let us know if have to switch the parsed variable instead
            of our configuration index.
        :type custom: bool

        :return:
            The opposite of the configuration index or the given variable.
        :rtype: bool

        :raises:
            :code:`Exception`
                When the configuration is not valid. In other words,
                if the PyFunceble.CONFIGURATION[variable_name] is not a bool.
        """

        if not custom:
            # We are not working with custom variable which is not into
            # the configuration.

            # We get the current state.
            current_state = dict.get(PyFunceble.CONFIGURATION, variable)
        else:
            # We are working with a custom variable which is not into the
            # configuration
            current_state = variable

        if isinstance(current_state, bool):
            # The current state is a boolean.

            if current_state:
                # The current state is equal to True.

                # We return False.
                return False

            # The current state is equal to False.

            # We return True.
            return True

        # The current state is not a boolean.

        # We set the message to raise.
        to_print = "Impossible to switch %s. Please post an issue to %s"

        # We raise an exception inviting the user to report an issue.
        raise Exception(
            to_print % (repr(variable), PyFunceble.LINKS["repo"] + "/issues.")
        )

    @classmethod
    def disable(cls, index):
        """
        Set the given configuration index to :code:`False`.
        """

        if PyFunceble.CONFIGURATION[index]:
            PyFunceble.CONFIGURATION[index] = False

    @classmethod
    def enable(cls, index):
        """
        Set the given configuration index to :code:`True`.
        """

        if not PyFunceble.CONFIGURATION[index]:
            PyFunceble.CONFIGURATION[index] = True

    def simple_domain(self):
        """
        Prepare the global configuration for a domain
        test.
        """

        should_be_disabled = ["show_percentage", "whois_database"]

        for index in should_be_disabled:
            self.disable(index)

    def simple_url(self):
        """
        Prepare the global configuration for an URL test.
        """

        should_be_disabled = ["show_percentage", "whois_database"]

        for index in should_be_disabled:
            self.enable(index)

    def file_url(self):
        """
        Prepare the global configuration for a list of URL to test.
        """

        should_be_disabled = ["generate_hosts"]
        should_be_enabled = ["no_whois", "plain_list_domain", "split"]

        for index in should_be_disabled:
            self.disable(index)

        for index in should_be_enabled:
            self.enable(index)


class CLICore:
    """
    Provide some methods which are dedicated for the CLI.
    """

    @classmethod
    def colorify_logo(cls, home=False):
        """
        Print the colored logo based on global results.

        :param home: Tell us if we have to print the initial coloration.
        :type home: bool
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
    def print_header(cls):
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
    def stay_safe(cls):
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


class Dispatcher:  # pylint: disable=too-few-public-methods, too-many-arguments
    """
    Dispatch to the right brain side.
    """

    def __init__(
        self,
        domain_or_ip=None,
        file_path=None,
        url_to_test=None,
        url_file_path=None,
        link_to_test=None,
    ):
        ExecutionTime("start")

        if domain_or_ip:
            SimpleCore(domain_or_ip).domain()
        elif url_to_test:
            SimpleCore(url_to_test).url()
        elif file_path:
            FileCore(file_path, "domain").read_and_test_file_content()

        Percentage().log()

        ExecutionTime("stop")

        CLICore.stay_safe()


class SimpleCore:
    """
    Brain of PyFunceble for simple test.

    :param subject: The subject we are testing.
    :type subject: str
    """

    def __init__(self, subject):
        self.preset = Preset()
        if PyFunceble.CONFIGURATION["idna_conversion"]:
            self.subject = domain2idna(subject)
        else:
            self.subject = subject

    def domain(self):
        """
        Handle the simple domain testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_domain()
        # We print the header if it was not done yet.
        CLICore.print_header()

        if self.subject:
            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(self.subject).get()["status"]
            else:
                # We test and get the status of the domain.
                status = Status(self.subject).get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(self.subject, status)

        else:
            CLICore.print_nothing_to_test()

    def url(self):
        """
        Handle the simple URL testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_url()
        # We print the header if it was not done yet.
        CLICore.print_header()

        if self.subject:
            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(self.subject, subject_type="url").get()["status"]
            else:
                # We test and get the status of the domain.
                status = URLStatus(self.subject, subject_type="url").get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(self.subject, status)
        else:
            CLICore.print_nothing_to_test()


class FileCore:
    """
    Brain of PyFunceble for file testing.

    :param file: The file we are testing.
    :type file: str

    :param file_type:
        The file type.
        Should be one of the following.

            - :code:`domain`

            - :code:`url`
    :type file_type: str
    """

    # We set a regex of element to delete.
    # Understand with this variable that we don't want to test those.
    regex_ignore = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$|ip6-mcastprefix$|ip6-localhost$|ip6-loopback$|ip6-allnodes$|ip6-allrouters$|ip6-localnet$"  # pylint: disable=line-too-long

    def __init__(self, file, file_type="domain"):
        self.preset = Preset()
        self.file = file
        self.file_type = file_type

        self.list_of_up_statuses = PyFunceble.STATUS["list"]["up"]
        self.list_of_up_statuses.extend(PyFunceble.STATUS["list"]["valid"])

        self.inactive_db = Inactive(self.file)
        self.inactive_db.initiate()

        self.download_link()

        # We generate the directory structure.
        DirectoryStructure()

    def download_link(self):
        """
        Download the file if it is an URL.
        """

        if self.file and Check(self.file).is_url_valid():
            destination = self.file.split("/")[-1]

            if (
                not PyFunceble.path.isfile(destination)
                or PyFunceble.INTERN["counter"]["number"]["tested"] == 0
            ):
                # The filename does not exist in the current directory
                # or the currently number of tested is equal to 0.

                # We download the content of the link.
                Download(self.file, destination).text()

            self.file = destination

    def domain(self, subject):
        """
        Handle the test of a single domain.

        :param subject: The subject we are testing.
        :type subject: str
        """

        if subject:
            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(
                    subject, subject_type="file_domain", filename=self.file
                ).get()["status"]
            else:
                # We test and get the status of the domain.
                status = Status(
                    subject, subject_type="file_domain", filename=self.file
                ).get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(subject, status)

            if status.lower() in self.list_of_up_statuses:

                if self.inactive_db.is_present(subject):
                    Generate(
                        subject, "file_domain", PyFunceble.STATUS["official"]["up"]
                    ).analytic_file("suspicious")

                    self.inactive_db.remove(subject)
            else:
                self.inactive_db.add(subject)

    def url(self, subject):
        """
        Handle the simple URL testing.

        :param subject: The subject we are testing.
        :type subject: str
        """

        if subject:
            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(
                    subject, subject_type="file_url", filename=self.file
                ).get()["status"]
            else:
                # We test and get the status of the domain.
                status = URLStatus(
                    subject, subject_type="file_url", filename=self.file
                ).get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(subject, status)

    @classmethod
    def _format_line(cls, line):
        """
        Format the extracted line before passing it to the system.

        :param line: The extracted line.
        :type line: str

        :return: The formatted line with only the element to test.
        :rtype: str

        .. note:
            Understand by formating the fact that we get rid
            of all the noises around the element we want to test.
        """

        if not line.startswith("#"):
            # The line is not a commented line.

            if "#" in line:
                # There is a comment at the end of the line.

                # We delete the comment from the line.
                line = line[: line.find("#")].strip()

            if " " in line or "\t" in line:
                # A space or a tabs is in the line.

                # We remove all whitestring from the extracted line.
                splited_line = line.split()

                # As there was a space or a tab in the string, we consider
                # that we are working with the hosts file format which means
                # that the domain we have to test is after the first string.
                # So we set the index to 1.
                index = 1

                while index < len(splited_line):
                    # We loop until the index is greater than the length of
                    #  the splited line.

                    if splited_line[index]:
                        # The element at the current index is not an empty string.

                        # We break the loop.
                        break

                    # The element at the current index is an empty string.

                    # We increase the index number.
                    index += 1

                # We return the last read element.
                return splited_line[index]

            # We return the extracted line.
            return line

        # The extracted line is a comment line.

        # We return an empty string as we do not want to work with commented line.
        return ""

    def read_and_test_file_content(self):
        """
        Read a file block by block and test its content.
        """

        CLICore.print_header()

        with open(self.file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n").strip()

                if (
                    line[0] != "#"
                    and not Regex(
                        line, self.regex_ignore, escape=False, return_data=False
                    ).match()
                    and not self.inactive_db.is_present(line)
                ):
                    if self.file_type == "domain":
                        self.domain(self._format_line(line))
                    elif self.file_type == "url":
                        self.url(self._format_line(line))
                    else:
                        raise Exception("Unknown file type.")


