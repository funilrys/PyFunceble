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
from typing import Dict, List, Optional

import PyFunceble.storage
from PyFunceble.checker.availability.params import AvailabilityCheckerParams
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.query.record.dns import DNSQueryToolRecord
from PyFunceble.query.record.whois import WhoisQueryToolRecord


@dataclasses.dataclass
class AvailabilityCheckerStatus(CheckerStatusBase):
    """
    Provides the description of an availablity status.
    """

    # pylint: disable=too-many-instance-attributes

    checker_type: Optional[str] = "AVAILABILITY"

    dns_lookup_record: Optional[DNSQueryToolRecord] = None
    whois_lookup_record: Optional[WhoisQueryToolRecord] = None

    domain_syntax: Optional[bool] = None
    second_level_domain_syntax: Optional[bool] = None
    subdomain_syntax: Optional[bool] = None

    ip_syntax: Optional[bool] = None
    ipv4_syntax: Optional[bool] = None
    ipv6_syntax: Optional[bool] = None
    ipv4_range_syntax: Optional[bool] = None
    ipv6_range_syntax: Optional[bool] = None
    url_syntax: Optional[bool] = None

    expiration_date: Optional[str] = None
    whois_record: Optional[str] = None

    status_before_extra_rules: Optional[str] = None
    status_after_extra_rules: Optional[str] = None

    status_source_before_extra_rules: Optional[str] = None
    status_source_after_extra_rules: Optional[str] = None

    dns_lookup: Optional[Dict[str, Optional[List[str]]]] = None
    netinfo: Optional[Dict[str, Optional[List[str]]]] = None
    http_status_code: Optional[int] = None

    def __post_init__(self) -> None:
        self.dns_lookup_record = DNSQueryToolRecord()
        self.whois_lookup_record = WhoisQueryToolRecord()
        self.params = AvailabilityCheckerParams()

    def is_special(self) -> bool:
        """
        Checks if the current status is a SPECIAL one.
        Meaning that we applied some of our own rules.
        """

        return bool(self.status_after_extra_rules)

    def is_available(self) -> bool:
        """
        Checks if the current status represent an available subject.
        """

        return self.is_active()

    def is_active(self) -> bool:
        """
        Checks if the current status is an ACTIVE one.
        """

        return self.status == PyFunceble.storage.STATUS.up

    def is_inactive(self) -> bool:
        """
        Checks if the current status is an INACTIVE one.
        """

        return self.status == PyFunceble.storage.STATUS.down

    def is_invalid(self) -> bool:
        """
        Checks if the current status is an INVALID one.
        """

        return self.status == PyFunceble.storage.STATUS.invalid
