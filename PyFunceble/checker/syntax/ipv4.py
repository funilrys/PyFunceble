"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the IPv4 syntax checker.

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

import ipaddress

from PyFunceble.checker.base import CheckerBase
from PyFunceble.helpers.regex import RegexHelper


class IPv4SyntaxChecker(CheckerBase):
    """
    Provides an interface to check the syntax of an IPv4.

    :param str subject:
        Optional, The subject to work with.
    """

    @staticmethod
    def _get_regex_reserved_ip() -> str:
        """
        Provides the regex to use to match all known reserved IPv4.
        """

        # pylint: disable=line-too-long
        reserved = [
            # Match 0.0.0.0–0.255.255.255
            r"(0\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 10.0.0.0–10.255.255.255
            r"(10\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 100.64.0.0–100.127.255.255
            r"(100\.(0?6[4-9]|0?[7-9][0-9]|1[0-1][0-9]|12[0-7])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 127.0.0.0–127.255.255.255
            r"(127\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 169.254.0.0–169.254.255.255
            r"(169\.254\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 172.16.0.0–172.31.255.255
            r"(172\.(0?1[6-9]|0?2[0-9]|0?3[0-1])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.0.0.0–192.0.0.255
            r"(192\.0\.0\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.0.2.0–192.0.2.255
            r"(192\.0\.2\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.31.196.0–192.31.196.255
            r"(192\.31\.196\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.52.193.0–192.52.193.255
            r"(192\.52\.193\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.88.99.0–192.88.99.255
            r"(192\.88\.99\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.168.0.0–192.168.255.255
            r"(192\.168\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 192.175.48.0-192.175.48.255
            r"(192\.175\.48\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))",
            # Match 198.18.0.0–198.19.255.255
            r"(198\.(0?1[8-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 198.51.100.0–198.51.100.255
            r"(198\.51\.100\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 203.0.113.0–203.0.113.255
            r"(203\.0\.113\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 224.0.0.0–239.255.255.255
            r"((22[4-9]|23[0-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 240.0.0.0–255.255.255.254
            r"((24[0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",
            # Match 255.255.255.255
            r"(255\.255\.255\.255)",
        ]
        # pylint: enable=enable-too-long

        return "({0})".format("|".join(reserved))

    @CheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Validate the given subject.
        """

        try:
            try:
                return ipaddress.ip_address(self.idna_subject).version == 4
            except ValueError:
                try:
                    return ipaddress.ip_interface(self.idna_subject).version == 4
                except ValueError:
                    return (
                        ipaddress.ip_network(self.idna_subject, strict=False).version
                        == 4
                    )
        except ValueError:
            return False

    @CheckerBase.ensure_subject_is_given
    def is_valid_range(self) -> bool:
        """
        Checks if the given subject is an IPv4 range
        """

        if self.is_valid() and "/" in self.idna_subject:
            return 0 <= int(self.idna_subject[self.idna_subject.rfind("/") + 1 :]) <= 32
        return False

    @CheckerBase.ensure_subject_is_given
    def is_reserved(self) -> bool:
        """
        Checks if the given subject is a reserved IPv4.
        """

        if self.is_valid():
            try:
                address = ipaddress.IPv4Address(self.idna_subject)

                return (
                    address.is_multicast
                    or address.is_private
                    or address.is_unspecified
                    or address.is_reserved
                    or address.is_loopback
                    or address.is_link_local
                    or not address.is_global
                    or RegexHelper(self._get_regex_reserved_ip()).match(
                        self.idna_subject, return_match=False
                    )
                )
            except ValueError:
                pass
        return False
