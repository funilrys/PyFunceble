"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to provides the nameserver to use.

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

import functools
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

    timeout: float = 3.0

    nameservers: Nameservers = Nameservers()
    internal_resolver: Optional[dns.resolver.Resolver] = None

    def __init__(
        self, nameservers: Optional[List[str]] = None, timeout: Optional[float] = None
    ) -> None:
        if nameservers is not None:
            self.set_nameservers(nameservers)
        else:
            self.nameservers.guess_and_set_nameservers()

        if timeout is not None:
            self.set_timeout(timeout)
        else:
            self.guess_and_set_timeout()

    def configure_resolver(func):  # pylint: disable=no-self-argument
        """
        Configures the resolvers after calling the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.internal_resolver.lifetime = self.timeout + 2.0
            self.internal_resolver.timeout = self.timeout
            self.internal_resolver.nameservers = self.nameservers.get_nameservers()
            self.internal_resolver.nameserver_ports = (
                self.nameservers.get_nameserver_ports()
            )

            return result

        return wrapper

    def set_nameservers(self, value: List[str]) -> "Resolver":
        """
        Sets the given nameserver.
        """

        self.nameservers.set_nameservers(value)

    def set_timeout(self, value: Union[float, int]) -> "Resolver":
        """
        Sets the timeout of a query.
        """

        if not isinstance(value, (float, int)):
            raise TypeError(f"<value> should be {float}, {type(value)} given.")

        self.timeout = float(value)

        return self

    def get_nameservers(self) -> Optional[List[str]]:
        """
        Provides the currently set list of nameserver.
        """

        return self.nameservers.get_nameservers()

    def get_nameserver_ports(self) -> Optional[dict]:
        """
        Provides the currently set list of nameserver ports.
        """

        return self.nameservers.get_nameserver_ports()

    def get_timeout(self) -> Optional[float]:
        """
        Provides the currently set query timeout.
        """

        return self.timeout

    def guess_and_set_timeout(self) -> "Resolver":
        """
        Tries to guess the the timeout from the configuration.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.set_timeout(float(PyFunceble.storage.CONFIGURATION.lookup.timeout))
        else:
            self.set_timeout(self.STD_TIMEOUT)

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

    @configure_resolver
    def get_resolver(self) -> dns.resolver.Resolver:
        """
        Provides the resolver to work with.
        """

        if self.internal_resolver:
            return self.internal_resolver

        if self.nameservers.get_nameservers():
            self.internal_resolver = dns.resolver.Resolver(configure=False)
        else:  # pragma: no cover ## I don't want to play with the default resolver.
            self.internal_resolver = dns.resolver.Resolver()

        return self.internal_resolver
