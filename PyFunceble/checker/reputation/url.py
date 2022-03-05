"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides URL reputation checker classes.

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


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

from PyFunceble.checker.reputation.base import ReputationCheckerBase
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.converter.url2netloc import Url2Netloc


class URLReputationChecker(ReputationCheckerBase):
    """
    Provides the URL reputation checker.

    :param str subject:
        Optional, The subject to work with.
    :param bool do_syntax_check_first:
        Optional, Activates/Disables the check of the status before the actual
        status gathering.
    """

    def query_a_record(self) -> Optional[List[str]]:
        url_base = Url2Netloc(self.status.subject).get_converted()

        ip_syntax_checker = IPSyntaxChecker(url_base)

        if ip_syntax_checker.is_valid_v4():
            return [url_base]

        if ip_syntax_checker.is_valid_v6() or (
            url_base.startswith("[") and url_base.endswith("]")
        ):

            url_base = url_base.replace("[", "").replace("]", "")

            result = set()

            for subject in (
                self.dns_query_tool.set_query_record_type("PTR")
                .set_subject(url_base)
                .query()
            ):
                result.update(
                    self.dns_query_tool.set_subject(subject)
                    .set_query_record_type("A")
                    .query()
                )

            self.dns_query_tool.subject = self.idna_subject

            return result

        result = (
            self.dns_query_tool.set_query_record_type("A").set_subject(url_base).query()
        )

        self.dns_query_tool.subject = self.idna_subject

        return result
