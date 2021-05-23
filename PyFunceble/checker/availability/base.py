"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all availability checker classes.

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

import multiprocessing
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

import PyFunceble.checker.utils.whois
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.params import AvailabilityCheckerParams
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.helpers.regex import RegexHelper
from PyFunceble.query.dns.query_tool import DNSQueryTool
from PyFunceble.query.http_status_code import HTTPStatusCode
from PyFunceble.query.netinfo.address import AddressInfo
from PyFunceble.query.netinfo.hostbyaddr import HostByAddrInfo
from PyFunceble.query.whois.query_tool import WhoisQueryTool


class AvailabilityCheckerBase(CheckerBase):
    """
    Provides the base of all our availability checker classes.

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

    # pylint: disable=too-many-public-methods, too-many-instance-attributes

    STD_USE_EXTRA_RULES: bool = True
    STD_USE_WHOIS_LOOKUP: bool = True
    STD_USE_DNS_LOOKUP: bool = True
    STD_USE_NETINFO_LOOKUP: bool = True
    STD_USE_HTTP_CODE_LOOKUP: bool = True
    STD_USE_REPUTATION_LOOKUP: bool = False
    STD_USE_WHOIS_DB: bool = True

    dns_query_tool: Optional[DNSQueryTool] = None
    whois_query_tool: Optional[WhoisQueryTool] = None
    addressinfo_query_tool: Optional[AddressInfo] = None
    hostbyaddr_query_tool: Optional[HostByAddrInfo] = None
    http_status_code_query_tool: Optional[HTTPStatusCode] = None
    domain_syntax_checker: Optional[DomainSyntaxChecker] = None
    ip_syntax_checker: Optional[IPSyntaxChecker] = None
    url_syntax_checker: Optional[URLSyntaxChecker] = None

    _use_extra_rules: bool = False
    _use_whois_lookup: bool = False
    _use_dns_lookup: bool = False
    _use_netinfo_lookup: bool = False
    _use_http_code_lookup: bool = False
    _use_reputation_lookup: bool = False
    _use_whois_db: bool = False

    status: Optional[AvailabilityCheckerStatus] = None
    params: Optional[AvailabilityCheckerParams] = None

    def __init__(
        self,
        subject: Optional[str] = None,
        *,
        use_extra_rules: Optional[bool] = None,
        use_whois_lookup: Optional[bool] = None,
        use_dns_lookup: Optional[bool] = None,
        use_netinfo_lookup: Optional[bool] = None,
        use_http_code_lookup: Optional[bool] = None,
        use_reputation_lookup: Optional[bool] = None,
        do_syntax_check_first: Optional[bool] = None,
        db_session: Optional[Session] = None,
        use_whois_db: Optional[bool] = None,
    ) -> None:
        self.dns_query_tool = DNSQueryTool().guess_all_settings()
        self.whois_query_tool = WhoisQueryTool()
        self.addressinfo_query_tool = AddressInfo()
        self.hostbyaddr_query_tool = HostByAddrInfo()
        self.http_status_code_query_tool = HTTPStatusCode()
        self.domain_syntax_checker = DomainSyntaxChecker()
        self.ip_syntax_checker = IPSyntaxChecker()
        self.url_syntax_checker = URLSyntaxChecker()
        self.db_session = db_session

        self.params = AvailabilityCheckerParams()

        self.status = AvailabilityCheckerStatus()
        self.status.params = self.params
        self.status.dns_lookup_record = self.dns_query_tool.lookup_record
        self.status.whois_lookup_record = self.whois_query_tool.lookup_record

        if use_extra_rules is not None:
            self.use_extra_rules = use_extra_rules
        else:
            self.guess_and_set_use_extra_rules()

        if use_whois_lookup is not None:
            self.use_whois_lookup = use_whois_lookup
        else:
            self.guess_and_set_use_whois_lookup()

        if use_dns_lookup is not None:
            self.use_dns_lookup = use_dns_lookup
        else:
            self.guess_and_set_dns_lookup()

        if use_netinfo_lookup is not None:
            self.use_netinfo_lookup = use_netinfo_lookup
        else:
            self.guess_and_set_use_netinfo_lookup()

        if use_http_code_lookup is not None:
            self.use_http_code_lookup = use_http_code_lookup
        else:
            self.guess_and_set_use_http_code_lookup()

        if use_reputation_lookup is not None:
            self.use_reputation_lookup = use_reputation_lookup
        else:
            self.guess_and_set_use_reputation_lookup()

        if use_whois_db is not None:
            self.use_whois_db = use_whois_db
        else:
            self.guess_and_set_use_whois_db()

        super().__init__(
            subject, do_syntax_check_first=do_syntax_check_first, db_session=db_session
        )

    @property
    def use_extra_rules(self) -> bool:
        """
        Provides the current value of the :code:`_use_extra_rules` attribute.
        """

        return self._use_extra_rules

    @use_extra_rules.setter
    def use_extra_rules(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the special rule.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_extra_rules = self.params.use_extra_rules = value

    def set_use_extra_rules(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the special rule.

        :param value:
            The value to set.
        """

        self.use_extra_rules = value

        return self

    @property
    def use_whois_lookup(self) -> bool:
        """
        Provides the current value of the :code:`_use_whois_lookup` attribute.
        """

        return self._use_whois_lookup

    @use_whois_lookup.setter
    def use_whois_lookup(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the WHOIS lookup.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_whois_lookup = self.params.use_whois_lookup = value

    def set_use_whois_lookup(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the WHOIS lookup.

        :param value:
            The value to set.
        """

        self.use_whois_lookup = value

        return self

    @property
    def use_dns_lookup(self) -> bool:
        """
        Provides the current value of the :code:`_use_dns_lookup` attribute.
        """

        return self._use_dns_lookup

    @use_dns_lookup.setter
    def use_dns_lookup(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the DNS Lookup.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_dns_lookup = self.params.use_dns_lookup = value

    def set_use_dns_lookup(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the DNS Lookup.

        :param value:
            The value to set.
        """

        self.use_dns_lookup = value

        return self

    @property
    def use_netinfo_lookup(self) -> bool:
        """
        Provides the current value of the :code:`_use_netinfo_lookup` attribute.
        """

        return self._use_netinfo_lookup

    @use_netinfo_lookup.setter
    def use_netinfo_lookup(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the network information
        lookup.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_netinfo_lookup = self.params.use_netinfo_lookup = value

    def set_use_netinfo_lookup(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the network information
        lookup.

        :param value:
            The value to set.
        """

        self.use_netinfo_lookup = value

        return self

    @property
    def use_http_code_lookup(self) -> None:
        """
        Provides the current value of the :code:`_use_http_code_lookup` attribute.
        """

        return self._use_http_code_lookup

    @use_http_code_lookup.setter
    def use_http_code_lookup(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the HTTP status code
        lookup.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_http_code_lookup = self.params.use_http_code_lookup = value

    def set_use_http_code_lookup(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the HTTP status code
        lookup.

        :param value:
            The value to set.
        """

        self.use_http_code_lookup = value

        return self

    @property
    def use_reputation_lookup(self) -> bool:
        """
        Provides the current value of the :code:`_use_reputation_lookup` attribute.
        """

        return self._use_reputation_lookup

    @use_reputation_lookup.setter
    def use_reputation_lookup(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the reputation
        lookup.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_reputation_lookup = self.params.use_reputation_lookup = value

    def set_use_reputation_lookup(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the reputation
        lookup.

        :param value:
            The value to set.
        """

        self.use_reputation_lookup = value

        return self

    @property
    def use_whois_db(self) -> bool:
        """
        Provides the current value of the :code:`_use_whois_db` attribute.
        """

        return self._use_whois_db

    @use_whois_db.setter
    def use_whois_db(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the WHOIS DB.

        :param value:
            The value to set.

        :param TypeError:
            When the given :code:`use_whois_db` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_whois_db = self.params.use_whois_db = value

    def set_use_whois_db(self, value: bool) -> "AvailabilityCheckerBase":
        """
        Sets the value which authorizes the usage of the WHOIS DB.

        :param value:
            The value to set.
        """

        self.use_whois_db = value

        return self

    def subject_propagator(self) -> "CheckerBase":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.
        """

        self.dns_query_tool.set_subject(self.idna_subject)
        self.whois_query_tool.set_subject(self.idna_subject)
        self.addressinfo_query_tool.set_subject(self.idna_subject)
        self.hostbyaddr_query_tool.set_subject(self.idna_subject)
        self.http_status_code_query_tool.set_subject(self.idna_subject)

        self.domain_syntax_checker.subject = self.idna_subject
        self.ip_syntax_checker.subject = self.idna_subject
        self.url_syntax_checker.subject = self.idna_subject

        self.status = AvailabilityCheckerStatus()
        self.status.params = self.params
        self.status.dns_lookup_record = self.dns_query_tool.lookup_record
        self.status.whois_lookup_record = self.whois_query_tool.lookup_record

        self.status.subject = self.subject
        self.status.idna_subject = self.idna_subject
        self.status.status = None

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

    def guess_and_set_use_extra_rules(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_extra_rules` attribute
        from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_extra_rules = PyFunceble.storage.CONFIGURATION.lookup.special
        else:
            self.use_extra_rules = self.STD_USE_EXTRA_RULES

        return self

    def guess_and_set_use_whois_lookup(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_whois` attribute
        from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_whois_lookup = PyFunceble.storage.CONFIGURATION.lookup.whois
        else:
            self.use_whois_lookup = self.STD_USE_WHOIS_LOOKUP

        return self

    def guess_and_set_dns_lookup(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_dns_lookup` attribute
        from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_dns_lookup = PyFunceble.storage.CONFIGURATION.lookup.dns
        else:
            self.use_dns_lookup = self.STD_USE_DNS_LOOKUP

        return self

    def guess_and_set_use_netinfo_lookup(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_netinfo_lookup` attribute
        from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_netinfo_lookup = PyFunceble.storage.CONFIGURATION.lookup.netinfo
        else:
            self.use_netinfo_lookup = self.STD_USE_NETINFO_LOOKUP

        return self

    def guess_and_set_use_http_code_lookup(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_http_code_lookup` attribute
        from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_http_code_lookup = (
                PyFunceble.storage.CONFIGURATION.lookup.http_status_code
            )
        else:
            self.use_http_code_lookup = self.STD_USE_HTTP_CODE_LOOKUP

        return self

    def guess_and_set_use_reputation_lookup(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_reputation_lookup` attribute
        from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_reputation_lookup = (
                PyFunceble.storage.CONFIGURATION.lookup.reputation
            )
        else:
            self.use_reputation_lookup = self.STD_USE_REPUTATION_LOOKUP

        return self

    def guess_and_set_use_whois_db(self) -> "AvailabilityCheckerBase":
        """
        Try to guess and set the value of the :code:`use_whois_db` attribute.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.use_whois_db = PyFunceble.storage.CONFIGURATION.cli_testing.whois_db
        else:
            self.use_whois_db = self.STD_USE_WHOIS_DB

    def guess_all_settings(
        self,
    ) -> "AvailabilityCheckerBase":  # pragma: no cover ## Method are more important
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self

    def query_syntax_checker(self) -> "AvailabilityCheckerBase":
        """
        Queries the syntax checker.
        """

        PyFunceble.facility.Logger.info(
            "Started to check the syntax of %r", self.status.idna_subject
        )

        self.status.second_level_domain_syntax = (
            self.domain_syntax_checker.is_valid_second_level()
        )
        self.status.subdomain_syntax = self.domain_syntax_checker.is_valid_subdomain()
        self.status.domain_syntax = bool(self.status.subdomain_syntax) or bool(
            self.status.second_level_domain_syntax
        )

        self.status.ipv4_syntax = self.ip_syntax_checker.is_valid_v4()
        self.status.ipv6_syntax = self.ip_syntax_checker.is_valid_v6()
        self.status.ipv4_range_syntax = self.ip_syntax_checker.is_valid_v4_range()
        self.status.ipv6_range_syntax = self.ip_syntax_checker.is_valid_v6_range()
        self.status.ip_syntax = bool(self.status.ipv4_syntax or self.status.ipv6_syntax)
        self.status.url_syntax = self.url_syntax_checker.is_valid()

        PyFunceble.facility.Logger.info(
            "Finished to check the syntax of %r", self.status.idna_subject
        )

        return self

    @CheckerBase.ensure_subject_is_given
    def query_dns_record(self) -> Optional[Dict[str, Optional[List[str]]]]:
        """
        Tries to query the DNS record(s) of the given subject.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the DNS record of %r.",
            self.status.idna_subject,
        )

        result = dict()

        if self.status.subdomain_syntax:
            lookup_order = ["NS", "A", "AAAA", "CNAME", "DNAME"]
        elif self.status.domain_syntax:
            lookup_order = ["NS", "CNAME", "A", "AAAA", "DNAME"]
        elif self.status.ip_syntax:
            lookup_order = ["PTR"]
        else:
            lookup_order = []

        if lookup_order:
            for record_type in lookup_order:
                local_result = self.dns_query_tool.set_query_record_type(
                    record_type
                ).query()

                if local_result:
                    result[record_type] = local_result

                    break

        PyFunceble.facility.Logger.debug("DNS Record:\n%r", result)

        PyFunceble.facility.Logger.info(
            "Finished to try to query the DNS record of %r",
            self.status.idna_subject,
        )

        return result

    def try_to_query_status_from_whois(
        self,
    ) -> "AvailabilityCheckerBase":
        """
        Tries to get and the status from the WHOIS record.

        .. warning::
            If the configuration is loaded, this method try to query from the
            best database first.

            If it's not found it will try to query it from the best WHOIS server
            then add it into the database (if the expiration date
            extraction is successful).

        .. note::
            The addition into the WHOIS database is only done if this method is
            running in a thread with a name that does not starts with
            :code:`PyFunceble` (case sensitive).
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: WHOIS Lookup",
            self.status.idna_subject,
        )

        if (
            PyFunceble.facility.ConfigLoader.is_already_loaded() and self.use_whois_db
        ):  # pragma: no cover ## Not interesting enough to spend time on it.
            whois_object = PyFunceble.checker.utils.whois.get_whois_dataset_object(
                db_session=self.db_session
            )
            known_record = whois_object[self.subject]

            if known_record and not isinstance(known_record, dict):
                # Comes from DB engine.
                known_record = known_record.to_dict()

            if not known_record:
                # We assume that expired dataset are never saved into the
                # dataset.
                self.status.expiration_date = (
                    self.whois_query_tool.get_expiration_date()
                )
                self.status.whois_record = self.whois_query_tool.lookup_record.record

                if (
                    self.status.expiration_date
                    and not multiprocessing.current_process().name.startswith(
                        PyFunceble.storage.PROJECT_NAME.lower()
                    )
                ):
                    whois_object.update(
                        {
                            "subject": self.subject,
                            "idna_subject": self.idna_subject,
                            "expiration_date": self.status.expiration_date,
                            "epoch": str(
                                datetime.strptime(
                                    self.status.expiration_date, "%d-%b-%Y"
                                ).timestamp()
                            ),
                        }
                    )
            else:
                self.status.expiration_date = known_record["expiration_date"]
                self.status.whois_record = None
        else:
            self.status.expiration_date = self.whois_query_tool.get_expiration_date()
            self.status.whois_record = self.whois_query_tool.lookup_record.record

        if self.status.expiration_date:
            self.status.status = PyFunceble.storage.STATUS.up
            self.status.status_source = "WHOIS"

            PyFunceble.facility.Logger.info(
                "Could define the status of %r from: WHOIS Lookup",
                self.status.idna_subject,
            )

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: WHOIS Lookup",
            self.status.idna_subject,
        )

        return self

    def try_to_query_status_from_dns(self) -> "AvailabilityCheckerBase":
        """
        Tries to query the status from the DNS lookup.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: DNS Lookup",
            self.status.idna_subject,
        )

        lookup_result = self.query_dns_record()

        if lookup_result:
            self.status.dns_lookup = lookup_result
            self.status.status = PyFunceble.storage.STATUS.up
            self.status.status_source = "DNSLOOKUP"

            PyFunceble.facility.Logger.info(
                "Could define the status of %r from: DNS Lookup",
                self.status.idna_subject,
            )

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: DNS Lookup",
            self.status.idna_subject,
        )

        return self

    def try_to_query_status_from_netinfo(self) -> "AvailabilityCheckerBase":
        """
        Tries to query the status from the network information.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: NETINFO Lookup",
            self.status.idna_subject,
        )

        if self.status.domain_syntax:
            lookup_result = self.addressinfo_query_tool.get_info()
        elif self.status.ip_syntax:
            lookup_result = self.hostbyaddr_query_tool.get_info()
        elif self.status.idna_subject.isdigit():
            lookup_result = None
        else:
            lookup_result = self.addressinfo_query_tool.get_info()

        if lookup_result:
            self.status.netinfo = lookup_result
            self.status.status = PyFunceble.storage.STATUS.up
            self.status.status_source = "NETINFO"

            PyFunceble.facility.Logger.info(
                "Could define the status of %r from: NETINFO Lookup",
                self.status.idna_subject,
            )

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: NETINFO Lookup",
            self.status.idna_subject,
        )

        return self

    def try_to_query_status_from_http_status_code(self) -> "AvailabilityCheckerBase":
        """
        Tries to query the status from the HTTP status code.
        """

        PyFunceble.facility.Logger.info(
            "Started to try to query the status of %r from: HTTP Status code Lookup",
            self.status.idna_subject,
        )

        if not self.status.url_syntax and not RegexHelper("[^a-z0-9._]").match(
            self.idna_subject, return_match=False
        ):
            # The regex is there because while testing for domain, sometime we
            # may see something like mailto:xxx@yyy.de

            self.http_status_code_query_tool.set_subject(
                f"http://{self.idna_subject}:80"
            )

        lookup_result = self.http_status_code_query_tool.get_status_code()

        if (
            lookup_result
            and lookup_result
            != self.http_status_code_query_tool.STD_UNKNOWN_STATUS_CODE
        ):
            self.status.http_status_code = lookup_result

            if (
                PyFunceble.facility.ConfigLoader.is_already_loaded()
            ):  # pragma: no cover ## Special behavior.
                dataset = PyFunceble.storage.HTTP_CODES
            else:
                dataset = PyFunceble.storage.STD_HTTP_CODES

            if (
                not self.status.status
                or self.status.status == PyFunceble.storage.STATUS.down
            ) and (
                self.status.http_status_code in dataset.list.up
                or self.status.http_status_code in dataset.list.potentially_up
            ):
                self.status.status = PyFunceble.storage.STATUS.up
                self.status.status_source = "HTTP CODE"

                PyFunceble.facility.Logger.info(
                    "Could define the status of %r from: HTTP Status code Lookup",
                    self.status.idna_subject,
                )
        else:
            self.status.http_status_code = None

        PyFunceble.facility.Logger.info(
            "Finished to try to query the status of %r from: HTTP Status code Lookup",
            self.status.idna_subject,
        )

        return self

    def try_to_query_status_from_syntax_lookup(self) -> "AvailabilityCheckerBase":
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

    def try_to_query_status_from_reputation(self) -> "AvailabilityCheckerBase":
        """
        Tries to query the status from the reputation lookup.
        """

        raise NotImplementedError()

    @CheckerBase.ensure_subject_is_given
    @CheckerBase.update_status_date_after_query
    def query_status(self) -> "AvailabilityCheckerBase":
        """
        Queries the status and for for more action.
        """

        raise NotImplementedError()

    # pylint: disable=useless-super-delegation
    def get_status(self) -> Optional[AvailabilityCheckerStatus]:
        return super().get_status()
