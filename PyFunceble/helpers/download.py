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
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import PyFunceble.helpers.exceptions
from PyFunceble.helpers.file import FileHelper


class DownloadHelper:
    """
    Simplification of the downloads.

    :param str url:
    :param int retry:
        The number of time we have to retry before raising an exception.
    """

    _url: Optional[str] = None
    _certificate_validation: bool = True
    _retries: int = 3

    def __init__(
        self,
        url: Optional[str] = None,
        *,
        certificate_validation: bool = True,
        retries: int = 3,
    ) -> None:
        if url:
            self.url = url

        if certificate_validation:
            self.certificate_validation = certificate_validation

        if retries:
            self.retries = retries

    @property
    def url(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_url` attribute.
        """

        return self._url

    @url.setter
    def url(self, value: str) -> None:
        """
        Sets the url to work with.

        :param value:
            The URL to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._url = value

    def set_url(self, value: str) -> "DownloadHelper":
        """
        Sets the url to work with.

        :param value:
            The URL to set.
        """

        self.url = value

        return self

    @property
    def certificate_validation(self) -> bool:
        """
        Provides the current state of the :code:`certificate_validation`
        attribute.
        """

        return self._certificate_validation

    @certificate_validation.setter
    def certificate_validation(self, value: bool) -> None:
        """
        Sets the value of the certificate validation.

        :param value:
            The value to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`bool`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._certificate_validation = value

    def set_certificate_validation(self, value: bool) -> "DownloadHelper":
        """
        Sets the value of the certificate validation.

        :param value:
            The value to set.
        """

        self.certificate_validation = value

        return self

    @property
    def retries(self) -> int:
        """
        Provides the current state of the :code:`_retries` attributes.
        """

        return self._retries

    @retries.setter
    def retries(self, value: int) -> None:
        """
        Sets the number of retries we are allowed to perform before raising an
        exception.

        :param value:
            The number of retry to apply.i

        :raise TypeError:
            When :code:`value` is not a :py:class:`int`.
        :raise ValueError:
            When :code:`value` is lower than :code:`0`.
        """

        if not isinstance(value, int):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        if value <= 0:
            raise ValueError("<value> should greater than zero.")

        self._retries = value

    def set_retries(self, value: int) -> "DownloadHelper":
        """
        Sets the number of retries we are allowed to perform before raising an
        exception.

        :param value:
            The number of retry to apply.i
        """

        self.retries = value

        return self

    def download_text(self, *, destination: Optional[str] = None) -> str:
        """
        Download the body of the set url.

        .. note::
            if :code:`destination` is set to :code:`None`,
            we only return the output.

            Otherwise, we save the output into the given
            destination, but we also return the output.

        :param destination: The download destination.

        :raise UnableToDownload: When could not unable to download the URL.
        """

        session = requests.Session()

        retries = Retry(total=self.retries, backoff_factor=3)
        adapter = HTTPAdapter(max_retries=retries)

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        req = session.get(self.url, verify=self.certificate_validation)

        if req.status_code == 200:
            response = req.text

            if destination and isinstance(destination, str):
                FileHelper(destination).write(req.text, overwrite=True)

            adapter.close()
            req.close()
            return response

        adapter.close()
        session.close()
        raise PyFunceble.helpers.exceptions.UnableToDownload(
            f"{req.url} (retries: {self.retries} | status code: {req.status_code})"
        )
