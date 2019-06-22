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

This submodule will provide HTTP Code extraction logic and interface.

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

import urllib3.exceptions as urllib3_exceptions
from urllib3 import disable_warnings

import PyFunceble


class HTTPCode:  # pylint: disable=too-few-public-methods
    """
    Get and return the HTTP code status of a given domain.

    :param str subject: The subject we are working with.

    :param subject _type:
        The type of the subject we are working with.
        Should be one of the following.

        - :code:`url`

        - :code:`domain`

        - :code:`file_url`

        - :code:`file_domain`
    """

    default = "*" * 3

    def __init__(self, subject, subject_type):  # pragma: no cover
        subject_type = subject_type.lower()

        if subject_type in ["url", "file_url"]:
            # We should work with full URL which actualy means that we have to get the
            # http status code from the URL we are currently testing.

            # We disable the urllib warning.
            disable_warnings(urllib3_exceptions.InsecureRequestWarning)

            # We initiate the element we have to get.
            self.subject = subject
        elif subject_type in ["domain", "file_domain"]:
            # We are working with domain.

            # We construct the element we have to get.
            # Note: As we may work with IP, we explicitly set the port we are
            # working with.
            self.subject = "http://%s:80" % subject
        else:
            raise Exception("Unknow subject type.")

        # We share the subject type.
        self.subject_type = subject_type

        if PyFunceble.CONFIGURATION["user_agent"]:
            # The user-agent is given.

            # We append the user agent to the header we are going to parse with
            # the request.
            self.headers = {"User-Agent": PyFunceble.CONFIGURATION["user_agent"]}
        else:
            # The user-agent is not given or is empty.

            # We return an empty header.
            self.headers = {}

    def _access(self):  # pragma: no cover
        """
        Get the HTTP code status.

        :return: The matched HTTP status code.
        :rtype: int|None
        """

        try:
            # We try to get the HTTP status code.

            if self.subject_type in ["url", "file_url"]:
                # We are globally testing a URL.

                # We get the head of the URL.
                req = PyFunceble.requests.head(
                    self.subject,
                    timeout=PyFunceble.CONFIGURATION["seconds_before_http_timeout"],
                    headers=self.headers,
                    verify=PyFunceble.CONFIGURATION["verify_ssl_certificate"],
                )
            else:
                # We are not globally testing a URL.

                # We get the head of the constructed URL.
                req = PyFunceble.requests.head(
                    self.subject,
                    timeout=PyFunceble.CONFIGURATION["seconds_before_http_timeout"],
                    headers=self.headers,
                )

            # And we try to get the status code.
            return req.status_code

        except (
            PyFunceble.requests.ConnectionError,
            PyFunceble.requests.exceptions.InvalidSchema,
            PyFunceble.requests.exceptions.InvalidURL,
            PyFunceble.requests.exceptions.MissingSchema,
            PyFunceble.requests.exceptions.Timeout,
            PyFunceble.socket.timeout,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            # If one of the listed exception is matched, that means that something
            # went wrong and we were unable to extract the status code.

            # We return None.
            return None

    def get(self):
        """
        Return the HTTP code status.

        :return: The matched and formatted status code.
        :rtype: str|int|None
        """

        if PyFunceble.HTTP_CODE["active"]:
            # The http status code extraction is activated.

            # We get the http status code.
            http_code = self._access()

            # We initiate a variable which will save the list of allowed
            # http status code.
            list_of_valid_http_code = []

            for codes in [
                PyFunceble.HTTP_CODE["list"]["up"],
                PyFunceble.HTTP_CODE["list"]["potentially_down"],
                PyFunceble.HTTP_CODE["list"]["potentially_up"],
            ]:
                # We loop throught the list of http status code.

                # We extend the list of valid with the currently read
                # codes.
                list_of_valid_http_code.extend(codes)

            if http_code not in list_of_valid_http_code or http_code is None:
                # * The extracted http code is not in the list of valid http code.
                # or
                # * The extracted http code is equal to `None`.

                # We return the default http code.
                return self.default

            # * The extracted http code is in the list of valid http code.
            # or
            # * The extracted http code is not equal to `None`.

            # We return the extracted http status code.
            return http_code

        # The http status code extraction is activated.

        # We return the default http code.
        return self.default
