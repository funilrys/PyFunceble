
# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the interface for url test.

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
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.helpers import Regex
from PyFunceble.http_code import HTTPCode
from PyFunceble.status import URLStatus


class URL:
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
            # The given url is not empty.

            # We initiate the element to test.
            to_test = url
        else:
            # The given url is empty.

            # We initiate the element to test from the globaly URl to test.
            to_test = PyFunceble.CONFIGURATION["URL"]

        if to_test.startswith("http"):
            # The element to test starts with http.

            try:
                # We initiate a regex which will match the domain or the url base.
                regex = r"((http:\/\/|https:\/\/)(.+?(?=\/)|.+?$))"

                # We extract the url base with the help of the initiated regex.
                domain = Regex(to_test, regex, return_data=True, rematch=True).match()[
                    2
                ]

                # We check if the url base is a valid domain.
                domain_status = ExpirationDate().is_domain_valid(domain)

                # We check if the url base is a valid IP.
                ip_status = ExpirationDate().is_ip_valid(domain)

                if domain_status or ip_status:
                    # * The url base is a valid domain.
                    # and
                    # * The url base is a valid IP.

                    # We return True.
                    return True
            except TypeError:
                pass

        # We return False.
        return False

    def get(self):  # pragma: no cover
        """
        Execute the logic behind the URL handling.
        """

        if self.is_url_valid():
            # The url is valid.

            # We initiate the HTTP status code.
            PyFunceble.CONFIGURATION.update(
                {"http_code": HTTPCode(full_url=True).get()}
            )

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

        # We handle and return the invalid down status.
        return URLStatus(PyFunceble.STATUS["official"]["invalid"]).handle()
