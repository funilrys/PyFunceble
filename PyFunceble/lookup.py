#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the lookup interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://funilrys.github.io/PyFunceble/

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

from socket import AF_INET, IPPROTO_TCP, SOCK_STREAM
from socket import error as socket_error
from socket import gaierror, getaddrinfo, gethostbyaddr, herror, socket
from socket import timeout as socket_timeout

from PyFunceble.check import Check
from PyFunceble.referer import Referer


class NSLookup:
    """
    Implementation of the UNIX :code:`nslookup` command.

    :param subject: The subject we are working with.
    :type subject: str

    :return:
        A dict with following index if an IPv4 is given.

            ::

                {
                    "addr_info" : []
                }

        A dict with following index for everythind else.

            ::

                {
                    "hostname": "xx",
                    "aliases": [],
                    "ips": []
                }

    :rtype: dict
    """

    def __init__(self, subject):
        if subject:
            if isinstance(subject, str):
                self.subject = subject
            else:
                raise ValueError("`subject` must be a string.")
        else:
            raise ValueError("`subject` must be given.")

    def request(self):
        """
        Perform the NS request.
        """

        result = {}

        try:
            if not Check(self.subject).is_ip_valid():
                # We are looking for something which is not an IP.

                # We request the address information.
                req = getaddrinfo(self.subject, 80, proto=IPPROTO_TCP)

                result["addr_info"] = []

                for sequence in req:
                    # We loop through the list returned by the request.

                    # We append the NS information into the output.
                    result["addr_info"].append(sequence[-1][0])
            else:
                req = gethostbyaddr(self.subject)

                result.update({"hostname": req[0], "aliases": req[1], "ips": req[2]})
        except (OSError, herror, gaierror):
            pass

        return result


class Whois:
    """
    Implementation of the UNIX `whois` command.

    :param subject: The subject we are working with.
    :type subject: str

    :param server:
        The WHOIS server we are working with.

        .. note::
            If none is given, we look for the best one.
    :type server: str

    :param timeout: 
        The timeout to apply.

        .. warning::
            The timeout must be a modulo of :code:`3`.
    :type timeout: int
    """

    universal_port = 43
    buffer_size = 4096

    def __init__(self, subject, server=None, timeout=3):
        if subject:
            if isinstance(subject, str):
                self.subject = subject
            else:
                raise ValueError("`subject` must be a string.")
        else:
            raise ValueError("`subject` must be given.")

        if server is not None:
            if isinstance(server, str):
                self.server = server
            else:
                raise ValueError("`server` must be a string.")
        else:
            self.server = Referer(self.subject).get()

        if timeout:
            if isinstance(timeout, int):
                self.timeout = timeout
            elif timeout.isdigit():
                self.timeout = int(timeout)
            else:
                raise ValueError("`timeout` must be an integer or digit string.")

    def request(self):
        """
        Perform the WHOIS request.
        """

        result = None

        if self.server:
            # A server was found or is given.

            # We initiate a socket for the request.
            req = socket(AF_INET, SOCK_STREAM)

            if self.timeout % 3 == 0:
                # The timeout is a modulo of 3.

                # We set the timeout.
                req.settimeout(self.timeout)

            try:
                # We try to connect to the whois server at the port 43.
                req.connect((self.server, self.universal_port))
            except socket_error:
                return result

            # We send and encode the domain we want the information from.
            req.send("{}\r\n".format(self.subject).encode())

            # We initiate a bytes variable which will save the response from the server.
            response = bytes("", "utf-8")

            while True:
                # We loop infinitly

                try:
                    data = req.recv(self.buffer_size)
                except (ConnectionResetError, socket_timeout):
                    # We got an error.

                    # We close the connection.
                    req.close()

                    # And we return the result.
                    return result

                # Wverythin goes right.

                # We append the data to the response.
                response += data

                if not data:
                    # The data is empty or equal to None.

                    # We close the connection.
                    req.close()

                    # And we break the loop.
                    break

            try:
                # We finally decode and return the response we got from the server.

                return response.decode()
            except UnicodeDecodeError:
                # We may get a decoding error.

                # We decode the response explicitly.
                # Note: Because we don't want to deal with other issue, we
                # decided to use `replace` in order to automatically replace
                # all non utf-8 encoded characters.
                return response.decode("utf-8", "replace")

        # The whois server is not given nor found.

        return result
