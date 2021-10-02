"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the second level domain syntax checker.

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

from PyFunceble.checker.syntax.domain_base import DomainSyntaxCheckerBase
from PyFunceble.helpers.regex import RegexHelper


class SecondLvlDomainSyntaxChecker(DomainSyntaxCheckerBase):
    """
    Provides an interface to check the syntax of a second domain.

    :param str subject:
        Optional, The subject to work with.
    """

    # pylint: disable=line-too-long
    REGEX_VALID_DOMAIN: str = r"^(?=.{0,253}$)(([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9](?:\.)?|[a-z0-9](?:\.)?))$"

    last_point_index: Optional[int] = None
    """
    Saves the index of the last point.
    """

    @DomainSyntaxCheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Validate the given subject.

        .. warning::
            A valid domain may also be a valid subdomain.

            If you precisely want to check a subdomain please refer to the
            right checker (not this one :-) )!
        """

        # pylint: disable=too-many-return-statements

        extension = self.get_extension()

        if not extension or (
            extension not in self.iana_dataset
            and extension not in self.SPECIAL_USE_DOMAIN_NAMES_EXTENSIONS
        ):
            return False

        subject_without_extension = self.idna_subject[: self.last_point_index]
        subject_without_suffix, _ = self.get_subject_without_suffix(
            self.idna_subject, extension
        )

        if subject_without_suffix:
            if "." in subject_without_suffix:
                return False

            return RegexHelper(self.REGEX_VALID_DOMAIN).match(
                self.idna_subject, return_match=False
            )

        if "." in subject_without_extension:
            return False

        return RegexHelper(self.REGEX_VALID_DOMAIN).match(
            self.idna_subject, return_match=False
        )
