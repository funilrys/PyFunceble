"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to get or guess the nameserver to use.

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

from typing import List, Optional, Tuple

import dns.exception
import dns.resolver

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.converter.url2netloc import Url2Netloc


class Nameservers:
    """
    Provides an interface to get the right nameserver to communicate with.
    """

    nameservers: Optional[List[str]] = None
    nameserver_ports: Optional[dict] = None

    protocol: Optional[str] = None

    domain_syntax_checker: DomainSyntaxChecker = DomainSyntaxChecker()
    url_syntax_checker: URLSyntaxChecker = URLSyntaxChecker()
    url2netloc: Url2Netloc = Url2Netloc()

    def __init__(
        self, nameserver: Optional[List[str]] = None, protocol: str = "TCP"
    ) -> None:
        self.protocol = protocol

        if nameserver is not None:
            self.set_nameservers(nameserver)

    @staticmethod
    def split_nameserver_from_port(
        nameserver: str,
        *,
        default_port: int = 53,
    ) -> Tuple[str, int]:
        """
        Splits the nameserver from its port.re

        :param nameserver:
            The nameserver to work with.
        :param default_port:
            The default port to apply, if none is found.
        """

        if ":" in nameserver:
            splitted = nameserver.rsplit(":")

            if splitted[-1].isdigit():
                return ":".join(splitted[:-1]), int(splitted[-1])

            return ":".join(splitted), default_port
        return nameserver, default_port

    @classmethod
    def get_ip_from_nameserver(cls, nameserver: str) -> List[str]:
        """
        Given a nameserver, this method resolve it in order to get the
        IP to contact.

        :param nameserver:
            The name to resolve.
        """

        PyFunceble.facility.Logger.info(
            "Started to get ip from nameserver (%r)", nameserver
        )

        result = []

        if cls.domain_syntax_checker.set_subject(nameserver).is_valid():
            try:
                result.extend(
                    [
                        x.address
                        for x in dns.resolver.Resolver().resolve(nameserver, "A")
                    ]
                )
            except dns.exception.DNSException:
                pass

            try:
                result.extend(
                    [
                        x.address
                        for x in dns.resolver.Resolver().resolve(nameserver, "AAAA")
                    ]
                )
            except dns.exception.DNSException:
                pass
        else:
            result.append(nameserver)

        PyFunceble.facility.Logger.debug(
            "IP from nameserver (%r):\n%r", nameserver, result
        )

        PyFunceble.facility.Logger.info(
            "Finished to get ip from nameserver (%r)", nameserver
        )

        return result

    def set_nameservers(self, value: List[str]) -> "Nameservers":
        """
        Sets the nameserver to use.

        Side Effect:
            Also updates the :code:`nameserver_ports` variable.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`list`.
        :raise ValueError:
            When the given :code:`value` is emtpy.
        """

        if not isinstance(value, list):
            raise TypeError(f"<value> should be {list}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self.nameserver_ports = dict()
        self.nameservers = list()

        for nameserver in value:
            if self.protocol.lower() == "https":
                if not nameserver.startswith("https://"):
                    netloc = self.url2netloc.set_data_to_convert(
                        nameserver
                    ).get_converted()

                    if "/" in nameserver:
                        path = nameserver[nameserver.find("/") :]
                    else:
                        path = ""

                    self.nameservers.append(
                        "https://"
                        # pylint: disable=line-too-long
                        f"{netloc}{path}"
                    )
                else:
                    self.nameservers.append(nameserver)

                # 443 is because it's more likely to be for DOH.
                self.nameserver_ports.update({self.nameservers[-1]: 443})
                continue

            server, port = self.split_nameserver_from_port(nameserver)

            for dns_ip in self.get_ip_from_nameserver(server):
                self.nameservers.append(dns_ip)
                self.nameserver_ports.update({dns_ip: port})

        return self

    def get_nameservers(self) -> Optional[List[str]]:
        """
        Provides the currently set nameservers.
        """

        return self.nameservers

    def get_nameserver_ports(self) -> Optional[dict]:
        """
        Provides the currently set nameserver_ports.
        """

        return self.nameserver_ports

    def guess_and_set_nameservers(self) -> "Nameservers":
        """
        Try to guess and set the nameserver to use.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if PyFunceble.storage.CONFIGURATION.dns.server:
                if isinstance(PyFunceble.storage.CONFIGURATION.dns.server, list):
                    self.set_nameservers(PyFunceble.storage.CONFIGURATION.dns.server)
                else:
                    self.set_nameservers([PyFunceble.storage.CONFIGURATION.dns.server])
            else:  # pragma: no cover
                ## Well, I don't like playing with the default resolver.
                self.set_nameservers(dns.resolver.get_default_resolver().nameservers)
        else:  # pragma: no cover
            ## Well, I don't like playing with the default resolver.
            self.set_nameservers(dns.resolver.get_default_resolver().nameservers)

        return self

    def guess_all_settings(
        self,
    ) -> "Nameservers":  # pragma: no cover ## Method themselves are more important
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self
