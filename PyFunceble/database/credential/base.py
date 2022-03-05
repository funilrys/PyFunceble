"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our credential holders.

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

import functools
import os
from typing import List, Optional

import PyFunceble.storage
from PyFunceble.helpers.file import FileHelper


class CredentialBase:
    """
    Provides the base of all our credential holder.
    """

    STD_HOST: str = "localhost"
    STD_PORT: int = 3306
    STD_NAME: str = PyFunceble.storage.PROJECT_NAME.lower()
    STD_USERNAME: str = PyFunceble.storage.PROJECT_NAME.lower()
    STD_PASSWORD: str = f"{PyFunceble.storage.PROJECT_NAME}:15_93le"
    STD_CHARSET: str = "utf8mb4"

    VAR2ENV: dict = {
        "host": "PYFUNCEBLE_DB_HOST",
        "port": "PYFUNCEBLE_DB_PORT",
        "name": "PYFUNCEBLE_DB_NAME",
        "username": "PYFUNCEBLE_DB_USERNAME",
        "password": "PYFUNCEBLE_DB_PASSWORD",
        "charset": "PYFUNCEBLE_DB_CHARSET",
    }
    """
    Maps our credential variable with environment variable.
    """

    dotenv_locations: List[str] = []
    """
    Provides the location of the dotenv to work with.

    .. warning::
        The order is important. The last one in the list will be taken as
        default if everything else is not found in the filesystem.
    """

    protocol: Optional[str] = None

    _host: Optional[str] = None
    _port: Optional[int] = None
    _name: Optional[str] = None
    _username: Optional[str] = None
    _password: Optional[str] = None
    _charset: Optional[str] = None

    def __init__(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        name: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        charset: Optional[str] = None,
    ) -> None:

        if host is not None:
            self.host = host
        else:
            self.host = self.STD_HOST

        if port is not None:
            self.port = port
        else:
            self.port = self.STD_PORT

        if name is not None:
            self.name = name
        else:
            self.name = self.STD_NAME

        if username is not None:
            self.username = username
        else:
            self.username = self.STD_USERNAME

        if password is not None:
            self.password = password
        else:
            self.password = self.STD_PASSWORD

        if charset is not None:
            self.charset = charset
        else:
            self.charset = self.STD_CHARSET

        self.dotenv_locations = [
            os.path.realpath(PyFunceble.storage.ENV_FILENAME),
            os.path.join(
                PyFunceble.storage.CONFIG_DIRECTORY, PyFunceble.storage.ENV_FILENAME
            ),
        ]

    def ensure_protocol_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the protocol is given before launching the decorated
        method.

        :raise ValueError:
            When the :code:`protocol` is not given.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.protocol:
                raise ValueError("<self.protocol> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def host(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_host` attribute.
        """

        return self._host

    @host.setter
    def host(self, value: str) -> None:
        """
        Sets the hosts to interact with.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._host = value

    def set_host(self, value: str) -> "CredentialBase":
        """
        Sets the hosts to interact with.

        :param value:
            The value to set.
        """

        self.host = value

        return self

    @property
    def port(self) -> Optional[int]:
        """
        Provides the current state of the :code:`_port` attribute.
        """

        return self._port

    @port.setter
    def port(self, value: int) -> None:
        """
        Sets the port to interact with.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`.
        """

        if not isinstance(value, int):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        self._port = value

    def set_port(self, value: int) -> "CredentialBase":
        """
        Sets the port to interact with.

        :param value:
            The value to set.
        """

        self.port = value

        return self

    @property
    def name(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_name` attribute.
        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the name of the database to interact with.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._name = value

    def set_name(self, value: str) -> "CredentialBase":
        """
        Sets the name of the database to interact with.

        :param value:
            The value to set.
        """

        self.name = value

        return self

    @property
    def username(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_username` attribute.
        """

        return self._username

    @username.setter
    def username(self, value: str) -> None:
        """
        Sets the username to use to authenticate ourselves.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._username = value

    def set_username(self, value: str) -> "CredentialBase":
        """
        Sets the username to use to authenticate ourselves.

        :param value:
            The value to set.
        """

        self.username = value

        return self

    @property
    def password(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_password` attribute.
        """

        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """
        Sets the password to use to authenticate ourselves.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._password = value

    def set_password(self, value: str) -> "CredentialBase":
        """
        Sets the password to use to authenticate ourselves.

        :param value:
            The value to set.
        """

        self.host = value

        return self

    @property
    def charset(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_charset` attribute.
        """

        return self._charset

    @charset.setter
    def charset(self, value: str) -> None:
        """
        Sets the charset to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._charset = value

    def set_charset(self, value: str) -> "CredentialBase":
        """
        Sets the charset to use.

        :param value:
            The value to set.
        """

        self.charset = value

        return self

    @ensure_protocol_is_given
    def get_uri(self) -> str:
        """
        Provides the SQLAlchemy URI.
        """

        if self.host.startswith("/"):
            return (
                f"{self.protocol}://{self.username}:{self.password}"
                f"@localhost/{self.name}?unix_socket={self.host}"
                f"&charset={self.charset}"
            )

        return (
            f"{self.protocol}://{self.username}:{self.password}"
            f"@{self.host}/{self.name}"
            f"?charset={self.charset}"
        )

    def get_dot_env_file(self) -> str:
        """
        Provides the dotenv file to work with.
        """

        file_helper = FileHelper()

        for file in self.dotenv_locations:
            if file_helper.set_path(file).exists():
                return file_helper.path

        return self.dotenv_locations[-1]
