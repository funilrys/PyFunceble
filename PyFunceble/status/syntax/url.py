"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the status interface for URL syntax check.

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

from ..gatherer_base import GathererBase


class Url(GathererBase):
    """
    Gather the syntax of the given URL.
    """

    # pylint: disable=no-member

    def __init__(self, subject, filename=None, whois_db=None, inactive_db=None):
        super().__init__(
            subject, filename=filename, whois_db=whois_db, inactive_db=inactive_db
        )

        self.subject_type += "url"

        self.__gather()

    def __gather(self):
        """
        Process the gathering.
        """

        self.status["_status_source"] = self.status.status_source = "SYNTAX"

        if self.status.url_syntax_validation:
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
