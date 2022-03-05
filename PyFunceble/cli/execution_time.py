"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the generation of the execution time.

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

# pylint: disable=too-many-lines

import datetime
import functools
from typing import Any, Optional

import PyFunceble.cli.storage
import PyFunceble.facility


class ExecutionTime:
    """
    Provides the interface for the execution time.

    :param authorized:
        The authorization to run.
    """

    STD_AUTHORIZED: bool = False

    _authorized: bool = False

    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None

    def __init__(
        self,
        authorized: Optional[bool] = None,
    ) -> None:
        if authorized is not None:
            self.authorized = authorized
        else:
            self.guess_and_set_authorized()

    def execute_if_authorized(default: Any = None):  # pylint: disable=no-self-argument
        """
        Executes the decorated method only if we are authorized to process.
        Otherwise, apply the given :code:`default`.
        """

        def inner_metdhod(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.authorized:
                    return func(self, *args, **kwargs)  # pylint: disable=not-callable
                return self if default is None else default

            return wrapper

        return inner_metdhod

    @staticmethod
    def split_difference(start: datetime.datetime, end: datetime.datetime) -> dict:
        """
        Calculates the difference between the two datetime object.

        :param start:
            The starting time.

        :param end:
            The ending time.

        :raise TypeError:
            When the given :code:`start` or :code:`end` is not a
            :py:class:`datetime.datetime`.
        """

        if not isinstance(start, datetime.datetime):
            raise TypeError(
                f"<start> should be {datetime.datetime}, {type(start)} given."
            )

        if not isinstance(end, datetime.datetime):
            raise TypeError(
                f"<start> should be {datetime.datetime}, {type(start)} given."
            )

        difference = end.timestamp() - start.timestamp()

        result = {}

        result["days"] = difference // (24 * 60 * 60)
        result["hours"] = (difference // (60 * 60)) % 24
        result["minutes"] = (difference % 3600) // 60
        result["seconds"] = difference % 60

        return result

    @property
    def authorized(self) -> Optional[bool]:
        """
        Provides the currently state of the :code:`_authorized` attribute.
        """

        return self._authorized

    @authorized.setter
    def authorized(self, value: bool) -> None:
        """
        Sets the value of the :code:`authorized` attribute.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._authorized = value

    def set_authorized(self, value: bool) -> "ExecutionTime":
        """
        Sets the value of the :code:`authorized` attribute.

        :param value:
            The value to set.
        """

        self.authorized = value

        return self

    @execute_if_authorized(None)
    def set_start_time(self) -> "ExecutionTime":
        """
        Sets the starting time to now.
        """

        self.start_time = datetime.datetime.utcnow()

        return self

    @execute_if_authorized(None)
    def set_end_time(self) -> "ExecutionTime":
        """
        Sets the starting time to now.
        """

        self.end_time = datetime.datetime.utcnow()

        return self

    def guess_and_set_authorized(self) -> "ExecutionTime":
        """
        Try to guess and set the authorization from the configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.authorized = bool(
                PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.execution_time
            )
        else:
            self.authorized = self.STD_AUTHORIZED

    @execute_if_authorized(None)
    def get_info(self) -> dict:
        """
        Provides the information to work with.
        """

        if not self.end_time:
            self.set_end_time()

        result = self.split_difference(self.start_time, self.end_time)

        result["days"] = str(int(result["days"])).zfill(2)
        result["hours"] = str(int(result["hours"])).zfill(2)
        result["minutes"] = str(int(result["minutes"])).zfill(2)
        result["seconds"] = str(round(result["seconds"], 6)).zfill(2)

        return result
