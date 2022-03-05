"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the URL syntax checker.

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


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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


import urllib.parse
from typing import Optional

from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.syntax.base import SyntaxCheckerBase
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker


class URLSyntaxChecker(SyntaxCheckerBase):
    """
    Provides an interface to check the syntax of a URL.

    :param str subject:
        Optional, The subject to work with.
    """

    @staticmethod
    def get_hostname_from_url(url: str) -> Optional[str]:
        """
        Extract the hostname part of the given URL.

        .. versionadded:: 4.1.0b7
        """

        parsed = urllib.parse.urlparse(url)

        if not parsed.scheme or not parsed.netloc:
            return None

        if parsed.hostname:
            if parsed.hostname != parsed.netloc:
                hostname = parsed.hostname
            else:
                hostname = parsed.netloc
        else:  ## pragma: no cover ## Safety check.
            hostname = parsed.netloc

        return hostname

    @CheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Validate the given subject.

        .. versionchanged:: 4.1.0b5.dev
           URL with scheme and port are no longer :code:`INVALID`.

        .. versionchanged:: 4.1.0b7.dev
           Hostname taken from :code:`get_hostname_from_url`
        """

        hostname = self.get_hostname_from_url(self.idna_subject)

        if not hostname:
            return False

        if (
            DomainSyntaxChecker(hostname).is_valid()
            or IPSyntaxChecker(hostname).is_valid()
        ):
            return True

        return False
