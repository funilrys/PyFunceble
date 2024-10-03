"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our interface for quering the WHOIS Record of a given subject.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

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

import functools
import socket
from typing import Optional, Union

from PyFunceble.dataset.iana import IanaDataset
from PyFunceble.query.record.whois import WhoisQueryToolRecord
from PyFunceble.query.whois.converter.expiration_date import ExpirationDateExtractor
from PyFunceble.query.whois.converter.registrar import RegistarExtractor

# pylint: disable=protected-access


class WhoisQueryTool:
    """
    Provides the interface to get the WHOIS record of a given subject.
    """

    BUFFER_SIZE: int = 4096
    STD_PORT: int = 43

    expiration_date_extractor: Optional[ExpirationDateExtractor] = None
    registrar_extractor: Optional[RegistarExtractor] = None
    iana_dataset: Optional[IanaDataset] = None

    _subject: Optional[str] = None
    _server: Optional[str] = None
    _query_timeout: float = 5.0
    _expiration_date: Optional[str] = None
    _record: Optional[str] = None
    _registrar: Optional[str] = None

    lookup_record: Optional[WhoisQueryToolRecord] = None

    def __init__(
        self,
        subject: Optional[str] = None,
        *,
        server: Optional[str] = None,
        query_timeout: Optional[float] = None,
    ) -> None:
        self.registrar_extractor = RegistarExtractor()
        self.expiration_date_extractor = ExpirationDateExtractor()
        self.iana_dataset = IanaDataset()

        if subject is not None:
            self.subject = subject

        if server is not None:
            self.server = server

        if query_timeout is not None:
            self.set_query_timeout(query_timeout)

    def ensure_subject_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the subject is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Just safety.
            if not isinstance(self.subject, str):
                raise TypeError(
                    f"<self.subject> should be {str}, {type(self.subject)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def update_lookup_record(func):  # pylint: disable=no-self-argument
        """
        Ensures that a clean record is generated after the execution of
        the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.lookup_record is None or self.subject != self.lookup_record.subject:
                self.lookup_record = WhoisQueryToolRecord(port=self.STD_PORT)
                self.lookup_record.subject = self.subject

            if self.query_timeout != self.lookup_record.query_timeout:
                self.lookup_record.query_timeout = self.query_timeout

            if self.server != self.lookup_record.server:
                self.lookup_record.server = self.server

            if self._expiration_date != self.lookup_record.expiration_date:
                self.lookup_record.expiration_date = self._expiration_date

            if self._registrar != self.lookup_record.registrar:
                self.lookup_record.registrar = self._registrar

            return result

        return wrapper

    def reset_record(func):  # pylint: disable=no-self-argument
        """
        Resets the record before executing the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.lookup_record:
                self.lookup_record.record = self._record = None
                self.lookup_record.expiration_date = self._expiration_date = None
                self.lookup_record.registrar = self._registrar = None

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def query_record(func):  # pylint: disable=no-self-argument
        """
        Queries the record before executing the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## It just works.
            if not self.lookup_record or self.lookup_record.record is None:
                self.query()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def subject(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    @reset_record
    @update_lookup_record
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

    def set_subject(self, value: str) -> "WhoisQueryTool":
        """
        Sets the subject to work with.

        :param value:
            The subject to set.
        """

        self.subject = value

        return self

    @property
    def server(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_server` attribute.
        """

        return self._server

    @server.setter
    @reset_record
    @update_lookup_record
    def server(self, value: str) -> None:
        """
        Sets the server to communicate with.

        :param value:
            The server to work with.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._server = value

    def set_server(self, value: str) -> "WhoisQueryTool":
        """
        Sets the server to communicate with.

        :param value:
            The server to work with.
        """

        self.server = value

        return self

    @property
    def query_timeout(self) -> float:
        """
        Provides the current state of the :code:`_query_timeout` attribute.
        """

        return self._query_timeout

    @query_timeout.setter
    def query_timeout(self, value: Union[float, int]) -> None:
        """
        Sets the query_timeout to apply.

        :param value:
            The query_timeout to apply.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`
            nor :py:class:`float`.
        :raise ValueError:
            When the given :code:`value` is less than `1`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> should be {int} or {float}, {type(value)} given.")

        if value < 0:
            raise ValueError(f"<value> ({value!r}) should be less than 0.")

        self._query_timeout = float(value)

    def set_query_timeout(self, value: Union[float, int]) -> "WhoisQueryTool":
        """
        Sets the query_timeout to apply.

        :param value:
            The query_timeout to apply.
        """

        self.query_timeout = value

        return self

    @property
    @query_record
    @update_lookup_record
    def expiration_date(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_expiration_date` attribute.
        """

        if self.lookup_record.record:
            self._expiration_date = self.expiration_date_extractor.set_data_to_convert(
                self.lookup_record.record
            ).get_converted()

        return self._expiration_date

    @property
    @query_record
    def record(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_record` attribute.
        """

        return self.lookup_record.record

    @property
    @query_record
    @update_lookup_record
    def registrar(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_registrar` attribute.
        """

        if self.lookup_record.record:
            self._registrar = self.registrar_extractor.set_data_to_convert(
                self.lookup_record.record
            ).get_converted()

        return self._registrar

    @ensure_subject_is_given
    def get_whois_server(
        self,
    ) -> Optional[str]:  # pragma: no cover ## Test the underlying method instead.
        """
        Provides the whois server to work with.
        """

        if self.subject.endswith("."):
            extension = self.subject[:-1]
        else:
            extension = self.subject

        extension = extension[extension.rfind(".") + 1 :]

        return self.iana_dataset.get_whois_server(extension)

    @update_lookup_record
    def get_lookup_record(
        self,
    ) -> Optional[WhoisQueryToolRecord]:
        """
        Provides the current query record.
        """

        return self.lookup_record

    @ensure_subject_is_given
    @update_lookup_record
    def query(
        self,
    ) -> str:  # pragma: no cover ## The effect of the response of this method
        ## are more important.
        """
        Queries the WHOIS record and return the current object.
        """

        if self.lookup_record.record is None:
            if not self.server:
                whois_server = self.get_whois_server()
            else:
                whois_server = self.server

            if whois_server:
                self.lookup_record.server = whois_server
                self.lookup_record.query_timeout = self.query_timeout

                req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                req.settimeout(self.query_timeout)

                try:
                    req.connect((whois_server, self.STD_PORT))
                    req.send(f"{self.subject}\r\n".encode())

                    response = "".encode()

                    while True:
                        try:
                            data = req.recv(self.BUFFER_SIZE)
                        except (ConnectionResetError, socket.timeout):
                            break

                        response += data

                        if not data:
                            break

                    req.close()

                    try:
                        self.lookup_record.record = self._record = response.decode()
                    except UnicodeDecodeError:
                        # Note: Because we don't want to deal with other issue, we
                        # decided to use `replace` in order to automatically replace
                        # all non utf-8 encoded characters.
                        self.lookup_record.record = self._record = response.decode(
                            "utf-8", "replace"
                        )
                except socket.error:
                    pass

            if self.lookup_record.record is None or not self.lookup_record.record:
                self.lookup_record.record = self._record = ""
                self.lookup_record.expiration_date = self._expiration_date = ""
                self.lookup_record.registrar = self._record = ""
            else:
                self.lookup_record.expiration_date = self.expiration_date
                self.lookup_record.registrar = self.registrar

        return self.lookup_record.record

    @query_record
    def get_record(
        self,
    ) -> Optional[str]:  # pragma: no cover ## Just a dataclass attribute.
        """
        Provides the current record.

        Side Effect:
            The record will be queried if it is non existent.
        """

        return self.lookup_record.record
