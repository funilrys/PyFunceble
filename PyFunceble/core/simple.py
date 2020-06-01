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
            self.save_into_database(dataset, None)

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
                subject.lower(), whois_db=self.whois_db
            ).get()

        if PyFunceble.CONFIGURATION.reputation:
            if subject_type in ["url"]:
                return PyFunceble.status.UrlReputation(subject, whois_db=self.whois_db)

            return PyFunceble.status.DomainAndIPReputation(
                subject.lower(), whois_db=self.whois_db
            ).get()

        if subject_type in ["url"]:
            return PyFunceble.status.UrlAvailability(
                subject, whois_db=self.whois_db
            ).get()

        return PyFunceble.status.DomainAndIpAvailability(
            subject.lower(), whois_db=self.whois_db
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
