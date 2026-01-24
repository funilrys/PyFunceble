"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to provide the nameserver to use.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025, 2026 Nissar Chababy

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

from typing import List, Optional, Union

import dns.resolver

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.query.dns.nameserver import Nameservers


class Resolver:
    """
    Provides the right resolver.

    :param nameservers:
        The list of nameservers to communicate with.
    """

    STD_TIMEOUT: float = 5.0

    _timeout: float = 3.0

    _nameservers: Nameservers = None
    _internal_resolver: Optional[dns.resolver.Resolver] = None

    def __init__(
        self, nameservers: Optional[List[str]] = None, timeout: Optional[float] = None
    ) -> None:
        self._nameservers = Nameservers()

        if nameservers is not None:
            self.nameservers = nameservers
        else:
            self.nameservers.guess_and_set_nameservers()

        if timeout is not None:
            self.timeout = timeout
        else:
            self.guess_and_set_timeout()

    @property
    def resolver(self) -> dns.resolver.Resolver:
        """
        Provides the resolver to work with.
        """

        if not self._internal_resolver:
            if self.get_raw_nameservers():
                self._internal_resolver = dns.resolver.Resolver(configure=False)
            else:  # pragma: no cover ## I don't want to play with the default resolver.
                self._internal_resolver = dns.resolver.Resolver()

            self._internal_resolver.lifetime = self.timeout + 2.0
            self._internal_resolver.timeout = self.timeout
            self._internal_resolver.nameservers = self.get_raw_nameservers()
            self._internal_resolver.nameserver_ports = self.get_raw_nameserver_ports()

        return self._internal_resolver

    @property
    def nameservers(self) -> Nameservers:
        """
        Provides the nameservers to use.
        """

        return self._nameservers

    @nameservers.setter
    def nameservers(self, value: List[str]) -> None:
        """
        Sets the nameservers to use.
        """

        self.nameservers.set_nameservers(value)
        self._internal_resolver = None  # Invalidate

    def set_nameservers(self, value: List[str]) -> "Resolver":
        """
        Sets the given nameserver.
        """

        self.nameservers = value

        return self

    @property
    def timeout(self) -> float:
        """
        Provides the timeout to use.
        """

        return self._timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        """
        Sets the timeout to use.
        """

        if not isinstance(value, (float, int)):
            raise TypeError(f"<value> should be {float}, {type(value)} given.")

        self._timeout = float(value)
        self._internal_resolver = None  # Invalidate

    def set_timeout(self, value: Union[float, int]) -> "Resolver":
        """
        Sets the timeout of a query.
        """

        self.timeout = value

        return self

    def get_raw_nameservers(self) -> Optional[List[str]]:
        """
        Provides the currently set list of nameserver.
        """

        return self.nameservers.get_nameservers()

    def get_raw_nameserver_ports(self) -> Optional[dict]:
        """
        Provides the currently set list of nameserver ports.
        """

        return self.nameservers.get_nameserver_ports()

    def guess_and_set_timeout(self) -> "Resolver":
        """
        Tries to guess the the timeout from the configuration.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.timeout = PyFunceble.storage.CONFIGURATION.lookup.timeout
        else:
            self.timeout = self.STD_TIMEOUT

        return self

    def guess_all_settings(
        self,
    ) -> "Resolver":  # pragma: no cover ## Method themselves are more important
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self
