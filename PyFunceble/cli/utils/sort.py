"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some utilities related to the sorting mechanism.

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

from typing import Any, Callable, List, Union

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.helpers.regex import RegexHelper


def standard(element: Any) -> List[Union[int, Any]]:
    """
    Provides the key to use for the standard sorting.

    :param element:
        The element to format.
    """

    element = element.strip()

    if not element:
        return []

    regex_helper = RegexHelper()

    element = Url2Netloc(element).get_converted().strip()

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        element = regex_helper.set_regex(
            r"^%s\s+" % PyFunceble.storage.CONFIGURATION.cli_testing.hosts_ip
        ).replace_match(element, "")

    cleaned = regex_helper.set_regex(r"[^a-zA-Z0-9\.]").replace_match(element, "")

    return [
        int(x) if x.isdigit() else x
        for x in regex_helper.set_regex(r"(\d+)").split(cleaned)
    ]


def hierarchical(element: Any) -> List[Union[int, Any]]:
    """
    Provides the key to use for the hierarchical sorting.

    :param element:
        The element to format.
    """

    element = element.strip()

    if not element:
        return []

    element = Url2Netloc(element).get_converted().strip()

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        element = RegexHelper(
            r"^%s\s+" % PyFunceble.storage.CONFIGURATION.cli_testing.hosts_ip
        ).replace_match(element, "")

    return standard(".".join(reversed(element.split("."))))


def get_best_sorting_key() -> Callable[[Any], List[Union[int, Any]]]:
    """
    Provides the best sorting key from the configuration.
    """

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if PyFunceble.storage.CONFIGURATION.cli_testing.sorting_mode.hierarchical:
            return hierarchical
    return standard
