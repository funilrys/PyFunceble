# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the logging handlers.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
import logging
from logging.handlers import RotatingFileHandler
from traceback import format_exc, format_stack

import PyFunceble


# pylint: disable=too-many-instance-attributes
class Logger:  # pragma: no cover
    """
    Provides our logging logic.
    """

    format_to_apply = "[%(asctime)s::%(levelname)s::%(origin_path)s:%(origin_line)s@%(origin_func)s](PID%(process)s): %(message)s"  # pylint: disable=line-too-long
    """
    The format to apply.
    """

    root_logger_format = "[%(asctime)s::%(levelname)s](PID%(process)s): %(message)s"
    """
    The format to parse to the root logger (if used).
    """

    def __init__(self, debug=False, on_screen=False, output_directory=None):
        if "logger" not in PyFunceble.INTERN:
            self.on_screen = (
                on_screen or "DEBUG_PYFUNCEBLE_ON_SCREEN" in PyFunceble.environ
            )

            self.authorized = self.authorization(debug)

            if self.authorized:
                self.formatter = logging.Formatter(self.format_to_apply)

                self.__set_output_directory(output_directory)
                self.__init_loggers()

                PyFunceble.INTERN["logger"] = self.__dict__
        else:
            for index, data in PyFunceble.INTERN["logger"].items():
                setattr(self, index, data)

    def authorization(self, debug):
        """
        Provide the operation authorization.
        """

        return (
            debug
            or self.on_screen
            or "DEBUG_PYFUNCEBLE" in PyFunceble.environ
            or "DEBUG_PYFUNCEBLE_ON_SCREEN" in PyFunceble.environ
            or PyFunceble.CONFIGURATION.debug
        )

    def __set_output_directory(self, output_directory):
        """
        Shares the given output directory.

        .. note::
            If the given output directory does not exists, we create it.

        :param string output_directory: The output directory.
        """

        if self.authorized:
            if output_directory:
                self.output_directory = output_directory
            else:
                self.output_directory = (
                    PyFunceble.OUTPUT_DIRECTORY
                    + PyFunceble.OUTPUTS.parent_directory
                    + PyFunceble.OUTPUTS.logs.directories.parent
                )

            if not PyFunceble.path.isdir(self.output_directory):
                PyFunceble.mkdir(self.output_directory)

    def __init_loggers(self):
        """
        Init all loggers.
        """

        if self.authorized:
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
        Return the information about where the logger was triggered.

        :return:
            A tuple, which is composed of the following.

            (trigger file path, trigger line, trigger function/method name)

        :rtype: tuple
        """

        stackback = [y for x in [x.split("\n") for x in format_stack()] for y in x if y]
        interest = stackback[-6].split(",")

        complete_file = interest[0].strip()[6:-1].split(PyFunceble.directory_separator)

        if complete_file[-2] != PyFunceble.NAME:
            file = "/".join(complete_file)
        else:
            file = "/".join(complete_file[-2:])
        line = interest[1].strip().split()[-1].strip()
        func_name = interest[2].strip()[3:]

        return file, line, func_name

    def __get_handler(self, handler_type):
        """
        Provide a handler for of the given type.
        """

        handler_type = handler_type.upper()

        if hasattr(logging, handler_type):
            if self.on_screen:
                handler = logging.StreamHandler()
            else:
                # handler = logging.FileHandler(
                #     self.output_directory + f"{handler_type.lower()}.log"
                # )
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
        Log the info message.
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
        Log the debug message.
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
        Log the warning message.
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
        Log the error message.
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
        Log the fatal message.
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
        Log the critical message.
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
        Log the exception message.
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
