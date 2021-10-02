"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the IP (v4 + v6) syntax checker.

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

from typing import Optional

from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.syntax.base import SyntaxCheckerBase
from PyFunceble.checker.syntax.ipv4 import IPv4SyntaxChecker
from PyFunceble.checker.syntax.ipv6 import IPv6SyntaxChecker
from PyFunceble.checker.syntax.status import SyntaxCheckerStatus


class IPSyntaxChecker(SyntaxCheckerBase):
    """
    Provides an interface to check the syntax of an IP (v6 or v4).

    :param str subject:
        Optional, The subject to work with.
    """

    ipv4_checker: Optional[IPv4SyntaxChecker] = None
    ipv6_checker: Optional[IPv6SyntaxChecker] = None

    def __init__(self, subject: Optional[str] = None) -> None:
        self.ipv4_checker = IPv4SyntaxChecker()
        self.ipv6_checker = IPv6SyntaxChecker()

        super().__init__(subject=subject)

    def subject_propagator(self) -> "IPSyntaxChecker":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.
        """

        self.ipv4_checker.subject = self.idna_subject
        self.ipv6_checker.subject = self.idna_subject

        self.status = SyntaxCheckerStatus()

        self.status.subject = self.subject
        self.status.idna_subject = self.idna_subject

        return self

    @CheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Validate the given subject.
        """

        return self.is_valid_v4() or self.is_valid_v6()

    @CheckerBase.ensure_subject_is_given
    def is_valid_v4(self) -> bool:
        """
        Checks if the given subject is a valid IPv4.
        """

        return self.ipv4_checker.is_valid()

    @CheckerBase.ensure_subject_is_given
    def is_valid_v6(self) -> bool:
        """
        Checks if the given subject is a valid IPv6.
        """

        return self.ipv6_checker.is_valid()

    @CheckerBase.ensure_subject_is_given
    def is_valid_range(self) -> bool:
        """
        Checks if the given subject is an IP range.
        """

        return self.is_valid_v4_range() or self.is_valid_v6_range()

    @CheckerBase.ensure_subject_is_given
    def is_valid_v4_range(self) -> bool:
        """
        Checks if the given subject is an IPv4 range.
        """

        return self.ipv4_checker.is_valid_range()

    @CheckerBase.ensure_subject_is_given
    def is_valid_v6_range(self) -> bool:
        """
        Checks if the given subject is an IPv6 range.
        """

        return self.ipv6_checker.is_valid_range()

    @CheckerBase.ensure_subject_is_given
    def is_reserved(self) -> bool:
        """
        Checks if the given subject is a reserved IP.
        """

        return self.is_reserved_v4() or self.is_reserved_v6()

    @CheckerBase.ensure_subject_is_given
    def is_reserved_v4(self) -> bool:
        """
        Checks if the given subject is a reserved IPv4.
        """

        return self.ipv4_checker.is_reserved()

    @CheckerBase.ensure_subject_is_given
    def is_reserved_v6(self) -> bool:
        """
        Checks if the given subject is a reserved IPv6.
        """

        return self.ipv6_checker.is_reserved()
