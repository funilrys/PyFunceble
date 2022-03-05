"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our logger.

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
import logging
import logging.handlers
import os
import traceback
from typing import Generator, Optional, Tuple, Union

import PyFunceble.cli.storage
import PyFunceble.storage
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper


class Logger:
    """
    Provides our logging logic.

    .. warning::
        There is several way to activate the logging.

        1. Through the :code:`PYFUNCEBLE_DEBUG_ON_SCREEN` environment variable.
        2. Through the :code:`DEBUG_PYFUNCEBLE_ON_SCREEN` environment variable.
        3. Through the :code:`PYFUNCEBLE_DEBUG` environment variable.
        4. Through the :code:`DEBUG_PYFUNCEBLE` environment variable.
        5. Through the :py:meth:`PyFunceble.logger.Logger.set_activated` method.
    """

    # pylint: disable=too-many-public-methods

    # pylint: disable=line-too-long
    OWN_FORMAT: str = (
        "[%(asctime)s | %(levelname)s | %(origin_path)s:"
        "%(origin_line)s@%(origin_func)s | PPID%(process)d:%(processName)s]:\n"
        "%(message)s\n"
    )
    """
    Our very own format.
    """

    ROOT_FORMAT: str = (
        "[%(asctime)s::%(levelname)s](PID%(process)s:%(processName)s): %(message)s"
    )
    """
    The format of the root loggy.
    """

    STD_MIN_LEVEL: int = logging.INFO

    _activated: bool = False
    _min_level: int = logging.INFO
    _output_directory: Optional[str] = None

    own_formatter: logging.Formatter = logging.Formatter(OWN_FORMAT)
    root_formatter: logging.Formatter = logging.Formatter(ROOT_FORMAT)

    info_logger: Optional[logging.Logger] = None
    debug_logger: Optional[logging.Logger] = None
    warning_logger: Optional[logging.Logger] = None
    error_logger: Optional[logging.Logger] = None
    fatal_logger: Optional[logging.Logger] = None
    critical_logger: Optional[logging.Logger] = None
    sqlalchemy_logger: Optional[logging.Logger] = None

    env_var_helper: EnvironmentVariableHelper = EnvironmentVariableHelper()

    def __init__(
        self,
        *,
        activated: Optional[bool] = None,
        min_level: Optional[int] = None,
        output_dir: Optional[str] = None,
    ) -> None:

        if output_dir:
            self.output_directory = output_dir
        else:
            self.output_directory = os.path.join(
                PyFunceble.cli.storage.OUTPUT_DIRECTORY,
                PyFunceble.cli.storage.OUTPUTS.logs.directories.parent,
            )

        if activated is not None:
            self.activated = activated

        if min_level is not None:
            self.min_level = min_level
        else:
            self.guess_and_set_min_level()

    @property
    def on_screen(self) -> bool:
        """
        Provides the authorization to log on screen.
        """

        return (
            self.env_var_helper.set_name("PYFUNCEBLE_DEBUG_ON_SCREEN").exists()
            or self.env_var_helper.set_name("DEBUG_PYFUNCEBLE_ON_SCREEN").exists()
        )

    @property
    def on_file(self) -> bool:
        """
        Provides the authorization to log on file.
        """

        return (
            self.env_var_helper.set_name("PYFUNCEBLE_DEBUG").exists()
            or self.env_var_helper.set_name("DEBUG_PYFUNCEBLE").exists()
        )

    @property
    def activated(self) -> bool:
        """
        Provides the current state of the :code:`_activated` attribute.
        """

        return self._activated

    @activated.setter
    def activated(self, value: bool) -> None:
        """
        Sets the value of the activated attribute.

        :param value:
            The value to set.

        :raise TypeError:
            When the given value is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._activated = value

    def set_activated(self, value: bool) -> "Logger":
        """
        Sets the value of the activated attribute.

        :param value:
            The value to set.
        """

        self.activated = value

        return self

    @property
    def min_level(self) -> int:
        """
        Provides the current state of the :code:`_min_level` attribute.
        """

        return self._min_level

    @min_level.setter
    def min_level(self, value: Union[int, str]) -> None:
        """
        Sets the minimum level to log.

        :param value:
            The value to set.

        :raise TypeError:
            When the given value is not a :py:class:`int` or :py:class:`str`.
        :raise ValueError:
            When the given value is not supported
        """

        if not isinstance(value, (int, str)):
            raise TypeError(f"<value> should be {int} or {str}, {type(value)} given.")

        # pylint: disable=protected-access
        if isinstance(value, int) and value not in logging._levelToName:
            raise ValueError(f"<value> is not in {list(logging._nameToLevel.keys())}")

        if isinstance(value, str):
            if value.upper() not in logging._nameToLevel:
                raise ValueError(
                    f"<value> is not in {list(logging._nameToLevel.keys())}"
                )
            value = logging._nameToLevel[value.upper()]

        self._min_level = value

        return self

    def set_min_level(self, value: Union[int, str]) -> "Logger":
        """
        Sets the minimum level to log.

        :param value:
            The value to set.
        """

        self.min_level = value

        return self

    @property
    def output_directory(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_output_directory` attribute.
        """

        if self.authorized:
            DirectoryHelper(self._output_directory).create()

        return self._output_directory

    @output_directory.setter
    def output_directory(self, value: str) -> None:
        """
        Sets the directory to write.

        Side Effect:
            Creation of the given value if it does not exists.

        :param value:
            The value to set.

        :raise TypeError:
            When the given value is not a  :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        self._output_directory = value

    def set_output_directory(self, value: str) -> "Logger":
        """
        Sets the directory to write.

        :param value:
            The value to set.
        """

        self.output_directory = value

        return self

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to actually log.
        """

        return (
            self.activated
            or self.on_screen
            or self.on_file
            or (
                bool(PyFunceble.storage.CONFIGURATION)
                and bool(PyFunceble.storage.CONFIGURATION.debug.active)
            )
        )

    @staticmethod
    def get_origin() -> dict:
        """
        Provides the informatioon about where the logger was triggered.

        :return:
            A tuple, which is composed of the following.

            (trigger file path, trigger line, trigger function/method name)
        """

        stackback = [
            y for x in [x.split("\n") for x in traceback.format_stack()] for y in x if y
        ]
        interest = stackback[-6].split(",")

        complete_file = interest[0].strip()[6:-1].split(os.sep)

        try:
            if complete_file[-2] != PyFunceble.storage.PROJECT_NAME:
                file = "/".join(complete_file)
            else:
                file = "/".join(complete_file[-2:])
        except IndexError:
            file = "/".join(complete_file)

        line = interest[1].strip().split()[-1].strip()
        func_name = interest[2].strip()[3:]

        if PyFunceble.storage.PROJECT_NAME in file:
            file = os.path.relpath(file)

        return {"origin_path": file, "origin_line": line, "origin_func": func_name}

    def single_logger_factory(level_name: str):  # pylint: disable=no-self-argument
        """
        Provides the general factory.

        :param level_name:
            The level to log.
        """

        def single_logger(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                # pylint: disable=no-member, protected-access

                if (
                    self.authorized
                    and logging._nameToLevel[level_name.upper()] >= self.min_level
                ):
                    try:
                        logger = getattr(
                            getattr(self, f"{level_name.lower()}_logger"),
                            level_name.lower(),
                        )

                        if not logger:
                            self.init_loggers()
                    except AttributeError:
                        self.init_loggers()

                        logger = getattr(
                            getattr(self, f"{level_name.lower()}_logger"),
                            level_name.lower(),
                        )

                    return logger(*args, **kwargs, extra=self.get_origin())

                return func

            return wrapper

        return single_logger

    def guess_and_set_min_level(self) -> "Logger":
        """
        Tries to guess the min level from the configuration.
        """

        env_vars = ["PYFUNCEBLE_DEBUG_LVL", "PYFUNCEBLE_LOGGING_LVL"]

        env_var_helper = EnvironmentVariableHelper()
        env_var_found = False

        for env_var in env_vars:
            if env_var_helper.set_name(env_var).exists():
                self.min_level = env_var_helper.get_value()
                env_var_found = True

                break

        if not env_var_found:
            if PyFunceble.storage.CONFIGURATION:
                # pylint: disable=protected-access
                self.min_level = logging._nameToLevel[
                    PyFunceble.storage.CONFIGURATION.debug.level.upper()
                ]
            else:
                self.min_level = self.STD_MIN_LEVEL

    def guess_all_settings(self) -> "Logger":
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self

    def destroy_loggers(self) -> "Logger":
        """
        Destroyes all existing loggers.
        """

        for logger, level in self.get_next_logger():
            logger.handlers.clear()

            delattr(self, f"{level}_logger")
            setattr(self, f"{level}_logger", None)

    def get_next_logger(self) -> Generator[None, Tuple[logging.Logger, str], None]:
        """
        Provides the next logger.
        """

        for logger_var_name in Logger.__dict__:
            if (
                not logger_var_name.endswith("_logger")
                or logger_var_name == "get_next_logger"
                or "sqlalchemy" in logger_var_name
            ):
                continue

            level = logger_var_name.split("_", 1)[0]

            if not getattr(self, logger_var_name):
                setattr(self, logger_var_name, logging.getLogger(f"PyFunceble.{level}"))

            yield getattr(self, logger_var_name), level

    def init_loggers(self) -> "Logger":
        """
        Init all our logger.
        """

        if self.authorized:
            self.destroy_loggers()

            if not self.sqlalchemy_logger:
                self.sqlalchemy_logger = logging.getLogger("sqlalchemy")

            self.sqlalchemy_logger.setLevel(self.min_level)
            self.sqlalchemy_logger.propagate = False

            for logger, level in self.get_next_logger():
                logger.propagate = False

                # pylint: disable=protected-access
                logger.setLevel(logging._nameToLevel[level.upper()])
                logger.addHandler(self.get_handler(level))

        return self

    def get_handler(
        self, level_name: str
    ) -> Optional[Union[logging.StreamHandler, logging.handlers.RotatingFileHandler]]:
        """
        Given a level name, this method provides the right handler for it!
        """

        level_name = level_name.upper()
        specials = ["SQLALCHEMY"]

        if hasattr(logging, level_name) or level_name in specials:
            if self.on_screen:
                handler = logging.StreamHandler()
            else:
                handler = logging.handlers.RotatingFileHandler(
                    os.path.join(self.output_directory, f"{level_name.lower()}.log"),
                    maxBytes=100_000_000,
                    backupCount=5,
                )

            if level_name in specials:
                handler.setLevel(self.min_level)
                handler.setFormatter(self.root_formatter)
            else:
                handler.setLevel(getattr(logging, level_name))
                handler.setFormatter(self.own_formatter)

            return handler

        return None

    @single_logger_factory("info")
    def info(self, *args, **kwargs):
        """
        Logs to the PyFunceble.info logger.
        """

    @single_logger_factory("debug")
    def debug(self, *args, **kwargs):
        """
        Logs to the PyFunceble.debug logger.
        """

    @single_logger_factory("warning")
    def warning(self, *args, **kwargs):
        """
        Logs to the PyFunceble.warning logger.
        """

    @single_logger_factory("error")
    def error(self, *args, **kwargs):
        """
        Logs to the PyFunceble.error logger.
        """

    @single_logger_factory("fatal")
    def fatal(self, *args, **kwargs):
        """
        Logs to the PyFunceble.fatal logger.
        """

    @single_logger_factory("critical")
    def critical(self, *args, **kwargs):
        """
        Logs to the PyFunceble.critical logger.
        """

    @single_logger_factory("exception")
    def exception(self, *args, **kwargs):
        """
        Logs to the PyFunceble.exception logger.
        """
