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
import requests.models

import PyFunceble.storage
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.query.dns.query_tool import DNSQueryTool


class RequestAdapterBase(requests.adapters.HTTPAdapter):
    """
    Extends the built-in HTTP adapater and acts as a base for all our own
    adapter.
    """

    resolving_cache: dict = {}
    resolving_use_cache: bool = False
    timeout: float = 5.0

    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self.timeout = float(kwargs["timeout"])
            del kwargs["timeout"]

        if "max_retries" in kwargs:
            kwargs["max_retries"] = requests.adapters.Retry(
                total=kwargs["max_retries"], respect_retry_after_header=False
            )

        if "dns_query_tool" in kwargs:
            self.dns_query_tool = kwargs["dns_query_tool"]
            del kwargs["dns_query_tool"]
        else:
            self.dns_query_tool = DNSQueryTool()

        super().__init__(*args, **kwargs)

    @staticmethod
    def fake_response() -> requests.models.Response:
        """
        Provides the fake response that is provided when we couldn't resolve the
        given domain.
        """

        raise PyFunceble.factory.Requester.exceptions.ConnectionError(
            "Could not resolve."
        )

    def resolve_with_cache(self, hostname: str) -> Optional[str]:
        """
        Try to resolve using an internal cache.
        """

        if hostname not in self.resolving_cache:
            self.resolving_cache[hostname] = self.resolve_without_cache(hostname)

        return self.resolving_cache[hostname]

    def resolve_without_cache(self, hostname: str) -> Optional[str]:
        """
        Resolves the IP of the given hostname.

        :param hostname:
            The hostname to get resolve.
        """

        def get_last_cname(subject: str, recursion_depth: int = 60) -> Optional[str]:
            """
            Given a subject, this function tries to query the CNAME until there
            is none.

            :param subject:
                The first subject.
            """

            last_cname_result = []
            last_cname_new_subject = subject

            depth = 0

            while depth < recursion_depth:
                local_last_cname_result = (
                    self.dns_query_tool.set_query_record_type("CNAME")
                    .set_subject(last_cname_new_subject)
                    .query()
                )

                depth += 1

                if any(x in last_cname_result for x in local_last_cname_result):
                    break

                last_cname_result.extend(local_last_cname_result)

                if local_last_cname_result:
                    last_cname_new_subject = local_last_cname_result[0]
                else:
                    break

            try:
                return last_cname_result[-1]
            except IndexError:
                return None

        result = set()

        if not IPSyntaxChecker(hostname).is_valid():
            last_cname = get_last_cname(hostname)

            if last_cname:
                result.update(
                    self.dns_query_tool.set_query_record_type("A")
                    .set_subject(last_cname)
                    .query()
                )
            else:
                result.update(
                    self.dns_query_tool.set_query_record_type("A")
                    .set_subject(hostname)
                    .query()
                )
        else:
            result.add(hostname)

        if result:
            return result.pop()
        return None

    def resolve(self, hostname: str) -> Optional[str]:
        """
        Resolves with the prefered method.
        """

        if hostname:
            if self.resolving_use_cache:
                return self.resolve_with_cache(hostname)
            return self.resolve_without_cache(hostname)
        return None
