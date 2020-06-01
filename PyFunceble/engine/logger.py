"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the loggging engine.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

import logging
from logging.handlers import RotatingFileHandler
from os import sep as directory_separator
from traceback import format_exc, format_stack

import PyFunceble


# pylint: disable=too-many-instance-attributes
class Logger:  # pragma: no cover
    """
    Provides our logging logic.
    """

    format_to_apply = "[%(asctime)s::%(levelname)s::%(origin_path)s:%(origin_line)s@%(origin_func)s](PID%(process)s:%(processName)s): %(message)s"  # pylint: disable=line-too-long
    """
    The format to apply.
    """

    root_logger_format = (
        "[%(asctime)s::%(levelname)s](PID%(process)s:%(processName)s): %(message)s"
    )
    """
    The format to parse to the root logger (if used).
    """

    def __init__(self, debug=False, on_screen=False, output_directory=None):
        self.on_screen = (
            on_screen
            or PyFunceble.helpers.EnvironmentVariable(
                "DEBUG_PYFUNCEBLE_ON_SCREEN"
            ).exists()
        )

        self.authorized = self.authorization(debug)

        self.init(output_directory)

    def authorization(self, debug):
        """
        Provides the operation authorization.
        """

        return (
            debug
            or self.on_screen
            or PyFunceble.helpers.EnvironmentVariable("DEBUG_PYFUNCEBLE").exists()
            or PyFunceble.helpers.EnvironmentVariable(
                "DEBUG_PYFUNCEBLE_ON_SCREEN"
            ).exists()
            or PyFunceble.CONFIGURATION.debug
        )

    def init(self, output_directory=None):
        """
        Initiates the logger.
        """

        if self.authorized:
            self.formatter = logging.Formatter(self.format_to_apply)

            self.__set_output_directory(output_directory)
            self.__init_loggers()

    def __set_output_directory(self, output_directory):
        """
        Shares the given output directory.

        .. note::
            If the given output directory does not exists, we create it.

        :param string output_directory: The output directory.
        """

        # pylint: disable=attribute-defined-outside-init

        if self.authorized and not self.on_screen:
            if output_directory:
                self.output_directory = output_directory
            else:
                self.output_directory = (
                    PyFunceble.OUTPUT_DIRECTORY
                    + PyFunceble.OUTPUTS.parent_directory
                    + PyFunceble.OUTPUTS.logs.directories.parent
                )

            PyFunceble.helpers.Directory(self.output_directory).create()

    def __init_loggers(self):
        """
        Initiates all loggers.
        """

        # pylint: disable=attribute-defined-outside-init

        if self.authorized and not hasattr(self, "info_logger"):
            self.info_logger = logging.getLogger("PyFunceble.info")
            self.info_logger.setLevel(logging.INFO)

            self.debug_logger = logging.getLogger("PyFunceble.debug")
            self.debug_logger.setLevel(logging.DEBUG)

            self.warning_logger = logging.getLogger("PyFunceble.warning")
            self.warning_logger.setLevel(logging.WARNING)

            self.error_logger = logging.getLogger("PyFunceble.error")
            self.error_logger.setLevel(logging.ERROR)

            self.fatal_logger = logging.getLogger("PyFunceble.fatal")
            self.fatal_logger.setLevel(logging.FATAL)

            self.critical_logger = logging.getLogger("PyFunceble.critical")
            self.critical_logger.setLevel(logging.CRITICAL)

            for logger_name in self.__dict__:
                if not logger_name.endswith("_logger"):
                    continue

                handler_type = logger_name.split("_")[0].lower()

                current_logger = getattr(self, logger_name)

                if not current_logger.hasHandlers():
                    current_logger.addHandler(self.__get_handler(handler_type))

    @classmethod
    def get_origin_info(cls):
        """
        Returns the information about where the logger was triggered.

        :return:
            A tuple, which is composed of the following.

            (trigger file path, trigger line, trigger function/method name)

        :rtype: tuple
        """

        stackback = [y for x in [x.split("\n") for x in format_stack()] for y in x if y]
        interest = stackback[-6].split(",")

        complete_file = interest[0].strip()[6:-1].split(directory_separator)

        try:
            if complete_file[-2] != PyFunceble.NAME:
                file = "/".join(complete_file)
            else:
                file = "/".join(complete_file[-2:])
        except IndexError:
            file = "/".join(complete_file)

        line = interest[1].strip().split()[-1].strip()
        func_name = interest[2].strip()[3:]

        return file, line, func_name

    def __get_handler(self, handler_type):
        """
        Provides a handler for of the given type.
        """

        handler_type = handler_type.upper()

        if hasattr(logging, handler_type):
            if self.on_screen:
                handler = logging.StreamHandler()
            else:
                handler = RotatingFileHandler(
                    self.output_directory + f"{handler_type.lower()}.log",
                    maxBytes=10_000_000,
                    backupCount=10,
                )

            handler.setLevel(getattr(logging, handler_type))
            handler.setFormatter(self.formatter)

            return handler

        return None

    def info(self, message):
        """
        Logs the info message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.info_logger.info(
                message,
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )

    def debug(self, message):
        """
        Logs the debug message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.debug_logger.debug(
                message,
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )

    def warning(self, message):
        """
        Logs the warning message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.warning_logger.warning(
                message,
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )

    def error(self, message):
        """
        Logs the error message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.error_logger.error(
                message,
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )

    def fatal(self, message):
        """
        Logs the fatal message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.fatal_logger.fatal(
                message,
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )

    def critical(self, message):
        """
        Logs the critical message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.critical_logger.critical(
                message,
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )

    def exception(self):
        """
        Logs the exception message.
        """

        if self.authorized:
            file, line, func_name = self.get_origin_info()
            self.error_logger.error(
                f"\n{format_exc()}",
                extra={
                    "origin_path": file,
                    "origin_line": line,
                    "origin_func": func_name,
                },
            )
