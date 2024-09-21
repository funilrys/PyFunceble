"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the IPv6 syntax checker.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import ipaddress

from PyFunceble.checker.base import CheckerBase


class IPv6SyntaxChecker(CheckerBase):
    """
    Provides an interface to check the syntax of an IPv6.

    :param str subject:
        Optional, The subject to work with.
    """

    @CheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Validate the given subject.
        """

        try:
            try:
                return ipaddress.ip_address(self.idna_subject).version == 6
            except ValueError:
                try:
                    return ipaddress.ip_interface(self.idna_subject).version == 6
                except ValueError:
                    return (
                        ipaddress.ip_network(self.idna_subject, strict=False).version
                        == 6
                    )
        except ValueError:
            return False

    @CheckerBase.ensure_subject_is_given
    def is_valid_range(self) -> bool:
        """
        Checks if the given subject is an IPv6 range.
        """

        if self.is_valid() and "/" in self.idna_subject:
            return (
                0 <= int(self.idna_subject[self.idna_subject.rfind("/") + 1 :]) <= 128
            )
        return False

    @CheckerBase.ensure_subject_is_given
    def is_reserved(self) -> bool:
        """
        Checks if the given subject is a reserved IPv6.
        """

        if self.is_valid():
            try:
                address = ipaddress.IPv6Address(self.idna_subject)

                return (
                    address.is_multicast
                    or address.is_private
                    or address.is_unspecified
                    or address.is_reserved
                    or address.is_loopback
                    or address.is_link_local
                    or not address.is_global
                )
            except ipaddress.AddressValueError:
                pass

        return False
