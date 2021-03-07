"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our status class. The status class is the class that will be provided
to end-user.

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

import dataclasses
from typing import List, Optional

import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.query.record.dns import DNSQueryToolRecord


@dataclasses.dataclass
class ReputationCheckerStatus(CheckerStatusBase):
    """
    Provides the description of an availablity status.
    """

    # pylint: disable=too-many-instance-attributes

    checker_type: Optional[str] = "REPUTATION"

    dns_lookup_record: Optional[DNSQueryToolRecord] = None

    domain_syntax: Optional[bool] = None
    second_level_domain_syntax: Optional[bool] = None
    subdomain_syntax: Optional[bool] = None

    ip_syntax: Optional[bool] = None
    ipv4_syntax: Optional[bool] = None
    ipv6_syntax: Optional[bool] = None
    ipv4_range_syntax: Optional[bool] = None
    ipv6_range_syntax: Optional[bool] = None
    url_syntax: Optional[bool] = None

    dns_lookup: Optional[List[str]] = None

    def __post_init__(self) -> None:
        self.dns_lookup_record = DNSQueryToolRecord()

    def has_bad_reputation(self) -> bool:
        """
        Checks if the current status represent an available subject.
        """

        return self.is_malicious()

    def is_sane(self) -> bool:
        """
        Checks if the current status is an SANE one.
        """

        return self.status == PyFunceble.storage.STATUS.sane

    def is_malicious(self) -> bool:
        """
        Checks if the current status is an MALICIOUS one.
        """

        return self.status == PyFunceble.storage.STATUS.malicious
