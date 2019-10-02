# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will manage the status.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long

from urllib.parse import urlparse

import requests

import PyFunceble


class HostSSLAdapter(requests.adapters.HTTPAdapter):
    """
    Extends the build-in HTTP Adapter for urllib3 for our needs.
    """

    @classmethod
    def resolve(cls, hostname):
        """
        Resolve the IP of the given hostname.

        :param str hostname: The hostname to resolve.

        :return: The IP of the host name or the hostname itself.
        :rtype: None, str
        """

        try:
            records = PyFunceble.DNSLookup(
                hostname, dns_server=PyFunceble.CONFIGURATION.dns_server, complete=False
            ).a_record()
        except AttributeError:
            records = PyFunceble.DNSLookup(
                hostname, dns_server=None, complete=False
            ).a_record()

        if isinstance(records, list):
            return records[0]

        return None

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        """
        Overwrite the upstream :code:send` method.

        We basically do the same. We only ensure that we request the IP from the choosen
        DNS record.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple or urllib3 Timeout object
        :param verify: (optional) Either a boolean, in which case it controls whether
            we verify the server's TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """

        parsed_url = urlparse(request.url)
        hostname_ip = self.resolve(parsed_url.hostname)

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
            self.poolmanager.connection_pool_kw.pop("server_hostname", None)
            self.poolmanager.connection_pool_kw.pop("assert_hostname", None)

        return super(HostSSLAdapter, self).send(
            request, stream=False, timeout=None, verify=True, cert=None, proxies=None
        )


class HostAdapter(requests.adapters.HTTPAdapter):
    """
    Extends the build-in HTTP Adapter for urllib3 for our needs.
    """

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        """
        Overwrite the upstream :code:send` method.

        We basically do the same. We only ensure that we request the IP from the choosen
        DNS record.

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :param stream: (optional) Whether to stream the request content.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple or urllib3 Timeout object
        :param verify: (optional) Either a boolean, in which case it controls whether
            we verify the server's TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use
        :param cert: (optional) Any user-provided SSL certificate to be trusted.
        :param proxies: (optional) The proxies dictionary to apply to the request.
        :rtype: requests.Response
        """

        parsed_url = urlparse(request.url)
        hostname_ip = HostSSLAdapter.resolve(parsed_url.hostname)

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

            self.poolmanager.connection_pool_kw.pop("server_hostname", None)
            self.poolmanager.connection_pool_kw.pop("assert_hostname", None)

        return super(HostAdapter, self).send(
            request, stream=False, timeout=None, verify=True, cert=None, proxies=None
        )


class Requests:
    """
    Handles all usage of :code:`requests`.
    """

    exceptions = requests.exceptions

    pyfunceble_max_retry = 3

    @classmethod
    def get(cls, url, **kwargs):
        """
        Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.get(url, **kwargs)

    @classmethod
    def options(cls, url, **kwargs):
        """
        Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.options(url, **kwargs)

    @classmethod
    def head(cls, url, **kwargs):
        """
        Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.head(url, **kwargs)

    @classmethod
    def post(cls, url, **kwargs):
        """
        Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.post(url, **kwargs)

    @classmethod
    def put(cls, url, **kwargs):
        """
        Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.put(url, **kwargs)

    @classmethod
    def patch(cls, url, **kwargs):
        """
        Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.patch(url, **kwargs)

    @classmethod
    def delete(cls, url, **kwargs):
        """
        Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        session = requests.Session()

        if url.startswith("https:"):
            session.mount(
                "https://", HostSSLAdapter(max_retries=cls.pyfunceble_max_retry)
            )
        else:
            session.mount("http://", HostAdapter(max_retries=cls.pyfunceble_max_retry))

        return session.delete(url, **kwargs)
