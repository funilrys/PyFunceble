"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our own requests handler

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import functools
import warnings
from typing import Optional, Union

import requests
import requests.exceptions
import urllib3.exceptions

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.dataset.user_agent import UserAgentDataset
from PyFunceble.query.requests.adapter.http import RequestHTTPAdapter
from PyFunceble.query.requests.adapter.https import RequestHTTPSAdapter


class Requester:
    """
    Provides our very own requests handler.
    """

    STD_VERIFY_CERTIFICATE: bool = False
    STD_TIMEOUT: float = 3.0

    urllib3_exceptions = urllib3.exceptions
    exceptions = requests.exceptions

    _timeout: float = 5.0
    _max_retries: int = 3
    _verify_certificate: bool = True

    session: Optional[requests.Session] = None

    def __init__(
        self,
        *,
        max_retries: Optional[int] = None,
        verify_certificate: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> None:
        if max_retries is not None:
            self.max_retries = max_retries

        if verify_certificate is not None:
            self.verify_certificate = verify_certificate
        else:
            self.guess_and_set_verify_certificate()

        if timeout is not None:
            self.timeout = timeout
        else:
            self.guess_and_set_timeout()

        self.session = self.get_session()

        warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    def recreate_session(func):  # pylint: disable=no-self-argument
        """
        Recreate a new session after executing the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if hasattr(self, "session") and isinstance(self.session, requests.Session):
                self.session = self.get_session()

            return result

        return wrapper

    def request_factory(verb: str):  # pylint: disable=no-self-argument
        """
        Provides a universal request factory.

        :param verb:
            The HTTP Verb to apply.
        """

        def request_method(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                # pylint: disable=no-member
                PyFunceble.facility.Logger.debug(
                    "Started %r request to %r with %r",
                    verb.upper(),
                    args[0],
                    kwargs,
                )
                req = getattr(self.session, verb.lower())(*args, **kwargs)

                PyFunceble.facility.Logger.debug(
                    "Finished %r request to %r with %r",
                    verb.upper(),
                    args[0],
                    kwargs,
                )

                return req

            return wrapper

        return request_method

    @property
    def max_retries(self) -> int:
        """
        Provides the current state of the :code:`_max_retries` attribute.
        """

        return self._max_retries

    @max_retries.setter
    @recreate_session
    def max_retries(self, value: int) -> None:
        """
        Sets the max retries value to apply to all subsequent requests.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`.
        :raise ValueError:
            When the given :code:`value` is less than :code:`1`.
        """

        if not isinstance(value, int):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        if value < 1:
            raise ValueError(f"<value> ({value!r}) should be less than 1.")

        self._max_retries = value

    def set_max_retries(self, value: int) -> "Requester":
        """
        Sets the max retries value to apply to all subsequent requests.

        :param value:
            The value to set.
        """

        self.max_retries = value

        return self

    @property
    def verify_certificate(self) -> bool:
        """
        Provides the current state of the :code:`_verify_certificate` attribute.
        """

        return self._verify_certificate

    @verify_certificate.setter
    @recreate_session
    def verify_certificate(self, value: bool) -> None:
        """
        Enable or disables the certificate validation.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> shoule be {bool}, {type(value)} given.")

        self._verify_certificate = value

    def set_verify_certificate(self, value: bool) -> "Requester":
        """
        Enable or disables the certificate validation.

        :param value:
            The value to set.
        """

        self.verify_certificate = value

        return self

    def guess_and_set_verify_certificate(self) -> "Requester":
        """
        Try to guess the value from the configuration and set it.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded() and bool(
            PyFunceble.storage.CONFIGURATION.verify_ssl_certificate
        ):
            self.set_verify_certificate(
                bool(PyFunceble.storage.CONFIGURATION.verify_ssl_certificate)
            )
        else:
            self.set_verify_certificate(self.STD_VERIFY_CERTIFICATE)

        return self

    @property
    def timeout(self) -> float:
        """
        Provides the current state of the :code:`_timeout` attribute.
        """

        return self._timeout

    @timeout.setter
    @recreate_session
    def timeout(self, value: Union[int, float]) -> None:
        """
        Enable or disables the certificate validation.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class`int` nor
            :py:class:`float`.
        :raise ValueError:
            Whent the given :code:`value` is less than `1`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> shoule be {int} or {float}, {type(value)} given.")

        if value < 1:
            raise ValueError("<value> should not be less than 1.")

        self._timeout = float(value)

    def set_timeout(self, value: Union[int, float]) -> "Requester":
        """
        Enable or disables the certificate validation.

        :param value:
            The value to set.
        """

        self.timeout = value

        return self

    def guess_and_set_timeout(self) -> "Requester":
        """
        Try to guess the value from the configuration and set it.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded() and bool(
            PyFunceble.storage.CONFIGURATION.lookup.timeout
        ):
            self.set_timeout(PyFunceble.storage.CONFIGURATION.lookup.timeout)
        else:
            self.set_timeout(self.STD_TIMEOUT)

        return self

    def guess_all_settings(self) -> "Requester":
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self

    def get_max_retries(self) -> int:
        """
        Provides the current value of :code:`max_retries`.
        """

        return self.max_retries

    def get_verify_certificate(self) -> bool:
        """
        Provides the current value of the certificate validation.
        """

        return self.verify_certificate

    def get_timeout(self) -> float:
        """
        Provides the currently set timetout.
        """

        return self.timeout

    def get_session(self) -> requests.Session:
        """
        Provides a new session.
        """

        session = requests.Session()

        session.verify = self.verify_certificate

        session.mount(
            "https://",
            RequestHTTPSAdapter(max_retries=self.max_retries, timeout=self.timeout),
        )
        session.mount(
            "http://",
            RequestHTTPAdapter(max_retries=self.max_retries, timeout=self.timeout),
        )

        custom_headers = {"User-Agent": UserAgentDataset().get_latest()}

        session.headers.update(custom_headers)

        return session

    @request_factory("GET")
    def get(self, *args, **kwargs) -> requests.Response:
        """
        Sends a GET request and get its response.
        """

    @request_factory("OPTIONS")
    def options(self, *args, **kwargs) -> requests.Response:
        """
        Sends am OPTIONS request and get its response.
        """

    @request_factory("HEAD")
    def head(self, *args, **kwargs) -> requests.Response:
        """
        Sends a HEAD request and get its response.
        """

    @request_factory("POST")
    def post(self, *args, **kwargs) -> requests.Response:
        """
        Sends a POST request and get its response.
        """

    @request_factory("PUT")
    def put(self, *args, **kwargs) -> requests.Response:
        """
        Sends a PUT request and get its response.
        """

    @request_factory("PATCH")
    def patch(self, *args, **kwargs) -> requests.Response:
        """
        Sends a PATCH request and get its response.
        """

    @request_factory("DELETE")
    def delete(self, *args, **kwargs) -> requests.Response:
        """
        Sends a DELETE request and get its response.
        """
