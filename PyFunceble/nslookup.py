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

This submodule will provide the nslookup interface.

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

from socket import IPPROTO_TCP, gaierror, getaddrinfo, gethostbyaddr, herror

from PyFunceble.check import Check


class NSLookup:  # pylint: disable=too-few-public-methods
    """
    Implementation of the UNIX :code:`nslookup` command.

    :param str subject: The subject we are working with.
    """

    def __init__(self, subject):
        if subject:
            if isinstance(subject, str):
                self.subject = subject
            else:
                raise ValueError("{0} expected".format(type(subject)))

    def request(self):
        """
        Perform the NS request.

        :return:
            A dict with following index if an IPv4 is given.

                ::

                    {
                        "addr_info" : []
                    }

            A dict with following index for everything else.

                ::

                    {
                        "hostname": "xx",
                        "aliases": [],
                        "ips": []
                    }

        :rtype: dict
        """

        result = {}

        try:
            if not Check(self.subject).is_ipv4():
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
