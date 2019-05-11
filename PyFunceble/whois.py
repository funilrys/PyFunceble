# pylint:disable=line-too-long, too-few-public-methods
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the whois record request interface.

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

from socket import AF_INET, SOCK_STREAM
from socket import error as socket_error
from socket import socket
from socket import timeout as socket_timeout

from PyFunceble.referer import Referer


class Whois:
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

                # We share it.
                self.server = server
            else:
                # The server is not a str.

                # We raise an exception.
                raise ValueError("`server` must be a string.")
        else:
            # The server is not given or is None.

            # We get the server.
            self.server = Referer(self.subject).get()

        if timeout:
            # The timeout is given.

            if isinstance(timeout, int):
                # The timeout is an int

                # We share it.
                self.timeout = timeout
            elif timeout.isdigit():
                # The timeout is a str digit.

                # We convert it to int and share it.
                self.timeout = int(timeout)
            else:
                # The timeout is something we could not understand.

                # We eaise an exception.
                raise ValueError("`timeout` must be an integer or digit string.")

    def request(self):
        """
        Perform the WHOIS request.
        """

        result = None

        if self.server and self.subject:
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
