"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the API core interface.

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

import PyFunceble

from .cli import CLICore


class APICore:
    """
    Provides the logic and interface for the tests from the API.

    :param str subject: The element we are testing.
    :param bool complete:
        Activate the return of a dictionnary with significant - if not all -
        data about the test.

    :param dict configuration:
        The custom configuration to load.

        .. note::
            This will let you overwrite any of the previously given
            configuration index.
    """

    # The subject we are working with.
    subject = None
    # Tell us if we have to return all possible data.
    complete = False
    # Saves the configuration.
    configuration = None

    def __init__(
        self,
        subject,
        complete=False,
        configuration=None,
        db_file_name="api_call",
        is_parent=True,
    ):
        # We share the subject.
        self.subject = subject

        # We share the complete option.
        self.complete = complete

        # We share the given configuration.
        self.configuration = configuration

        # We share the db file name.
        self.db_file_name = db_file_name

        # We load the global configuration
        # if it was not alreay done.
        PyFunceble.load_config(
            generate_directory_structure=False, custom=self.configuration
        )

        if (
            "api_config_loaded" not in PyFunceble.INTERN
            or self.configuration != PyFunceble.INTERN["api_config_loaded"]
        ):
            # We update the configuration with the given
            # configuration.
            preset = PyFunceble.cconfig.Preset()
            preset.init_all()
            preset.api()

            PyFunceble.INTERN["api_config_loaded"] = (
                self.configuration.copy()
                if isinstance(self.configuration, dict)
                else dict()
            )

        # We create an instance of the whois database.
        self.whois_db = PyFunceble.database.Whois(parent_process=is_parent)

        # We create an instance of the inactive database.
        self.inactive_db = PyFunceble.database.Inactive(
            db_file_name, parent_process=is_parent
        )

    def __inactive_database_management(self, subject, status):
        """
        Given the subject and status, we add or remove the subject
        from the inactive database.
        """

        if self.inactive_db.authorized:
            # We are authorized to operate with the
            # inactive database.s

            if status.lower() in PyFunceble.STATUS.list.up:
                # The status is in the list of UP status.

                # We remove it from the database.
                self.inactive_db.remove(subject)
            else:
                # The status is not in the list of UP status.

                # We add it into the database.
                self.inactive_db.add(subject, status)

    def reputation(self, subject_type):
        """
        Make a reputation check.

        :param str subject_type:
            Should be one of the following.

            - :code:`domain`

            - :code:`url`
        """

        if isinstance(self.subject, list):
            # The given subject is a list of subjects.

            # We initiate a variable which save our result.
            result = {}

            for subject in self.subject:
                # We loop through the list of subject.

                result[subject] = APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).reputation(subject_type)

            # We return our local result.
            return result

        if "url" in subject_type:
            data = PyFunceble.status.UrlReputation(
                self.subject, whois_db=self.whois_db, inactive_db=self.inactive_db
            ).get()
        else:
            data = PyFunceble.status.DomainAndIPReputation(
                self.subject, whois_db=self.whois_db, inactive_db=self.inactive_db
            ).get()

        self.__inactive_database_management(self.subject, data["status"])
        CLICore.save_into_database(data, self.db_file_name)

        if self.complete:
            # The user want a copy of the compelte data.

            # We return them
            return data

        # We only return the status.
        return data["status"]

    def availability(self, subject_type):
        """
        Make an availability check.

        :param str subject_type:
            Should be one of the following.

            - :code:`domain`

            - :code:`url`
        """

        if "url" in subject_type:
            return self.url()
        return self.domain_and_ip()

    def syntax(self, subject_type):
        """
        Make a syntax check.

        :param str subject_type:
            Should be one of the following.

            - :code:`domain`

            - :code:`url`
        """

        if isinstance(self.subject, list):
            # The given subject is a list of subjects.

            # We initiate a variable which save our result.
            result = {}

            for subject in self.subject:
                # We loop through the list of subject.

                result[subject] = APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).syntax(subject_type)

            # We return our local result.
            return result

        if "url" in subject_type:
            data = PyFunceble.status.UrlSyntax(
                self.subject, whois_db=self.whois_db, inactive_db=self.inactive_db
            ).get()
        else:
            data = PyFunceble.status.DomainAndIpSyntax(
                self.subject, whois_db=self.whois_db, inactive_db=self.inactive_db
            ).get()

        self.__inactive_database_management(self.subject, data["status"])
        CLICore.save_into_database(data, self.db_file_name)

        if self.complete:
            # The user want a copy of the compelte data.

            # We return them
            return data

        # We only return the status.
        return data["status"]

    def domain_and_ip(self):
        """
        Run a domain/IP availability check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subject is a list of subjects.

            # We initiate a variable which save our result.
            result = {}

            for subject in self.subject:
                # We loop through the list of subject.

                result[subject] = APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).domain_and_ip()

            # We return our local result.
            return result

        # We get the status of the given subject.
        data = PyFunceble.status.DomainAndIpAvailability(
            self.subject, whois_db=self.whois_db, inactive_db=self.inactive_db
        ).get()

        self.__inactive_database_management(self.subject, data["status"])
        CLICore.save_into_database(data, self.db_file_name)

        if self.complete:
            # The user want a copy of the compelte data.

            # We return them
            return data

        # We only return the status.
        return data["status"]

    def domain_syntax(self):
        """
        Run a domain syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subject is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).domain_syntax()
                for subject in self.subject
            }

        # We return the validity of the the given subject.
        return PyFunceble.Check(self.subject).is_domain()

    def subdomain_syntax(self):
        """
        Run a subdomain syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).subdomain_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_subdomain()

    def ipv4_syntax(self):
        """
        Run an IPv4 syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).ipv4_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_ipv4()

    def ipv6_syntax(self):
        """
        Run an IPv6 syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subject is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).ipv6_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_ipv6()

    def ip_syntax(self):
        """
        Run an IP syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subject is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).ip_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_ip()

    def ipv4_range_syntax(self):
        """
        Run an IPv4 range syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).ipv4_range_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_ipv4_range()

    def ipv6_range_syntax(self):
        """
        Run an IPv6 range syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).ipv6_range_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_ipv6_range()

    def ip_range_syntax(self):
        """
        Run an IP range syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).ip_range_syntax()
                for subject in self.subject
            }

        # We return the validity of the given subject.
        return PyFunceble.Check(self.subject).is_ip_range()

    def url(self):
        """
        Run an URL availability check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We initiate a local variable which will save
            # what we are going to return.
            result = {}

            for subject in self.subject:
                # We loop through the list of subjects.

                result[subject] = APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).url()

            # We return the result of each subjects.
            return result

        # We get the complete data about the status of the subject.
        data = PyFunceble.status.UrlAvailability(
            self.subject, whois_db=self.whois_db, inactive_db=self.inactive_db
        ).get()

        self.__inactive_database_management(self.subject, data["status"])
        CLICore.save_into_database(data, self.db_file_name)

        if self.complete:
            # The user want a complete copy of the data.

            # We return them.
            return data

        # We return the result of each subjects.
        return data["status"]

    def url_syntax(self):
        """
        Run an IPv4 syntax check over the given subject.
        """

        if isinstance(self.subject, list):
            # The given subjet is a list of subject.

            # We return the validity of each subjects.
            return {
                subject: APICore(
                    subject, complete=self.complete, configuration=self.configuration
                ).url_syntax()
                for subject in self.subject
            }

        # We return the validity of the subject.
        return PyFunceble.Check(self.subject).is_url()
