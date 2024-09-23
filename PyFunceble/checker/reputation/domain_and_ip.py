"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the domains and IP reputation checker.

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

from PyFunceble.checker.reputation.base import ReputationCheckerBase
from PyFunceble.checker.reputation.domain import DomainReputationChecker
from PyFunceble.checker.reputation.ip import IPReputationChecker


class DomainAndIPReputationChecker(ReputationCheckerBase):
    """
    Provides the interface for checking the reputation of an IP or domain.

    :param str subject:
        Optional, The subject to work with.
    :param bool do_syntax_check_first:
        Optional, Activates/Disables the check of the status before the actual
        status gathering.
    """

    @ReputationCheckerBase.ensure_subject_is_given
    @ReputationCheckerBase.update_status_date_after_query
    def query_status(self) -> "DomainAndIPReputationChecker":
        """
        Queries the result without anything more.
        """

        if self.status.ip_syntax:
            query_object = IPReputationChecker(
                self.subject,
                do_syntax_check_first=self.do_syntax_check_first,
                db_session=self.db_session,
                use_platform=self.use_platform,
            )
        else:
            query_object = DomainReputationChecker(
                self.subject,
                do_syntax_check_first=self.do_syntax_check_first,
                db_session=self.db_session,
                use_platform=self.use_platform,
            )

        query_object.ipv4_reputation_query_tool = self.ipv4_reputation_query_tool
        query_object.platform_query_tool = self.platform_query_tool
        query_object.dns_query_tool = self.dns_query_tool

        result = query_object.query_status()

        self.__dict__.update(query_object.__dict__)

        return result
