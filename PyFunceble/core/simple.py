"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the simple core interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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

        if PyFunceble.CONFIGURATION.generate_complements:
            self.subject = PyFunceble.get_complements(self.subject, include_given=True)
        else:
            self.subject = self.subject

    def __save_in_database(self, dataset):
        """
        Saves the given dataset (result) into the database.

        :param dataset: The dataset to save.
        :type dataset: dict, list
        """

        if isinstance(dataset, list):
            for data in dataset:
                self.__save_in_database(data)
        else:
            self.save_into_database(dataset, None, self.mysql_db)

    def test(self, subject, subject_type):  # pylint: disable=too-many-return-statements
        """
        Processes a test of the given subject and return the result.
        """

        if isinstance(subject, list):
            return [self.test(x, subject_type) for x in subject]

        if isinstance(PyFunceble.CONFIGURATION.cooldown_time, (float, int)):
            PyFunceble.sleep(PyFunceble.CONFIGURATION.cooldown_time)

        if PyFunceble.CONFIGURATION.syntax:
            if subject_type in ["url"]:
                return PyFunceble.status.UrlSyntax(subject, whois_db=self.whois_db)

            return PyFunceble.status.DomainAndIpSyntax(
                subject, whois_db=self.whois_db
            ).get()

        if PyFunceble.CONFIGURATION.reputation:
            if subject_type in ["url"]:
                return PyFunceble.status.UrlReputation(subject, whois_db=self.whois_db)

            return PyFunceble.status.DomainAndIPReputation(
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
        Handles the simple domain testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_domain()
        # We print the header if it was not done yet.
        self.print_header()

        if self.subject:
            self.__save_in_database(self.test(self.subject, "domain"))
        else:
            self.print_nothing_to_test()

    def url(self):
        """
        Handles the simple URL testing.
        """

        # We run the preset specific to this method.
        self.preset.simple_url()
        # We print the header if it was not done yet.
        self.print_header()

        if self.subject:
            self.__save_in_database(self.test(self.subject, "url"))
        else:
            self.print_nothing_to_test()
