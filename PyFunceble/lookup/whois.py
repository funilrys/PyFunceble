"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the WHOIS lookup interface.

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

from random import choice
from socket import AF_INET, SOCK_STREAM
from socket import error as socket_error
from socket import socket
from socket import timeout as socket_timeout

import PyFunceble

from .referer import Referer


class WhoisLookup:
    """
    Implementation of the UNIX `whois` command.

    :param str subject: The subject we are working with.

    :param str server:
        The WHOIS server we are working with.

        .. note::
            If :code:`None` is given, we look for the best one.

    :param int timeout:
        The timeout to apply.

        .. warning::
            The timeout must be a modulo of :code:`3`.
    """

    # Set the port we are going to working with.
    universal_port = 43
    # Set the size of the buffer which extrating
    # the expiration date.
    buffer_size = 4096

    def __init__(self, subject, server=None, timeout=3):
        if subject:
            # The subject is not empty nor None.

            if isinstance(subject, str):
                # The subject is a str.

                # We share it.
                self.subject = subject
            else:
                # The subject is not a str.

                # We raise an exception.
                raise ValueError("expected {0}".format(type(str)))

        if server is not None:
            # The server is given.

            if isinstance(server, str):
                # The server is a str.

                resolved_server = PyFunceble.DNSLOOKUP.a_record(server)

                try:
                    # We share it.
                    self.server = choice(resolved_server)
                except (IndexError, TypeError):
                    self.server = None
            else:
                # The server is not a str.

                # We raise an exception.
                raise ValueError("`server` must be a string.")
        else:
            # The server is not given or is None.

            # We get the server.
            self.server = Referer(self.subject).get()[0]

        if timeout:
            # The timeout is given.

            if isinstance(timeout, (int, float)):
                # The timeout is an int

                # We share it.
                self.timeout = float(timeout)
            else:
                # The timeout is something we could not understand.

                # We eaise an exception.
                raise ValueError("`timeout` must be an integer or float.")

    def request(self):  # pragma: no cover
        """
        Perform the WHOIS request.
        """

        result = None

        if self.server and self.subject:
            # A server was found or is given.

            # We initiate a socket for the request.
            req = socket(AF_INET, SOCK_STREAM)

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

                # Eerything goes right.

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
