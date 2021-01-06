"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our adapter.

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

import requests.adapters

from PyFunceble.query.dns.query_tool import DNSQueryTool


class RequestAdapterBase(requests.adapters.HTTPAdapter):
    """
    Extends the built-in HTTP adapater and acts as a base for all our own
    adapter.
    """

    resolving_cache: dict = dict()
    resolving_use_cache: bool = False
    timeout: float = 5.0

    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self.timeout = float(kwargs["timeout"])
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)

    def resolve_with_cache(self, hostname: str) -> Optional[str]:
        """
        Try to resolve using an internal cache.
        """

        if hostname not in self.resolving_cache:
            self.resolving_cache[hostname] = self.resolve_without_cache(hostname)

        return self.resolving_cache[hostname]

    @staticmethod
    def resolve_without_cache(hostname: str) -> Optional[str]:
        """
        Resolves the IP of the given hostname.

        :param hostname:
            The hostname to get resolve.
        """

        result = (
            DNSQueryTool()
            .guess_all_settings()
            .set_query_record_type("A")
            .set_subject(hostname)
            .query()
        )

        if result:
            return result[0]
        return None

    def resolve(self, hostname: str) -> Optional[str]:
        """
        Resolves with the prefered method.
        """

        if self.resolving_use_cache:
            return self.resolve_with_cache(hostname)
        return self.resolve_without_cache(hostname)
