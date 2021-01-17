"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some utilities related to the ascii logo.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import colorama

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.utils.platform import PlatformUtility


def colorify(color: str) -> str:
    """
    Colorify the logo with the given color.

    :param color:
        The name of the color to apply.

        .. warning::
            The given color name must be one of the supported
            by colorama.

    :raise ValueError:
        When the given :code:`color` is unsupported.
    """

    color = color.upper()

    if not hasattr(colorama.Fore, color):
        raise ValueError(f"<color> ({color!r}) is not supported.")

    color_to_apply = getattr(colorama.Fore, color)
    result = []

    if PlatformUtility.is_windows():
        to_color = PyFunceble.cli.storage.WIN_ASCII_PYFUNCEBLE
    else:
        to_color = PyFunceble.cli.storage.ASCII_PYFUNCEBLE

    if (
        PyFunceble.facility.ConfigLoader.is_already_loaded()
        and PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour
    ):
        for line in to_color.split("\n"):
            result.append(f"{color_to_apply}{line}{colorama.Fore.RESET}")

        return "\n".join(result)
    return to_color


def get_home_representation() -> str:
    """
    Provides our home ASCII logo representation.
    """

    return colorify("yellow")
