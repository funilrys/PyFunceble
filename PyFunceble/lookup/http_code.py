"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the HTTP Code lookup interface.

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

import socket

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

        - :code:`ipv6`
    """

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
            # We are working with domain/IPv4.

            # We construct the element we have to get.
            # Note: As we may work with IP, we explicitly set the port we are
            # working with.
            self.subject = "http://%s:80" % subject
        elif subject_type in ["ipv6"]:
            # We are working with an IPv6

            # We construct the element we have to get.
            self.subject = "http://[%s]:80" % subject
        else:
            raise Exception("Unknow subject type.")

        # We share the subject type.
        self.subject_type = subject_type

        # We set the default status code.
        self.default = PyFunceble.HTTP_CODE.not_found_default

        user_agent = PyFunceble.engine.UserAgent().get()

        if user_agent:
            # The user-agent is given.

            # We append the user agent to the header we are going to parse with
            # the request.
            self.headers = {"User-Agent": user_agent}
        else:
            # The user-agent is not given or is empty.

            # We return an empty header.
            self.headers = {}

        PyFunceble.LOGGER.debug(f"Subject: {repr(self.subject)}")
        PyFunceble.LOGGER.debug(f"Headers:\n{self.headers}")

    def _get_it(self):  # pragma: no cover
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
                req = PyFunceble.REQUESTS.head(
                    self.subject,
                    timeout=PyFunceble.CONFIGURATION.timeout,
                    headers=self.headers,
                    verify=PyFunceble.CONFIGURATION.verify_ssl_certificate,
                    allow_redirects=False,
                )
            else:
                # We are not globally testing a URL.

                # We get the head of the constructed URL.
                req = PyFunceble.REQUESTS.head(
                    self.subject,
                    timeout=PyFunceble.CONFIGURATION.timeout,
                    headers=self.headers,
                    verify=PyFunceble.CONFIGURATION.verify_ssl_certificate,
                    allow_redirects=False,
                )

            PyFunceble.LOGGER.debug(f"Status Code: {req.status_code}")

            # And we try to get the status code.
            return req.status_code

        except (
            PyFunceble.REQUESTS.exceptions.ConnectionError,
            PyFunceble.REQUESTS.exceptions.InvalidSchema,
            PyFunceble.REQUESTS.exceptions.InvalidURL,
            PyFunceble.REQUESTS.exceptions.MissingSchema,
            PyFunceble.REQUESTS.exceptions.Timeout,
            socket.timeout,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            # If one of the listed exception is matched, that means that something
            # went wrong and we were unable to extract the status code.

            PyFunceble.LOGGER.exception()

            # We return None.
            return None

    def get(self):
        """
        Return the HTTP code status.

        :return: The matched and formatted status code.
        :rtype: str|int|None
        """

        if PyFunceble.HTTP_CODE.active:
            # The http status code extraction is activated.

            # We get the http status code.
            http_code = self._get_it()

            # We initiate a variable which will save the list of allowed
            # http status code.
            list_of_valid_http_code = []

            for codes in [
                PyFunceble.HTTP_CODE.list.up,
                PyFunceble.HTTP_CODE.list.potentially_down,
                PyFunceble.HTTP_CODE.list.potentially_up,
            ]:
                # We loop throught the list of http status code.

                # We extend the list of valid with the currently read
                # codes.
                list_of_valid_http_code.extend(codes)

            if http_code is None or http_code not in list_of_valid_http_code:
                # * The extracted http code is not in the list of valid http code.
                # or
                # * The extracted http code is equal to `None`.

                PyFunceble.LOGGER.info(
                    "Could not find http status code. "
                    f"Setting it it {repr(self.default)}"
                )

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
