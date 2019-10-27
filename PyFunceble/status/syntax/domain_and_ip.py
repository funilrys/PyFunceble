import PyFunceble

from ..gatherer_base import GathererBase


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

    def __gather(self):
        """
        Process the gathering.
        """

        self.status["_status_source"] = self.status.status_source = "SYNTAX"

        if (
            self.status.domain_syntax_validation
            or self.status.ipv4_syntax_validation
            or self.status.ipv6_syntax_validation
        ):
            self.status[
                "_status"
            ] = self.status.status = PyFunceble.STATUS.official.valid
        else:
            self.status[
                "_status"
            ] = self.status.status = PyFunceble.STATUS.official.invalid

        PyFunceble.output.Generate(
            self.subject,
            self.subject_type,
            self.status.status,
            source=self.status.status_source,
            whois_server=self.status.whois_server,
            filename=self.filename,
            ip_validation=self.status.ipv4_syntax_validation
            or self.status.ipv6_syntax_validation,
        ).status_file()

        PyFunceble.LOGGER.debug(f"[{self.subject}] State:\n{self.status.get()}")
