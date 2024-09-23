"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the environment variable helpers.

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

import logging
import os
from typing import Any, Optional, Union

import dotenv


class EnvironmentVariableHelper:
    """
    Simplify the way we work with environment variable.

    :param str name:
        The name of the environment variable to work with.
    """

    _name: Optional[str] = None
    _env_file_path: Optional[str] = None

    def __init__(self, name: Optional[str] = None, env_file_path: Optional[str] = None):
        if name is not None:
            self.name = name

        if env_file_path is not None:
            self.env_file_path = env_file_path

        logging.getLogger("dotenv").setLevel(logging.CRITICAL)

    @property
    def name(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_name` attribute.
        """

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the name of the environment variable to work with.

        :param value:
            The name to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`str`
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._name = value

    def set_name(self, value: str) -> "EnvironmentVariableHelper":
        """
        Sets the name of the environment variable to work with.

        :param value:
            The name to set.
        """

        self.name = value

        return self

    @property
    def env_file_path(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_env_file_path` attribute.
        """

        return self._env_file_path

    @env_file_path.setter
    def env_file_path(self, value: str) -> None:
        """
        Sets the location of the environment file to work with.

        :param value:
            The name to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`str`
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._env_file_path = value

    def set_env_file_path(self, value: str) -> "EnvironmentVariableHelper":
        """
        Sets the location of the environment file to work with.

        :param value:
            The name to set.
        """

        self.env_file_path = value

        return self

    def exists(self) -> bool:
        """
        Checks if the given environment variable name exists.
        """

        return self.name in os.environ

    def get_value(self, *, default: Optional[Any] = None) -> Union[Any, str]:
        """
        Returns the value of the given environment variable name
        (if exists.)

        :param default: The default value to return.
        """

        if self.exists():
            return os.environ[self.name]

        return default

    def get_value_from_env_file(
        self, *, default: Optional[Any] = None
    ) -> Union[Any, str]:
        """
        Returns the value of the given environment variable if it exists
        in the given file path.
        """

        read_value = dotenv.get_key(self.env_file_path, self.name)

        if read_value is not None:
            return read_value
        return default

    def set_value(self, value: str) -> "EnvironmentVariableHelper":
        """
        Sets the given value into the given environment variable name.

        :param str value:
            The value to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`value`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        os.environ[self.name] = value

        return self

    def set_value_in_env_file(self, value: str) -> "EnvironmentVariableHelper":
        """
        Sets the given value and save it into the given dotenv file.

        .. warning::
            This method also set the environment variable from the current
            environment.

        :param value:
            The value to set.
        """

        self.set_value(value)

        dotenv.set_key(self.env_file_path, self.name, value)

        return self

    def delete(self) -> "EnvironmentVariableHelper":
        """
        Deletes the given environment variable if exists.
        """

        if self.exists():
            del os.environ[self.name]

        return self

    def delete_from_env_file(self) -> "EnvironmentVariableHelper":
        """
        Deletes the given environment file from the given dotenv file.

        .. warning::
            This method also delete the environment variable from the current
            environment.
        """

        self.delete()

        dotenv.unset_key(self.env_file_path, self.name)

        return self
