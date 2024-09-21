"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the domains and IP syntax checker.

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

from PyFunceble.checker.syntax.base import SyntaxCheckerBase
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker


class DomainAndIPSyntaxChecker(SyntaxCheckerBase):
    """
    Provides the interface for checking the syntax of an IP or domain.

    :param str subject:
        Optional, The subject to work with.
    """

    @SyntaxCheckerBase.ensure_subject_is_given
    @SyntaxCheckerBase.update_status_date_after_query
    def query_status(
        self,
    ) -> "DomainAndIPSyntaxChecker":  # pragma: no cover ## Just a switch.
        """
        Queries the result without anything more.
        """

        query_object: Union[IPSyntaxChecker, DomainSyntaxChecker] = None

        ip_checker = IPSyntaxChecker(self.subject)

        if ip_checker.is_valid():
            query_object = ip_checker
        else:
            query_object = DomainSyntaxChecker(self.subject, db_session=self.db_session)

        query_object.platform_query_tool = self.platform_query_tool

        result = query_object.query_status()

        self.__dict__.update(query_object.__dict__)

        return result
