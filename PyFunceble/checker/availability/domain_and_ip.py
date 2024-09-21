"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the domains and IP availability checker.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from typing import Union

from PyFunceble.checker.availability.base import AvailabilityCheckerBase
from PyFunceble.checker.availability.domain import DomainAvailabilityChecker
from PyFunceble.checker.availability.ip import IPAvailabilityChecker


class DomainAndIPAvailabilityChecker(AvailabilityCheckerBase):
    """
    Provides the interface for checking the availability of a IP or domain.

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

    @AvailabilityCheckerBase.ensure_subject_is_given
    @AvailabilityCheckerBase.update_status_date_after_query
    def query_status(
        self,
    ) -> "DomainAndIPAvailabilityChecker":  # pragma: no cover ## Just a switch.
        """
        Queries the result without anything more.
        """

        query_object: Union[IPAvailabilityChecker, DomainAvailabilityChecker] = None

        if self.status.ip_syntax:
            query_object = IPAvailabilityChecker(
                self.subject,
                use_extra_rules=self.use_extra_rules,
                use_whois_lookup=self.use_whois_lookup,
                use_dns_lookup=self.use_dns_lookup,
                use_netinfo_lookup=self.use_netinfo_lookup,
                use_http_code_lookup=self.use_http_code_lookup,
                use_reputation_lookup=self.use_reputation_lookup,
                do_syntax_check_first=self.do_syntax_check_first,
                db_session=self.db_session,
                use_whois_db=self.use_whois_db,
                use_platform=self.use_platform,
            )
        else:
            query_object = DomainAvailabilityChecker(
                self.subject,
                use_extra_rules=self.use_extra_rules,
                use_whois_lookup=self.use_whois_lookup,
                use_dns_lookup=self.use_dns_lookup,
                use_netinfo_lookup=self.use_netinfo_lookup,
                use_http_code_lookup=self.use_http_code_lookup,
                use_reputation_lookup=self.use_reputation_lookup,
                do_syntax_check_first=self.do_syntax_check_first,
                db_session=self.db_session,
                use_whois_db=self.use_whois_db,
                use_platform=self.use_platform,
            )

        query_object.dns_query_tool = self.dns_query_tool
        query_object.whois_query_tool = self.whois_query_tool
        query_object.platform_query_tool = self.platform_query_tool
        query_object.hostbyaddr_query_tool = self.hostbyaddr_query_tool
        query_object.addressinfo_query_tool = self.addressinfo_query_tool
        query_object.http_status_code_query_tool = self.http_status_code_query_tool

        result = query_object.query_status()

        self.__dict__.update(query_object.__dict__)

        return result

    @staticmethod
    def is_valid() -> bool:  # pylint: disable=arguments-differ
        raise NotImplementedError()
