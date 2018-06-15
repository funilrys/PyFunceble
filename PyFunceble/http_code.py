#!/usr/bin/env python3

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

This submodule will provide HTTP Code extraction logic and interface.

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
import urllib3.exceptions as urllib3_exceptions

# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import requests, socket


class HTTPCode(object):  # pylint: disable=too-few-public-methods
    """
    Get and return the HTTP code status of a given domain.

    Argument:
        - full_url: bool
            - False: We check only in a domain mode environnment.
            - True: We check in a www environnment.

    """

    def __init__(self, full_url=False):  # pragma: no cover
        self.full_url = full_url

        if full_url:
            self.to_get = PyFunceble.CONFIGURATION["URL"]
        else:
            self.to_get = "http://%s:80" % PyFunceble.CONFIGURATION["domain"]

    def _access(self):  # pragma: no cover
        """
        Get the HTTP code status.

        Returns: int or None
            int: The catched HTTP status_code.
            None: Nothing catched.
        """

        try:
            req = requests.head(
                self.to_get,
                timeout=PyFunceble.CONFIGURATION["seconds_before_http_timeout"],
            )

            return req.status_code

        except (
            requests.exceptions.InvalidURL,
            socket.timeout,
            requests.exceptions.Timeout,
            requests.ConnectionError,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            return None

    def get(self):
        """
        Return the HTTP code status.

        Returns: str or int
            str: if no status_code is catched.
            int: the status_code.
        """
        if PyFunceble.HTTP_CODE["active"]:
            http_code = self._access()
            list_of_valid_http_code = []

            for codes in [
                PyFunceble.HTTP_CODE["list"]["up"],
                PyFunceble.HTTP_CODE["list"]["potentially_down"],
                PyFunceble.HTTP_CODE["list"]["potentially_up"],
            ]:
                list_of_valid_http_code.extend(codes)

            if http_code not in list_of_valid_http_code or http_code is None:
                return "*" * 3

            return http_code

        return None
