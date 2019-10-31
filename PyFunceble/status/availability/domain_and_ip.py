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

    def __gather_dns_lookup(self):
        """
        Handle the lack of WHOIS record by doing a DNS Lookup.
        """

        self.status.dns_lookup = PyFunceble.DNSLOOKUP.request(self.subject)

        if self.status["_status"].lower() not in PyFunceble.STATUS.list.invalid:
            if self.status.dns_lookup:
                self.status["_status"] = PyFunceble.STATUS.official.up
            else:
                self.status["_status"] = PyFunceble.STATUS.official.down

            PyFunceble.LOGGER.debug(
                f'[{self.subject}] State before extra rules:\n{self.status["_status"]}'
            )

            self.status.status, self.status.status_source = ExtraRules(
                self.subject, self.subject_type, self.status.http_status_code
            ).handle(self.status["_status"], self.status["_status_source"])
        else:
            if self.status.dns_lookup:
                self.status["_status"] = PyFunceble.STATUS.official.up
                self.status["_status_source"] = "DNSLOOKUP"

            self.status.status, self.status.status_source = (
                self.status["_status"],
                self.status["_status_source"],
            )

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
            if self.status.ipv6_syntax_validation:
                self.status.http_status_code = PyFunceble.lookup.HTTPCode(
                    self.subject, "ipv6"
                ).get()
            else:
                self.status.http_status_code = PyFunceble.lookup.HTTPCode(
                    self.subject, self.subject_type
                ).get()

            if not self.status.subdomain_syntax_validation:
                (
                    self.status.expiration_date,
                    self.status.whois_record,
                ) = self.__gather_expiration_date()

                if isinstance(self.status.expiration_date, str):
                    self.status["_status_source"] = self.status.status_source = "WHOIS"
                    self.status[
                        "_status"
                    ] = self.status.status = PyFunceble.STATUS.official.up
                else:
                    self.status["_status_source"] = "DNSLOOKUP"
                    self.status["_status"] = PyFunceble.STATUS.official.down
                    self.__gather_dns_lookup()
            else:
                self.status["_status_source"] = "DNSLOOKUP"
                self.status["_status"] = PyFunceble.STATUS.official.down
                self.__gather_dns_lookup()
        else:
            self.status["_status_source"] = "SYNTAX"
            self.status["_status"] = PyFunceble.STATUS.official.invalid

            self.__gather_dns_lookup()

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
