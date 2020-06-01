"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the status gatherer base.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

import PyFunceble

from .status import Status


# pylint: disable=too-many-instance-attributes
class GathererBase:
    """
    Provides the gatherer base.

    :param str subject:
        The subject to gather data for.
    :param str filename:
        The filename which the subject is associated with.
    :param whois_db:
        An instance of the whois db interface.
    :param inactive_db:
        An instance of the inactive db interface.
    """

    # pylint: disable=no-member

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

    def gather_http_status_code(self):
        """
        Univertialy gather the status code.
        """

        if self.status.ipv6_syntax_validation:
            self.status.http_status_code = PyFunceble.lookup.HTTPCode(
                self.subject, "ipv6"
            ).get()
        else:
            self.status.http_status_code = PyFunceble.lookup.HTTPCode(
                self.subject, self.subject_type
            ).get()
