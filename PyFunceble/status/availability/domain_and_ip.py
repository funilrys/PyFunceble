"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the status interface for domains and IP availability check.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import PyFunceble

from ..gatherer_base import GathererBase
from .extra_rules import ExtraRules


class DomainAndIp(GathererBase):
    """
    Gather the availability of the given
    IP or Domain.
    """

    # pylint: disable=no-member

    def __init__(self, subject, filename=None, whois_db=None, inactive_db=None):
        super().__init__(
            subject, filename=filename, whois_db=whois_db, inactive_db=inactive_db
        )

        self.subject_type += "domain"
        self.__gather()

    def __gather_expiration_date(self):
        """
        Gather the expiration date.
        """

        if not self.status.whois_server:
            return None, None

        if self.whois_db:
            expiration_date_from_database = self.whois_db.get_expiration_date(
                self.subject
            )
        else:
            expiration_date_from_database = None

        if expiration_date_from_database:
            return expiration_date_from_database, "DATE EXTRACTED FROM WHOIS DATABASE"

        whois_record = PyFunceble.lookup.Whois(
            self.subject,
            self.status.whois_server,
            timeout=PyFunceble.CONFIGURATION.timeout,
        ).request()

        try:
            expiration_date = PyFunceble.extractor.ExpirationDate(
                whois_record
            ).get_extracted()

            if expiration_date and not PyFunceble.helpers.Regex(
                r"[0-9]{2}\-[a-z]{3}\-2[0-9]{3}"
            ).match(expiration_date, return_match=False):
                # The formatted expiration date does not match our unified format.

                # We log the problem.
                PyFunceble.output.Logs().expiration_date(self.subject, expiration_date)

                PyFunceble.LOGGER.error(
                    "Expiration date of "
                    f"{repr(self.subject)} ({repr(expiration_date)}) "
                    "was not converted proprely."
                )

            if self.whois_db:
                # We save the whois record into the database.
                self.whois_db.add(self.subject, expiration_date, whois_record)
        except PyFunceble.exceptions.WrongParameterType:
            expiration_date = None

        return expiration_date, whois_record

    def __gather_extra_rules(self):
        """
        Handle the lack of WHOIS record.
        """

        if self.status["_status"].lower() not in PyFunceble.STATUS.list.invalid:
            if self.status["_status"].lower() in PyFunceble.STATUS.list.down:
                self.status.dns_lookup = PyFunceble.DNSLOOKUP.request(self.subject)

                if self.status.dns_lookup:
                    self.status["_status"] = PyFunceble.STATUS.official.up
                    self.status["_status_source"] = "DNSLOOKUP"
                else:
                    self.status["_status"] = PyFunceble.STATUS.official.down
                    self.status["_status_source"] = "DNSLOOKUP"
        else:
            self.status.dns_lookup = PyFunceble.DNSLOOKUP.request(self.subject)

            if self.status.dns_lookup:
                # This is a safety. Indeed, as I may not be that reactive in the
                # future, this allow a new rule to be checked with the dns lookup
                # logic.

                self.status["_status"] = PyFunceble.STATUS.official.up
                self.status["_status_source"] = "DNSLOOKUP"

        PyFunceble.LOGGER.debug(
            f'[{self.subject}] State before extra rules:\n{self.status["_status"]}'
        )

        self.gather_http_status_code()

        self.status.status, self.status.status_source = ExtraRules(
            self.subject, self.subject_type, self.status.http_status_code
        ).handle(self.status["_status"], self.status["_status_source"])

    def __gather(self):
        """
        Process the gathering.
        """

        ip_validation = (
            self.status.ipv4_syntax_validation or self.status.ipv6_syntax_validation
        )

        if (
            PyFunceble.CONFIGURATION.local
            or self.status.domain_syntax_validation
            or ip_validation
        ):
            if not self.status.subdomain_syntax_validation:
                (
                    self.status.expiration_date,
                    self.status.whois_record,
                ) = self.__gather_expiration_date()

                if isinstance(self.status.expiration_date, str):
                    self.status["_status_source"] = "WHOIS"
                    self.status["_status"] = PyFunceble.STATUS.official.up
                    self.__gather_extra_rules()
                else:
                    self.status["_status_source"] = "WHOIS"
                    self.status["_status"] = PyFunceble.STATUS.official.down
                    self.__gather_extra_rules()
            else:
                self.status["_status_source"] = "SYNTAX"
                self.status["_status"] = PyFunceble.STATUS.official.down
                self.__gather_extra_rules()
        else:
            self.status["_status_source"] = "SYNTAX"
            self.status["_status"] = PyFunceble.STATUS.official.invalid

            self.__gather_extra_rules()

        PyFunceble.output.Generate(
            self.subject,
            self.subject_type,
            self.status.status,
            source=self.status.status_source,
            expiration_date=self.status.expiration_date,
            http_status_code=self.status.http_status_code,
            whois_server=self.status.whois_server,
            filename=self.filename,
            ip_validation=ip_validation,
        ).status_file(
            exclude_file_generation=(
                self.exclude_file_generation
                and self.status.status not in [PyFunceble.STATUS.official.up]
            )
        )

        PyFunceble.LOGGER.debug(f"[{self.subject}] State:\n{self.status.get()}")
