import PyFunceble

from ..gatherer_base import GathererBase


class Url(GathererBase):
    """
    Gather the availability of the given URL.
    """

    # pylint: disable=no-member

    def __init__(self, subject, filename=None, whois_db=None, inactive_db=None):
        super().__init__(
            subject, filename=filename, whois_db=whois_db, inactive_db=inactive_db
        )

        self.subject_type += "url"

        # We initiate the list of active status code.
        self.active_list = []
        self.active_list.extend(PyFunceble.HTTP_CODE.list.potentially_up)
        self.active_list.extend(PyFunceble.HTTP_CODE.list.up)

        # We initiate the list of inactive status code.
        self.inactive_list = []
        self.inactive_list.extend(PyFunceble.HTTP_CODE.list.potentially_down)
        self.inactive_list.append(PyFunceble.HTTP_CODE.not_found_default)

        self.__gather()

    def __gather(self):
        """
        Process the gathering.
        """

        self.status["_status_source"] = self.status.status_source = "URL"

        if PyFunceble.CONFIGURATION.local or self.status.url_syntax_validation:
            if self.status.http_status_code in self.active_list:
                self.status[
                    "_status"
                ] = self.status.status = PyFunceble.STATUS.official.up
            elif self.status.http_status_code in self.inactive_list:
                self.status[
                    "_status"
                ] = self.status.status = PyFunceble.STATUS.official.down
        else:
            self.status["_status_source"] = self.status.status_source = "SYNTAX"
            self.status[
                "_status"
            ] = self.status.status = PyFunceble.STATUS.official.invalid

        PyFunceble.output.Generate(
            self.subject,
            self.subject_type,
            self.status.status,
            source=self.status.status_source,
            http_status_code=self.status.http_status_code,
            filename=self.filename,
        ).status_file(
            exclude_file_generation=(
                self.exclude_file_generation
                and self.status.status not in [PyFunceble.STATUS.official.up]
            )
        )

        PyFunceble.LOGGER.debug(f"[{self.subject}] State:\n{self.status.get()}")
