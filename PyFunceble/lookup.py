#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the lookup interface.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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

import PyFunceble
from PyFunceble import socket


class Lookup(object):
    """
    This class can be used to NSLOOKUP or WHOIS lookup.
    """

    @classmethod
    def nslookup(cls):
        """
        Implementation of UNIX nslookup.
        """

        try:
            try:
                try:
                    socket.getaddrinfo(
                        PyFunceble.CONFIGURATION["domain"], 80, 0, 0, socket.IPPROTO_TCP
                    )
                except OSError:
                    return False

            except socket.herror:  # pragma: no cover
                return False

            return True

        except socket.gaierror:  # pragma: no cover
            return False

    @classmethod
    def whois(cls, whois_server, domain=None, timeout=None):  # pragma: no cover
        """
        Implementation of UNIX whois.

        Arguments:
            - whois_server: str
                The whois server to use to get the record.
            - domain: str
                The domain to get the whois record from.
            - timeout: int
                The timeout to apply to the request.

        Returns: None or str
            None: No whois record catched.
            str: The whois record.
        """

        if domain is None:
            domain = PyFunceble.CONFIGURATION["domain"]

        if timeout is None:
            timeout = PyFunceble.CONFIGURATION["seconds_before_http_timeout"]

        if whois_server:

            req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if PyFunceble.CONFIGURATION["seconds_before_http_timeout"] % 3 == 0:
                req.settimeout(timeout)
            else:
                req.settimeout(3)

            try:
                req.connect((whois_server, 43))
            except socket.error:
                return None

            req.send((domain + "\r\n").encode())
            response = b""

            while True:
                try:
                    try:
                        data = req.recv(4096)
                    except ConnectionResetError:
                        req.close()

                        return None

                except socket.timeout:
                    req.close()

                    return None

                response += data
                if not data:
                    break

            req.close()

            try:
                return response.decode()

            except UnicodeDecodeError:
                return response.decode("utf-8", "replace")

        return None
