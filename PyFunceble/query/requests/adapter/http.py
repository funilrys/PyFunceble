"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the our HTTP adapter.

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

import urllib.parse

import requests

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.query.requests.adapter.base import RequestAdapterBase


class RequestHTTPAdapter(RequestAdapterBase):
    """
    Provides our HTTP adapter.
    """

    # pylint: disable=arguments-differ
    def send(self, request, **kwargs) -> requests.Response:
        """
        Overwrite the upstream :code:`send` method.

        We basically do the same. We only ensure that we request the IP from the chosen
        DNS record.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or
            a :ref:`(connect timeout, read timeout) <timeouts>` tuple.
        :type timeout: float or tuple or urllib3 Timeout object
        :param verify: (optional) Either a boolean, in which case it controls whether
            we verify the server's TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """

        kwargs["timeout"] = self.timeout

        parsed_url = urllib.parse.urlparse(request.url)
        hostname_ip = self.resolve(parsed_url.hostname)

        PyFunceble.facility.Logger.debug("Parsed URL: %r", parsed_url)
        PyFunceble.facility.Logger.debug("Resolved IP: %r", hostname_ip)
        PyFunceble.facility.Logger.debug("KWARGS: %r", kwargs)
        PyFunceble.facility.Logger.debug(
            "Pool Manager: %r", self.poolmanager.connection_pool_kw
        )

        if hostname_ip:
            request.url = request.url.replace(
                f"{parsed_url.scheme}://{parsed_url.hostname}",
                f"{parsed_url.scheme}://{hostname_ip}",
            )

            # Ensure that the Hosts header is present. Otherwise, connection might
            # not work.
            request.headers["Host"] = parsed_url.hostname
        else:
            self.poolmanager.connection_pool_kw.pop(
                "server_hostname", PyFunceble.storage.NOT_RESOLVED_STD_HOSTNAME
            )
            self.poolmanager.connection_pool_kw.pop(
                "assert_hostname", PyFunceble.storage.NOT_RESOLVED_STD_HOSTNAME
            )

            request.url = f"http://{PyFunceble.storage.NOT_RESOLVED_STD_HOSTNAME}"

        response = super().send(request, **kwargs)
        response.url = response.url.replace(hostname_ip, parsed_url.hostname)

        return response
