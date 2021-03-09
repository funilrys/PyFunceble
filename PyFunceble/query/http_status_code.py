"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our interface for getting the status code of a given subject.

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
import socket
from typing import Optional, Union

import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage


class HTTPStatusCode:
    """
    Provides an interface for the extration of the HTTP status code.
    """

    STD_UNKNOWN_STATUS_CODE: int = 99999999
    STD_TIMEOUT: float = 5.0
    STD_VERIFY_CERTIFICATE: bool = True
    STD_ALLOW_REDIRECTS: bool = False

    _subject: Optional[str] = None
    _timeout: float = 5.0
    _verify_certificate: bool = True
    _allow_redirects: bool = False

    def __init__(
        self,
        subject: Optional[str] = None,
        *,
        timeout: Optional[float] = None,
        verify_certificate: Optional[bool] = None,
        allow_redirects: Optional[bool] = None,
    ) -> None:
        if subject is not None:
            self.subject = subject

        if timeout is not None:
            self.timeout = timeout
        else:
            self.guess_and_set_timeout()

        if verify_certificate is not None:
            self.verify_certificate = verify_certificate
        else:
            self.guess_and_set_verify_certificate()

        if allow_redirects is not None:
            self.allow_redirects = allow_redirects
        else:
            self.allow_redirects = self.STD_ALLOW_REDIRECTS

        # Be sure that all settings are loaded proprely!!
        PyFunceble.factory.Requester.guess_all_settings()

    def ensure_subject_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the subject is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            if not isinstance(self.subject, str):
                raise TypeError(
                    f"<self.subject> should be {str}, {type(self.subject)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def subject(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    def subject(self, value: str) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._subject = value

    def set_subject(self, value: str) -> "HTTPStatusCode":
        """
        Sets the subject to work with.

        :param value:
            The subject to set.
        """

        self.subject = value

        return self

    @property
    def timeout(self) -> float:
        """
        Provides the current state of the :code:`_timeout` attribute.
        """

        return self._timeout

    @timeout.setter
    def timeout(self, value: Union[float, int]) -> None:
        """
        Sets the timeout to apply.

        :param value:
            The timeout to apply.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`
            nor :py:class:`float`.
        :raise ValueError:
            When the given :code:`value` is less than `1`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> should be {int} or {float}, {type(value)} given.")

        if value < 1:
            raise ValueError(f"<value> ({value!r}) should be less than 1.")

        self._timeout = float(value)

    def set_timeout(self, value: Union[float, int]) -> "HTTPStatusCode":
        """
        Sets the timeout to apply.

        :param value:
            The timeout to apply.
        """

        self.timeout = float(value)

        return self

    def guess_and_set_timeout(self) -> "HTTPStatusCode":
        """
        Tries to guess and set the timeout from the configuration.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.timeout = PyFunceble.storage.CONFIGURATION.lookup.timeout
        else:
            self.timeout = self.STD_TIMEOUT

        return self

    @property
    def verify_certificate(self) -> bool:
        """
        Provides the current state of the :code:`verify_certificate` attribute.
        """

        return self._verify_certificate

    @verify_certificate.setter
    def verify_certificate(self, value: bool) -> None:
        """
        Sets the value of the :code:`verify_certificate` variable.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._verify_certificate = value

    def set_verify_certificate(self, value: bool) -> "HTTPStatusCode":
        """
        Sets the value of the :code:`verify_certificate` variable.

        :param value:
            The value to set.
        """

        self.verify_certificate = value

        return self

    def guess_and_set_verify_certificate(self) -> "HTTPStatusCode":
        """
        Tries to guess and set the :code:`verify_certificate` attribute.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.verify_certificate = bool(
                PyFunceble.storage.CONFIGURATION["verify_ssl_certificate"]
            )
        else:
            self.verify_certificate = self.STD_VERIFY_CERTIFICATE

        return self

    @property
    def allow_redirects(self) -> bool:
        """
        Provides the current state of the :code:`_allow_redirects` attribute.
        """

        return self._allow_redirects

    @allow_redirects.setter
    def allow_redirects(self, value: bool) -> None:
        """
        Sets the value of the :code:`verify_certificate` variable.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._allow_redirects = value

    def set_allow_redirects(self, value: bool) -> "HTTPStatusCode":
        """
        Sets the value of the :code:`verify_certificate` variable.

        :param value:
            The value to set.
        """

        self.allow_redirects = value

        return self

    @ensure_subject_is_given
    def get_status_code(self) -> int:
        """
        Provides the status code.
        """

        try:
            req = PyFunceble.factory.Requester.head(
                self.subject,
                timeout=self.timeout,
                verify=self.verify_certificate,
                allow_redirects=self.allow_redirects,
            )

            return req.status_code
        except (
            PyFunceble.factory.Requester.exceptions.ConnectionError,
            PyFunceble.factory.Requester.exceptions.InvalidSchema,
            PyFunceble.factory.Requester.exceptions.InvalidURL,
            PyFunceble.factory.Requester.exceptions.MissingSchema,
            PyFunceble.factory.Requester.exceptions.Timeout,
            socket.timeout,
            PyFunceble.factory.Requester.urllib3_exceptions.InvalidHeader,
        ):
            pass

        return self.STD_UNKNOWN_STATUS_CODE
