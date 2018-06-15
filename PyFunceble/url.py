
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
            ip_status = ExpirationDate().is_ip_valid(domain)

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
