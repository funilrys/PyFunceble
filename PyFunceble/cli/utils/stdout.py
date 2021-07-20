"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some utilities related to the CLI stdout.

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

import secrets

import colorama

import PyFunceble.facility
import PyFunceble.storage


def get_template_to_use() -> str:
    """
    Provides the template to use.
    """

    if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.simple:
        return "simple"
    if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.all:
        return "all"

    return "less"


def print_single_line(value: str = ".", end: str = "", *, force: bool = False) -> None:
    """
    Prints the given :code:`value` in the current line.

    :param value:
        The default value
    :param end:
        Same as the end argument of the built-in print function.
    :param force:
        Forces the printing.
    """

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if (
            force
            or PyFunceble.storage.CONFIGURATION.cli_testing.ci.active
            or PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.dots
        ):
            print(value, end=end)


def print_thanks() -> None:
    """
    Randomly prints our thanks message.
    """

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if (
            not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet
            and not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.simple
        ):
            if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour:
                print(
                    f"\n{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    f"Thank you for using PyFunceble!{colorama.Style.RESET_ALL}"
                )
            else:
                print("\nThank you for using PyFunceble!")

            if int(secrets.token_hex(8), 16) % 3 == 0:
                if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour:
                    print(
                        f"{colorama.Fore.YELLOW}{colorama.Style.BRIGHT}"
                        f"Share your experience on {colorama.Fore.CYAN}Twitter "
                        f"{colorama.Fore.YELLOW}with {colorama.Fore.CYAN}"
                        f"#PyFunceble{colorama.Fore.YELLOW} "
                        f"or {colorama.Fore.CYAN}@PyFunceble"
                        f"{colorama.Fore.YELLOW}!"
                    )
                else:
                    print(
                        "Share your experience on Twitter with #PyFunceble or "
                        "@PyFunceble!"
                    )

            if int(secrets.token_hex(8), 16) % 3 == 0:
                if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour:
                    print(
                        f"{colorama.Fore.YELLOW}{colorama.Style.BRIGHT}"
                        f"Do you have a feedback, an issue or an improvement idea? "
                        f"{colorama.Fore.YELLOW}Let us know on {colorama.Fore.CYAN}"
                        f"GitHub{colorama.Fore.YELLOW}!"
                    )
                else:
                    print(
                        "Do you ave a feedback, an issue or an improvement idea? "
                        "Let us know on GitHub!"
                    )
