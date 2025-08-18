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
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

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
    :param int retries:
        The number of time we have to retry before raising an exception.
    :param bool certificate_validation:
        The state of the certificate validation.
    :param bool own_proxy_handler:
        Whether we should use our own proxy handler or not.
    :param dict proxies:
        The proxy to use.

        When :code:`own_proxy_handler` is set to :code:`True`, the proxies
        are expected to come from the global configuration.
        Otherwise, the proxies are expected to be a dictionary as defined
        by the requests library.
    """

    _url: Optional[str] = None
    _certificate_validation: bool = True
    _retries: int = 3
    _proxies: Optional[dict] = None

    _session = None
    _own_proxy_handler: Optional[bool] = True
    _proxies: Optional[dict] = None

    def __init__(
        self,
        url: Optional[str] = None,
        *,
        certificate_validation: bool = True,
        retries: int = 3,
        own_proxy_handler: Optional[bool] = True,
        proxies: Optional[dict] = None,
    ) -> None:
        if url is not None:
            self.url = url

        if proxies is not None:
            self.proxies = proxies

        self.retries = retries
        self.certificate_validation = bool(certificate_validation)
        self.own_proxy_handler = own_proxy_handler

    @property
    def session(self) -> requests.Session:
        """
        Provides the current state of the :code:`_session` attribute.
        """

        if not self._session:
            if self.own_proxy_handler:
                # pylint: disable=import-outside-toplevel
                from PyFunceble.query.requests.requester import Requester

                self._session = Requester(proxy_pattern=self.proxies)
            else:
                self._session = requests.Session()
                self._session.proxies = self.proxies

                retries = Retry(total=self.retries, backoff_factor=3)
                adapter = HTTPAdapter(max_retries=retries)

                self._session.mount("http://", adapter)
                self._session.mount("https://", adapter)

        return self._session

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

    @property
    def own_proxy_handler(self) -> Optional[bool]:
        """
        Provides the current state of the :code:`own_proxy_handler` attribute.
        """

        return self._own_proxy_handler

    @own_proxy_handler.setter
    def own_proxy_handler(self, value: bool) -> None:
        """
        Sets the state of the own proxy handler.

        :param value:
            The value to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._own_proxy_handler = value

        if value:
            # We force the recreation of the session.
            self._session = None

    def set_own_proxy_handler(self, value: bool) -> "DownloadHelper":
        """
        Sets the state of the own proxy handler.

        :param value:
            The value to set.
        """

        self.own_proxy_handler = value

        return self

    @property
    def proxies(self) -> Optional[dict]:
        """
        Provides the current state of the :code:`_proxies` attribute.
        """

        return self._proxies

    @proxies.setter
    def proxies(self, value: Optional[dict]) -> None:
        """
        Sets the proxy to use.

        :param value:
            The proxy to use.

            When :code:`own_proxy_handler` is set to :code:`True`, the proxies
            are expected to come from the global configuration.
            Otherwise, the proxies are expected to be a dictionary as defined
            by the requests library.

        :raise TypeError:
            When :code:`value` is not a :py:class:`dict`.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        self._proxies = value

        if value:
            # We force the recreation of the session.
            self._session = None

    def set_proxies(self, value: Optional[dict]) -> "DownloadHelper":
        """
        Sets the proxy to use.

        :param value:
            The proxy to use.

            When :code:`own_proxy_handler` is set to :code:`True`, the proxies
            are expected to come from the global configuration.
            Otherwise, the proxies are expected to be a dictionary as defined
            by the requests library.
        """

        self.proxies = value

        return self

    def download_text(
        self,
        *,
        destination: Optional[str] = None,
    ) -> str:
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

        try:
            req = self.session.get(self.url, verify=self.certificate_validation)

            if req.status_code == 200:
                response = req.text

                if destination and isinstance(destination, str):
                    FileHelper(destination).write(req.text, overwrite=True)

                return response

            raise PyFunceble.helpers.exceptions.UnableToDownload(
                f"{req.url} (retries: {self.retries} | status code: {req.status_code})"
            )
        except requests.exceptions.RequestException as exception:
            raise PyFunceble.helpers.exceptions.UnableToDownload(
                f"{self.url} (could not resolve?)"
            ) from exception
