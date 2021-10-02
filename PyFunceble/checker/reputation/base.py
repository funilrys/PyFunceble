"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all reputation checker classes.

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


from typing import List, Optional

from sqlalchemy.orm import Session

import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.reputation.params import ReputationCheckerParams
from PyFunceble.checker.reputation.status import ReputationCheckerStatus
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.dataset.ipv4_reputation import IPV4ReputationDataset
from PyFunceble.query.dns.query_tool import DNSQueryTool


class ReputationCheckerBase(CheckerBase):
    """
    Provides the base of all our reputation checker classes.

    :param str subject:
        Optional, The subject to work with.
    :param bool do_syntax_check_first:
        Optional, Activates/Disables the check of the status before the actual
        status gathering.
    """

    dns_query_tool: Optional[DNSQueryTool] = None
    ipv4_reputation_query_tool: Optional[IPV4ReputationDataset] = None
    domain_syntax_checker: Optional[DomainSyntaxChecker] = None
    ip_syntax_checker: Optional[IPSyntaxChecker] = None
    url_syntax_checker: Optional[URLSyntaxChecker] = None

    status: Optional[ReputationCheckerStatus] = None
    params: Optional[ReputationCheckerParams] = None

    def __init__(
        self,
        subject: Optional[str] = None,
        do_syntax_check_first: Optional[bool] = None,
        db_session: Optional[Session] = None,
    ) -> None:
        self.dns_query_tool = DNSQueryTool().guess_all_settings()
        self.ipv4_reputation_query_tool = IPV4ReputationDataset()
        self.domain_syntax_checker = DomainSyntaxChecker()
        self.ip_syntax_checker = IPSyntaxChecker()
        self.url_syntax_checker = URLSyntaxChecker()

        self.params = ReputationCheckerParams()

        self.status = ReputationCheckerStatus()
        self.status.params = self.params
        self.status.dns_lookup_record = self.dns_query_tool.lookup_record

        super().__init__(
            subject, do_syntax_check_first=do_syntax_check_first, db_session=db_session
        )

    @staticmethod
    def is_valid() -> bool:
        raise NotImplementedError()

    def subject_propagator(self) -> "CheckerBase":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.
        """

        self.dns_query_tool.set_subject(self.idna_subject)

        self.domain_syntax_checker.subject = self.idna_subject
        self.ip_syntax_checker.subject = self.idna_subject
        self.url_syntax_checker.subject = self.idna_subject

        self.status = ReputationCheckerStatus()
        self.status.params = self.params
        self.status.dns_lookup_record = self.dns_query_tool.lookup_record

        self.status.subject = self.subject
        self.status.idna_subject = self.idna_subject

        self.query_syntax_checker()

        return self

    def should_we_continue_test(self, status_post_syntax_checker: str) -> bool:
        """
        Checks if we are allowed to continue a standard testing.
        """

        return bool(
            not self.status.status
            or status_post_syntax_checker == PyFunceble.storage.STATUS.invalid
        )

    def query_syntax_checker(self) -> "ReputationCheckerBase":
        """
        Queries the syntax checker.
        """

        self.status.second_level_domain_syntax = (
            self.domain_syntax_checker.is_valid_second_level()
        )
        self.status.subdomain_syntax = self.domain_syntax_checker.is_valid_subdomain()
        self.status.domain_syntax = bool(
            self.status.subdomain_syntax or self.status.second_level_domain_syntax
        )

        self.status.ipv4_syntax = self.ip_syntax_checker.is_valid_v4()
        self.status.ipv6_syntax = self.ip_syntax_checker.is_valid_v6()
        self.status.ipv4_range_syntax = self.ip_syntax_checker.is_valid_v4_range()
        self.status.ipv6_range_syntax = self.ip_syntax_checker.is_valid_v6_range()
        self.status.ip_syntax = bool(self.status.ipv4_syntax or self.status.ipv6_syntax)
        self.status.url_syntax = self.url_syntax_checker.is_valid()

        return self

    def query_a_record(self) -> Optional[List[str]]:
        """
        Queries all the A record.
        """

        raise NotImplementedError()

    def try_to_query_status_from_dns_lookup(self) -> "ReputationCheckerBase":
        """
        Tries to query the status from the DNS lookup.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: DNS Lookup",
            self.status.idna_subject,
        )

        if not self.status.ipv4_syntax:
            lookup_result = self.query_a_record()
            self.status.dns_lookup = lookup_result
        else:
            lookup_result = [self.status.subject]

        if lookup_result:
            for subject in lookup_result:
                if subject in self.ipv4_reputation_query_tool:
                    self.status.status = PyFunceble.storage.STATUS.malicious
                    self.status.status_source = "REPUTATION"

                    PyFunceble.facility.Logger.info(
                        "Could define the status of %r from: DNS Lookup",
                        self.status.idna_subject,
                    )

                    break

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: DNS Lookup",
            self.status.idna_subject,
        )

        return self

    def try_to_query_status_from_syntax_lookup(self) -> "ReputationCheckerBase":
        """
        Tries to query the status from the syntax.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: Syntax Lookup",
            self.status.idna_subject,
        )

        if (
            not self.status.domain_syntax
            and not self.status.ip_syntax
            and not self.status.url_syntax
        ):
            self.status.status = PyFunceble.storage.STATUS.invalid
            self.status.status_source = "SYNTAX"

            PyFunceble.facility.Logger.info(
                "Could define the status of %r from: Syntax Lookup",
                self.status.idna_subject,
            )

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: Syntax Lookup",
            self.status.idna_subject,
        )

        return self

    @CheckerBase.ensure_subject_is_given
    @CheckerBase.update_status_date_after_query
    def query_status(self) -> "ReputationCheckerBase":
        """
        Queries the status and for for more action.
        """

        status_post_syntax_checker = None

        if not self.status.status and self.do_syntax_check_first:
            self.try_to_query_status_from_syntax_lookup()

            if self.status.status:
                status_post_syntax_checker = self.status.status

        if self.should_we_continue_test(status_post_syntax_checker):
            self.try_to_query_status_from_dns_lookup()

        if not self.status.status:
            self.status.status = PyFunceble.storage.STATUS.sane
            self.status.status_source = "REPUTATION"

            PyFunceble.facility.Logger.info(
                "Could not define the status of %r. Setting to %r",
                self.status.idna_subject,
                self.status.status,
            )

        return self

    # pylint: disable=useless-super-delegation
    def get_status(self) -> Optional[ReputationCheckerStatus]:
        return super().get_status()
