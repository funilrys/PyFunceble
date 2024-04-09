"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the stdout printer.

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

from typing import Dict, List, Optional

import colorama

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.filesystem.printer.base import PrinterBase


class StdoutPrinter(PrinterBase):
    """
    Provides the stdout printer.
    """

    STD_FILE_HEADER: str = (
        f"# Generated by {PyFunceble.storage.PROJECT_NAME} "
        f"(v{PyFunceble.storage.PROJECT_VERSION.split()[0]}) "
        f"/ {PyFunceble.storage.SHORT_REPO_LINK}\n"
    )
    STD_ALLOW_COLORATION: bool = True

    STATUS2BACKGROUND_COLOR: Dict[str, str] = {
        PyFunceble.storage.STATUS.up: f"{colorama.Fore.BLACK}{colorama.Back.GREEN}",
        PyFunceble.storage.STATUS.valid: f"{colorama.Fore.BLACK}"
        f"{colorama.Back.GREEN}",
        PyFunceble.storage.STATUS.sane: f"{colorama.Fore.BLACK}"
        f"{colorama.Back.GREEN}",
        PyFunceble.storage.STATUS.down: f"{colorama.Fore.BLACK}{colorama.Back.RED}",
        PyFunceble.storage.STATUS.malicious: f"{colorama.Fore.BLACK}"
        f"{colorama.Back.RED}",
        PyFunceble.storage.STATUS.invalid: f"{colorama.Fore.BLACK}"
        f"{colorama.Back.CYAN}",
    }

    STATUS2FORGROUND_COLOR: Dict[str, str] = {
        PyFunceble.storage.STATUS.up: f"{colorama.Style.BRIGHT}"
        f"{colorama.Fore.GREEN}",
        PyFunceble.storage.STATUS.valid: f"{colorama.Style.BRIGHT}"
        f"{colorama.Fore.GREEN}",
        PyFunceble.storage.STATUS.sane: f"{colorama.Style.BRIGHT}"
        f"{colorama.Fore.GREEN}",
        PyFunceble.storage.STATUS.down: f"{colorama.Style.BRIGHT}"
        f"{colorama.Fore.RED}",
        PyFunceble.storage.STATUS.malicious: f"{colorama.Style.BRIGHT}"
        f"{colorama.Fore.RED}",
        PyFunceble.storage.STATUS.invalid: f"{colorama.Style.BRIGHT}"
        f"{colorama.Fore.CYAN}",
    }

    BACKGROUND_COLORATED: List[str] = ["all", "less"]
    FOREGROUND_COLORATED: List[str] = ["percentage", "simple"]

    _allow_coloration: bool = True

    def __init__(
        self,
        template_to_use: Optional[str] = None,
        *,
        dataset: Optional[Dict[str, str]] = None,
        allow_coloration: Optional[bool] = None,
    ) -> None:
        if allow_coloration is not None:
            self.allow_coloration = allow_coloration
        else:
            self.guess_allow_coloration()

        super().__init__(template_to_use=template_to_use, dataset=dataset)

    @property
    def allow_coloration(self) -> bool:
        """
        Provides the current state of the :code:`_allow_coloration` attribute.
        """

        return self._allow_coloration

    @allow_coloration.setter
    def allow_coloration(self, value: bool) -> Optional[bool]:
        """
        Sets the authorization to use the coloration.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When teh given :code:`value` is empty.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._allow_coloration = value

    def set_allow_coloration(self, value: bool) -> "StdoutPrinter":
        """
        Sets the authorization to use the coloration.

        :param value:
            The value to set.
        """

        self.allow_coloration = value

        return self

    def guess_allow_coloration(self) -> "StdoutPrinter":
        """
        Try to guess and set the :code:`allow_coloration` attribute.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.allow_coloration = (
                PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour
            )
        else:
            self.allow_coloration = self.STD_ALLOW_COLORATION

    def print_interpolated_line(self):
        """
        Prints the interpolated line into the destination.
        """

        PyFunceble.facility.Logger.info("Started to print to stdout.")

        line_to_print = self.get_line_to_print()

        PyFunceble.facility.Logger.debug("Line to print: %r", line_to_print)

        if "status" in self.dataset:
            status_to_compare = self.dataset["status"]

            if self.allow_coloration:
                if self.template_to_use in self.BACKGROUND_COLORATED:
                    print(
                        f"{self.STATUS2BACKGROUND_COLOR[status_to_compare]}"
                        f"{line_to_print}"
                    )
                elif self.template_to_use in self.FOREGROUND_COLORATED:
                    print(
                        f"{self.STATUS2FORGROUND_COLOR[status_to_compare]}"
                        f"{line_to_print}"
                    )
                else:
                    print(line_to_print)
            else:
                print(line_to_print)
        elif self.template_to_use == "execution_time":
            if self.allow_coloration:
                print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}{line_to_print}")
            else:
                print(line_to_print)
        else:
            print(line_to_print)

        PyFunceble.facility.Logger.info("Finished to print to stdout.")
