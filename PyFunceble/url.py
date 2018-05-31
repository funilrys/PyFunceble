
"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the interface for url test.


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
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.helpers import Regex
from PyFunceble.http_code import HTTPCode
from PyFunceble.status import URLStatus


class URL(object):
    """
    This method will manage everything aroud the tests of urls.
    """

    @classmethod
    def is_url_valid(cls, url=None):
        """
        Check if the domain of the given URL is valid.

        Argument:
            - url: str
                The url to test.

        Returns: bool
            - True: is valid.
            - False: is invalid.
        """

        if url:
            to_test = url
        else:
            to_test = PyFunceble.CONFIGURATION["URL"]

        if to_test.startswith("http"):
            regex = r"((http:\/\/|https:\/\/)(.+?(?=\/)|.+?$))"
            domain = Regex(to_test, regex, return_data=True, rematch=True).match()[2]

            domain_status = ExpirationDate().is_domain_valid(domain)
            ip_status = ExpirationDate().is_domain_valid(domain)

            if domain_status or ip_status:
                return True

        return False

    def get(self):  # pragma: no cover
        """
        Execute the logic behind the URL handling.
        """

        if self.is_url_valid():
            PyFunceble.CONFIGURATION.update(
                {"http_code": HTTPCode(full_url=True).get()}
            )

            active_list = []
            active_list.extend(PyFunceble.HTTP_CODE["list"]["potentially_up"])
            active_list.extend(PyFunceble.HTTP_CODE["list"]["up"])

            inactive_list = []
            inactive_list.extend(PyFunceble.HTTP_CODE["list"]["potentially_down"])
            inactive_list.append("*" * 3)

            if PyFunceble.CONFIGURATION["http_code"] in active_list:
                return URLStatus(PyFunceble.STATUS["official"]["up"]).handle()

            elif PyFunceble.CONFIGURATION["http_code"] in inactive_list:
                return URLStatus(PyFunceble.STATUS["official"]["down"]).handle()

        return URLStatus(PyFunceble.STATUS["official"]["invalid"]).handle()
