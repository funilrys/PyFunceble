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
            query_object = IPAvailabilityChecker()
        else:
            query_object = DomainAvailabilityChecker()

        query_object.__dict__ = self.__dict__

        result = query_object.query_status()

        self.__dict__.update(query_object.__dict__)

        return result

    @staticmethod
    def is_valid() -> bool:
        raise NotImplementedError()
