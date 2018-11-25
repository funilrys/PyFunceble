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

This submodule will provide the interface for URL testing.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


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
# pylint: enable=line-too-long

import PyFunceble
from PyFunceble.check import Check
from PyFunceble.http_code import HTTPCode
from PyFunceble.status import URLStatus


class URL:  # pylint: disable=too-few-public-methods
    """
    Manage everything around the URL testing.
    """

    @classmethod
    def get(cls):  # pragma: no cover
        """
        Execute the logic behind the URL handling.

        :return: The status of the URL.
        :rtype: str
        """

        if Check().is_url_valid() or PyFunceble.CONFIGURATION["local"]:
            # * The url is valid.
            # or
            # * We are testing in/for a local or private network.

            if "current_test_data" in PyFunceble.CONFIGURATION:
                PyFunceble.CONFIGURATION["current_test_data"][
                    "url_syntax_validation"
                ] = True

            # We initiate the HTTP status code.
            PyFunceble.CONFIGURATION.update({"http_code": HTTPCode().get()})

            # We initiate the list of active status code.
            active_list = []
            active_list.extend(PyFunceble.HTTP_CODE["list"]["potentially_up"])
            active_list.extend(PyFunceble.HTTP_CODE["list"]["up"])

            # We initiate the list of inactive status code.
            inactive_list = []
            inactive_list.extend(PyFunceble.HTTP_CODE["list"]["potentially_down"])
            inactive_list.append("*" * 3)

            if PyFunceble.CONFIGURATION["http_code"] in active_list:
                # The extracted HTTP status code is in the list of active list.

                # We handle and return the up status.
                return URLStatus(PyFunceble.STATUS["official"]["up"]).handle()

            if PyFunceble.CONFIGURATION["http_code"] in inactive_list:
                # The extracted HTTP status code is in the list of inactive list.

                # We handle and return the down status.
                return URLStatus(PyFunceble.STATUS["official"]["down"]).handle()

        # The extracted HTTP status code is not in the list of active nor invalid list.

        if "current_test_data" in PyFunceble.CONFIGURATION:
            # The end-user want more information whith his test.

            # We update the url_syntax_validation index.
            PyFunceble.CONFIGURATION["current_test_data"][
                "url_syntax_validation"
            ] = False

        # We handle and return the invalid down status.
        return URLStatus(PyFunceble.STATUS["official"]["invalid"]).handle()
