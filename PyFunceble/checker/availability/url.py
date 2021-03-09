"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the URL availability checker.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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


import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.base import AvailabilityCheckerBase
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.checker.reputation.url import URLReputationChecker


class URLAvailabilityChecker(AvailabilityCheckerBase):
    """
    Provides the interface for checking the availability of a given URL.

    :param str subject:
        Optional, The subject to work with.
    :param bool use_extra_rules:
        Optional, Activates/Disables the usage of our own set of extra rules.
    :param bool use_whois_lookup:
        Optional, Activates/Disables the usage of the WHOIS lookup to gather
        the status of the given :code:`subject`.
    :param bool use_dns_lookup:
        Optional, Activates/Disables the usage of the DNS lookup to gather the
        status of the given :code:`subject`.
    :param bool use_netinfo_lookup:
        Optional, Activates/Disables the usage of the network information
        lookup module to gather the status of the given :code:`subject`.
    :param bool use_http_code_lookup:
        Optional, Activates/Disables the usage of the HTTP status code lookup
        to gather the status of the given :code:`subject`.
    :param bool use_reputation_lookup:
        Optional, Activates/Disables the usage of the reputation dataset
        lookup to gather the status of the given :code:`subject`.
    :param bool do_syntax_check_first:
        Optional, Activates/Disables the check of the status before the actual
        status gathering.
    :param bool use_whois_db:
        Optional, Activates/Disable the usage of a local database to store the
        WHOIS datasets.
    """

    def subject_propagator(self) -> "URLAvailabilityChecker":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.
        """

        self.http_status_code_query_tool.set_subject(self.idna_subject)

        self.domain_syntax_checker.subject = self.idna_subject
        self.ip_syntax_checker.subject = self.idna_subject
        self.url_syntax_checker.subject = self.idna_subject

        self.status = AvailabilityCheckerStatus()
        self.status.params = self.params
        self.status.dns_lookup_record = None
        self.status.whois_lookup_record = None

        self.status.subject = self.subject
        self.status.idna_subject = self.idna_subject
        self.status.status = None

        self.query_syntax_checker()

        return self

    def try_to_query_status_from_http_status_code(self) -> "URLAvailabilityChecker":
        """
        Tries to query the status from the network information.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: HTTP Status code Lookup",
            self.status.idna_subject,
        )

        lookup_result = self.http_status_code_query_tool.get_status_code()

        if (
            lookup_result
            and lookup_result
            != self.http_status_code_query_tool.STD_UNKNOWN_STATUS_CODE
        ):
            self.status.http_status_code = lookup_result

            if PyFunceble.facility.ConfigLoader.is_already_loaded():
                dataset = PyFunceble.storage.HTTP_CODES
            else:
                dataset = PyFunceble.storage.STD_HTTP_CODES

            if (
                self.status.http_status_code in dataset.list.up
                or self.status.http_status_code in dataset.list.potentially_up
            ):
                self.status.status = PyFunceble.storage.STATUS.up
                self.status.status_source = "HTTP CODE"

                PyFunceble.facility.Logger.info(
                    "Could define the status of %r from: HTTP Status code Lookup",
                    self.status.idna_subject,
                )
        else:
            self.status.http_status_code = None

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: HTTP Status code Lookup",
            self.status.idna_subject,
        )

        return self

    def try_to_query_status_from_reputation(self) -> "URLAvailabilityChecker":
        """
        Tries to query the status from the reputation lookup.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: Reputation Lookup",
            self.status.idna_subject,
        )

        lookup_result = URLReputationChecker(self.status.idna_subject).get_status()

        # pylint: disable=no-member
        if lookup_result and lookup_result.is_malicious():
            self.status.status = PyFunceble.storage.STATUS.up
            self.status.status_source = "REPUTATION"

            PyFunceble.facility.Logger.info(
                "Could define the status of %r from: Reputation Lookup",
                self.status.idna_subject,
            )

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: Reputation Lookup",
            self.status.idna_subject,
        )

        return self

    @AvailabilityCheckerBase.ensure_subject_is_given
    @AvailabilityCheckerBase.update_status_date_after_query
    def query_status(self) -> "URLAvailabilityChecker":
        """
        Queries the result without anything more.
        """

        status_post_syntax_checker = None

        if not self.status.status and self.do_syntax_check_first:
            self.try_to_query_status_from_syntax_lookup()

            if self.status.status:
                status_post_syntax_checker = self.status.status

        if self.use_reputation_lookup and self.should_we_continue_test(
            status_post_syntax_checker
        ):
            self.try_to_query_status_from_reputation()

        if self.should_we_continue_test(status_post_syntax_checker):
            self.try_to_query_status_from_http_status_code()

        if not self.status.status:
            self.status.status = PyFunceble.storage.STATUS.down
            self.status.status_source = "STDLOOKUP"

            PyFunceble.facility.Logger.info(
                "Could not define status the status of %r. Setting to %r",
                self.status.idna_subject,
                self.status.status,
            )

        return self

    @staticmethod
    def is_valid() -> bool:
        raise NotImplementedError()
