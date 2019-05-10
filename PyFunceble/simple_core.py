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

Provide the logic for a simple test from the CLI.

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
# pylint:enable=line-too-long

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble.file_core import FileCore
from PyFunceble.status import Status, SyntaxStatus, URLStatus
from PyFunceble.whois_db import WhoisDB


class SimpleCore:
    """
    Brain of PyFunceble for simple test.

    :param str subject: The subject we are testing.
    """

    def __init__(self, subject):
        self.preset = PyFunceble.Preset()

        if PyFunceble.CONFIGURATION["idna_conversion"]:
            self.subject = domain2idna(subject)
        else:
            self.subject = subject

        self.whois_db = WhoisDB()

    def domain(self):
        """
        Handle the simple domain testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_domain()
        # We print the header if it was not done yet.
        PyFunceble.CLICore.print_header()

        if self.subject:
            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(self.subject).get()["status"]
            else:
                # We test and get the status of the domain.
                status = Status(self.subject, whois_db=self.whois_db).get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(
                    "{0} {1}".format(
                        FileCore.get_simple_coloration(status) + self.subject, status
                    )
                )
        else:
            PyFunceble.CLICore.print_nothing_to_test()

    def url(self):
        """
        Handle the simple URL testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_url()
        # We print the header if it was not done yet.
        PyFunceble.CLICore.print_header()

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
                print(
                    "{0} {1}".format(
                        FileCore.get_simple_coloration(status) + self.subject, status
                    )
                )
        else:
            PyFunceble.CLICore.print_nothing_to_test()
