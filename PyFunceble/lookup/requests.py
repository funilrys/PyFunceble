"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the HTTP lookup/request interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

from urllib.parse import urlparse

import requests

import PyFunceble


class HostSSLAdapter(requests.adapters.HTTPAdapter):
    """
    Extends the build-in HTTP Adapter for urllib3 for our needs.
    """

    def __resolve_with_cache(self, hostname):
        """
        Resolve the IP of the given hostname.

        :param str hostname: The hostname to resolve.

        :return: The IP of the host name or the hostname itself.
        :rtype: None, str
        """

        if not hasattr(self, "__resolve_cache"):
            # pylint:disable=attribute-defined-outside-init
            self.__resolve_cache = {hostname: self.resolve(hostname)}
        elif hostname not in self.__resolve_cache:
            self.__resolve_cache[hostname] = self.resolve(hostname)

        return self.__resolve_cache[hostname]

    @classmethod
    def resolve(cls, hostname):
        """
        Resolve the IP of the given hostname.

        :param str hostname: The hostname to resolve.

        :return: The IP of the host name or the hostname itself.
        :rtype: None, str
        """

        try:
            records = PyFunceble.DNSLOOKUP.a_record(hostname)
        except AttributeError:
            records = None

        if isinstance(records, list):
            return records[0]

        return None

    # pylint: disable=arguments-differ
    def send(self, request, **kwargs):
        """
        Overwrite the upstream :code:send` method.

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

        parsed_url = urlparse(request.url)
        hostname_ip = self.__resolve_with_cache(parsed_url.hostname)

        PyFunceble.LOGGER.info(
            f"{parsed_url}, {hostname_ip}, {parsed_url.scheme}, {kwargs}"
        )

        if parsed_url.scheme == "https" and hostname_ip:
            request.url = request.url.replace(
                f"https://{parsed_url.hostname}", f"https://{hostname_ip}"
            )

            self.poolmanager.connection_pool_kw["server_hostname"] = parsed_url.hostname
            self.poolmanager.connection_pool_kw["assert_hostname"] = parsed_url.hostname

            # Ensure that the Hosts header is present. Otherwise, connection might
            # not work.
            request.headers["Host"] = parsed_url.hostname
        elif parsed_url.scheme == "http" and hostname_ip:
            request.url = request.url.replace(
                f"http://{parsed_url.hostname}", f"http://{hostname_ip}"
            )
        else:
            self.poolmanager.connection_pool_kw.pop(
                "server_hostname", "pyfunceble-not-resolved"
            )
            self.poolmanager.connection_pool_kw.pop(
                "assert_hostname", "pyfunceble-not-resolved"
            )

            request.url = "https://pyfunceble-not-resolved"

        return super(HostSSLAdapter, self).send(request, **kwargs)


class HostAdapter(requests.adapters.HTTPAdapter):
    """
    Extends the build-in HTTP Adapter for urllib3 for our needs.
    """

    def __resolve_with_cache(self, hostname):
        """
        Resolve the IP of the given hostname.

        :param str hostname: The hostname to resolve.

        :return: The IP of the host name or the hostname itself.
        :rtype: None, str
        """

        if not hasattr(self, "__resolve_cache"):
            # pylint:disable=attribute-defined-outside-init
            self.__resolve_cache = {hostname: HostSSLAdapter.resolve(hostname)}
        elif hostname not in self.__resolve_cache:
            self.__resolve_cache[hostname] = HostSSLAdapter.resolve(hostname)

        return self.__resolve_cache[hostname]

    # pylint: disable=arguments-differ
    def send(self, request, **kwargs):
        """
        Overwrite the upstream :code:send` method.

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
            must be a path to a CA bundle to use.
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """

        parsed_url = urlparse(request.url)
        hostname_ip = self.__resolve_with_cache(parsed_url.hostname)

        PyFunceble.LOGGER.info(
            f"{parsed_url}, {hostname_ip}, {parsed_url.scheme}, {kwargs}"
        )

        if parsed_url.scheme == "http" and hostname_ip:
            request.url = request.url.replace(
                f"http://{parsed_url.hostname}", f"http://{hostname_ip}"
            )

            # Ensure that the Hosts header is present. Otherwise, connection might
            # not work.
            request.headers["Host"] = parsed_url.hostname
        elif parsed_url.scheme == "https" and hostname_ip:
            request.url = request.url.replace(
                f"https://{parsed_url.hostname}", f"https://{hostname_ip}"
            )

            self.poolmanager.connection_pool_kw["server_hostname"] = parsed_url.hostname
            self.poolmanager.connection_pool_kw["assert_hostname"] = parsed_url.hostname

            # Ensure that the Hosts header is present. Otherwise, connection might
            # not work.
            request.headers["Host"] = parsed_url.hostname
        else:
            self.poolmanager.connection_pool_kw.pop(
                "server_hostname", "pyfunceble-not-resolved"
            )
            self.poolmanager.connection_pool_kw.pop(
                "assert_hostname", "pyfunceble-not-resolved"
            )

            request.url = "http://pyfunceble-not-resolved"

        return super(HostAdapter, self).send(request, **kwargs)


class Requests:
    """
    Handles all usage of :code:`requests`.

    :param str url: The URL to work with.
    """

    exceptions = requests.exceptions
    pyfunceble_max_retry = False

    def __init__(self):
        self.session = requests.Session()
        self.session.mount(
            "https://", HostSSLAdapter(max_retries=self.pyfunceble_max_retry)
        )
        self.session.mount(
            "http://", HostAdapter(max_retries=self.pyfunceble_max_retry)
        )

    def get(self, url, **kwargs):
        """
        Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting GET request to {url} with {kwargs}.")
        result = self.session.get(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished GET request to {url} with {kwargs}.")

        return result

    def options(self, url, **kwargs):
        """
        Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting OPTIONS request to {url} with {kwargs}.")
        result = self.session.options(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished OPTIONS request to {url} with {kwargs}.")

        return result

    def head(self, url, **kwargs):
        """
        Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting HEAD request to {url} with {kwargs}.")
        result = self.session.head(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished HEAD request to {url} with {kwargs}.")

        return result

    def post(self, url, **kwargs):
        """
        Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting POST request to {url} with {kwargs}.")
        result = self.session.post(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished POST request to {url} with {kwargs}.")

        return result

    def put(self, url, **kwargs):
        """
        Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting PUT request to {url} with {kwargs}.")
        result = self.session.put(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished PUT request to {url} with {kwargs}.")

        return result

    def patch(self, url, **kwargs):
        """
        Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting PATCH request to {url} with {kwargs}.")
        result = self.session.patch(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished PATCH request to {url} with {kwargs}.")

        return result

    def delete(self, url, **kwargs):
        """
        Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        PyFunceble.LOGGER.debug(f"Starting DELETE request to {url} with {kwargs}.")
        result = self.session.delete(url, **kwargs)
        PyFunceble.LOGGER.debug(f"Finished DELETE request to {url} with {kwargs}.")

        return result
