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

from .cli import CLICore


class SimpleCore(CLICore):
    """
    Brain of PyFunceble for simple test.

    :param str subject: The subject we are testing.
    """

    def __init__(self, subject):
        super().__init__()

        if PyFunceble.CONFIGURATION.idna_conversion:
            self.subject = domain2idna(subject)
        else:
            self.subject = subject

    def test(self, subject, subject_type):
        """
        Process a test of the given subject and return the result.
        """

        if isinstance(subject, list):
            return [self.test(x, subject_type) for x in subject]

        if PyFunceble.CONFIGURATION.syntax:
            return PyFunceble.status.DomainAndIpSyntax(
                subject, whois_db=self.whois_db
            ).get()

        if subject_type in ["url"]:
            return PyFunceble.status.UrlAvailability(
                subject, whois_db=self.whois_db
            ).get()

        return PyFunceble.status.DomainAndIpAvailability(
            subject, whois_db=self.whois_db
        ).get()

    def domain(self):
        """
        Handle the simple domain testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_domain()
        # We print the header if it was not done yet.
        self.print_header()

        if self.subject:
            data = self.test(self.subject, "domain")

            self.save_into_database(data, None, self.mysql_db)
        else:
            self.print_nothing_to_test()

    def url(self):
        """
        Handle the simple URL testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_url()
        # We print the header if it was not done yet.
        self.print_header()

        if self.subject:
            data = self.test(self.subject, "url")

            self.save_into_database(data, None, self.mysql_db)
        else:
            self.print_nothing_to_test()
