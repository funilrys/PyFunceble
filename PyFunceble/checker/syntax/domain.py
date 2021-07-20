"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the general domain syntax checker.

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

from typing import Optional

from sqlalchemy.orm import Session

from PyFunceble.checker.syntax.base import SyntaxCheckerBase
from PyFunceble.checker.syntax.domain_base import DomainSyntaxCheckerBase
from PyFunceble.checker.syntax.second_lvl_domain import SecondLvlDomainSyntaxChecker
from PyFunceble.checker.syntax.status import SyntaxCheckerStatus
from PyFunceble.checker.syntax.subdomain import SubDomainSyntaxChecker


class DomainSyntaxChecker(DomainSyntaxCheckerBase, SyntaxCheckerBase):
    """
    Provides an interface to check the syntax of a domain.

    :param str subject:
        Optional, The subject to work with.
    """

    second_level_checker: Optional[SecondLvlDomainSyntaxChecker] = None
    subdomain_checker: Optional[SubDomainSyntaxChecker] = None

    def __init__(
        self, subject: Optional[str] = None, db_session: Optional[Session] = None
    ) -> None:
        self.second_level_checker: SecondLvlDomainSyntaxChecker = (
            SecondLvlDomainSyntaxChecker()
        )
        self.subdomain_checker: SubDomainSyntaxChecker = SubDomainSyntaxChecker()

        self.db_session = db_session
        super().__init__(subject)

    def subject_propagator(self) -> "DomainSyntaxChecker":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.
        """

        self.second_level_checker.subject = self.idna_subject
        self.subdomain_checker.subject = self.idna_subject

        self.status = SyntaxCheckerStatus()

        self.status.subject = self.subject
        self.status.idna_subject = self.idna_subject

        return self

    @DomainSyntaxCheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Validate the given subject if exists.
        """

        return self.is_valid_second_level() or self.is_valid_subdomain()

    @DomainSyntaxCheckerBase.ensure_subject_is_given
    def is_valid_second_level(self) -> bool:
        """
        Checks if the given subject is a valid second level demain.
        """

        return self.second_level_checker.is_valid()

    @DomainSyntaxCheckerBase.ensure_subject_is_given
    def is_valid_subdomain(self) -> bool:
        """
        Checks if the given subject is a valid subdomain
        """

        return self.subdomain_checker.is_valid()
