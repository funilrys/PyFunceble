import PyFunceble

from .status import Status


# pylint: disable=too-many-instance-attributes
class GathererBase:
    def __init__(self, subject, filename=None, whois_db=None, inactive_db=None):
        if not subject:
            raise PyFunceble.exceptions.UnknownSubject(subject)

        self.subject = subject
        self.filename = filename

        self.whois_db = whois_db
        self.inactive_db = inactive_db

        self.exclude_file_generation = (
            self.inactive_db is not None
            and self.inactive_db.authorized
            and self.subject in self.inactive_db.to_retest
        )

        PyFunceble.LOGGER.debug(f"[{self.subject}] File: {self.filename}")
        PyFunceble.LOGGER.debug(
            f"[{self.subject}] Exclude file generation: {self.exclude_file_generation}"
        )

        if self.filename:
            self.subject_type = "file_"
        else:
            self.subject_type = ""

        self.status = Status(self.subject)
        self.checker = self.status.checker

    def get(self):
        """
        Provides the status.
        """

        return self.status.get()
