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


import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.base import AvailabilityCheckerBase
from PyFunceble.checker.reputation.url import URLReputationChecker


class URLAvailabilityChecker(AvailabilityCheckerBase):
    """
    Provides the interface for checking the availability of a given URL.
    """

    def try_to_query_status_from_http_status_code(self) -> "URLAvailabilityChecker":
        """
        Tries to query the status from the network information.
        """

        lookup_result = self.http_status_code_query_tool.get_status_code()

        if (
            lookup_result
            and lookup_result != self.http_status_code_query_tool.STD_UNKWON_STATUS_CODE
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
        else:
            self.status.http_status_code = None

        return self

    def try_to_query_status_from_reputation(self) -> "URLAvailabilityChecker":
        """
        Tries to query the status from the reputation lookup.
        """

        lookup_result = URLReputationChecker(self.status.idna_subject).get_status()

        if lookup_result and lookup_result.is_malicious():
            self.status.status = PyFunceble.storage.STATUS.up
            self.status.status_source = "REPUTATION"

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

        if (
            self.should_we_continue_test(status_post_syntax_checker)
            and self.use_reputation_lookup
        ):
            self.try_to_query_status_from_reputation()

        if self.should_we_continue_test(status_post_syntax_checker):
            self.try_to_query_status_from_http_status_code()

        if not self.status.status:
            self.status.status = PyFunceble.storage.STATUS.down
            self.status.status_source = "STDLOOKUP"

        return self

    @staticmethod
    def is_valid() -> bool:
        raise NotImplementedError()
