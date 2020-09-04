"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the download helpers.

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

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..exceptions import NoInternetConnection, UnableToDownload
from .file import File


class Download:
    """
    Simplification of the downloads.

    :param str url:
        The url to download.
    :param bool verify_certificate:
        Allows/Disallows the certificate verification.
    :param int retry:
        The number of time we have to retry before raising an exception.
    """

    def __init__(self, url, verify_certificate=True, retry=3):
        if not isinstance(url, str):
            raise TypeError(f"<url> must be {str}, {type(url)} given.")

        if not isinstance(verify_certificate, bool):
            raise TypeError(
                f"<verify_certificate> must be {bool}, {type(verify_certificate)} given."
            )

        self.url = url
        self.certificate_verification = verify_certificate

        if not isinstance(retry, int):
            raise TypeError(f"<retry> should be {int}, {type(retry)} given.")

        if retry <= 0:
            retry = 1

        self.retry = retry

    def text(self, destination=None):
        """
        Download the body of the given url.

        .. note::
            if :code:`destination` is set to :code:`None`,
            we only return the output.

            Otherwise, we save the output into the given
            destination, but we also return the output.

        :param str destination: The download destination.
        :rtype: str:
        :raise Exception: When the status code is not 200.
        :raise NoInternetConnection: When no connection could be made.
        """

        session = requests.Session()

        retries = Retry(total=self.retry, backoff_factor=3)
        adapter = HTTPAdapter(max_retries=retries)

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        try:
            req = session.get(self.url, verify=self.certificate_verification)

            if req.status_code == 200:
                response = req.text

                if destination and isinstance(destination, str):
                    File(destination).write(req.text, overwrite=True)

                return response

            raise UnableToDownload(
                f"{req.url} (retries: {self.retry} | status code: {req.status_code})"
            )
        except requests.exceptions.ConnectionError as exception:
            raise NoInternetConnection(self.url) from exception
