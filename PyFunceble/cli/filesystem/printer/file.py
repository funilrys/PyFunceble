"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the file printer.

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

import functools
from datetime import datetime
from typing import Dict, Optional

import PyFunceble.storage
from PyFunceble.cli.filesystem.printer.base import PrinterBase
from PyFunceble.helpers.file import FileHelper


class FilePrinter(PrinterBase):
    """
    Provides the file printer.
    """

    STD_FILE_GENERATION: str = (
        f"# Generated by {PyFunceble.storage.PROJECT_NAME} "
        f"(v{PyFunceble.storage.PROJECT_VERSION.split()[0]}) "
        f"/ {PyFunceble.storage.SHORT_REPO_LINK}\n"
    )

    file_helper: FileHelper = FileHelper()

    _destination: Optional[str] = None
    allow_coloration: bool = True

    def __init__(
        self,
        template_to_use: Optional[str] = None,
        *,
        dataset: Optional[Dict[str, str]] = None,
        destination: Optional[str] = None,
    ) -> None:
        if destination is not None:
            self.destination = destination

        super().__init__(template_to_use=template_to_use, dataset=dataset)

    def ensure_destination_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the destination is given before launching the
        decorated method.

        :raise TypeError:
            When the current :code:`self.template_to_use` is not set.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.destination, str):
                raise TypeError("<self.destination> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def propagate_destination(func):  # pylint: disable=no-self-argument
        """
        Propagates the new value of the destination just after launching the
        decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.file_helper.set_path(self.destination)

            return result

        return wrapper

    @property
    def destination(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_destination` attribute.
        """

        return self._destination

    @destination.setter
    @propagate_destination
    def destination(self, value: str) -> None:
        """
        Sets the destination to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When teh given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._destination = value

    def set_destination(self, value: str) -> "FilePrinter":
        """
        Sets the destination to use.

        :param value:
            The value to set.
        """

        self.destination = value

        return self

    @staticmethod
    def get_generation_date_line() -> str:
        """
        Provides the line which informs of the date a file was generated.
        """

        return f"# Date of generation: {datetime.utcnow().isoformat()}"

    @ensure_destination_is_given
    def print_interpolated_line(self) -> None:
        """
        Prints the interpolated line into the destination.
        """

        line_to_print = self.get_line_to_print() + "\n"
        without_header = ["hosts", "plain"]

        if not self.file_helper.exists():
            self.file_helper.write(self.STD_FILE_GENERATION, overwrite=True)
            self.file_helper.write(self.get_generation_date_line())
            self.file_helper.write("\n\n")

            if self.template_to_use not in without_header:
                self.file_helper.write(self.get_header_to_print())
                self.file_helper.write("\n")

        self.file_helper.write(line_to_print)
