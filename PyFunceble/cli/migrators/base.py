"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of our migrator classes.

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

from typing import Optional

from sqlalchemy.orm import Session

import PyFunceble.storage
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase


class MigratorBase:
    """
    Provides the base of all classes.
    """

    done: bool = False
    continuous_integration: Optional[ContinuousIntegrationBase] = None
    db_session: Optional[Session] = None

    _config_dir: Optional[str] = None
    print_action_to_stdout: bool = False

    def __init__(
        self, print_action_to_stdout: bool = False, *, config_dir: Optional[str] = None
    ) -> None:
        self.print_action_to_stdout = print_action_to_stdout

        if config_dir is not None:
            self._config_dir = config_dir
        else:
            self._config_dir = PyFunceble.storage.CONFIG_DIRECTORY

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        A method to be called (automatically) after the __init__ execution.
        """

    @property
    def config_dir(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_config_dir` attribute.
        """

        return self._config_dir

    @config_dir.setter
    def config_dir(self, value: str) -> None:
        """
        Sets the configuration directory.

        :param value:
            The value to set.

        :raise TypeError:
            When value is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._config_dir = value

    def set_config_dir(self, value: str) -> "MigratorBase":
        """
        Sets the configuration directory.

        :param value:
            The value to set.
        """

        self.config_dir = value

        return self

    def start(self) -> "MigratorBase":
        """
        Starts the migration.
        """

        raise NotImplementedError()
