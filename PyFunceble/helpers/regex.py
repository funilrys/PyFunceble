"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the regular expressions helpers.

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

import re
from typing import List, Optional, Union


class RegexHelper:
    """
    Simplify the regex matching and usage.

    :param str regex: The regex to use.
    :param escape_regex: Escapes the given regex.
    """

    _regex: Optional[str] = None
    escape_regex: bool = False

    def __init__(self, regex: Optional[str] = None, escape_regex: bool = False):
        self.escape_regex = escape_regex

        if regex is not None:
            self.regex = regex

    @property
    def regex(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_regex` attribute.
        """

        return self._regex

    @regex.setter
    def regex(self, value: str) -> None:
        """
        Sets the regex to work with.

        :param value:
            The regex to work with.

        :raise TypeError:
            When :code:`value` is not :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(str)} given.")

        if not self.escape_regex:
            self._regex = value
        else:
            self._regex = re.escape(value)

    def set_regex(self, value: str) -> "RegexHelper":
        """
        Sets the regex to work with.

        :param value:
            The regex to work with.

        :raise TypeError:
            When :code:`value` is not :py:class:`str`.
        """

        self.regex = value

        return self

    def get_not_matching_list(self, data: List[str]) -> List[str]:
        """
        Returns the strings which does not the match the regex
        in the given data.
        """

        pre_result = re.compile(self.regex)

        return [x for x in data if not pre_result.search(str(x))]

    def get_matching_list(self, data: List[str]) -> List[str]:
        """
        Returns the strings which does the match the regex
        in the given data.
        """

        pre_result = re.compile(self.regex)

        return [x for x in data if pre_result.search(str(x))]

    def match(
        self,
        data: str,
        *,
        rematch: bool = False,
        group: int = 0,
        return_match: bool = True,
    ) -> Union[bool, str, List[str]]:
        """
        Checks if the given data match the given regex string.

        :param data: The data to work with.
        :param rematch:
            The equivalent of the $BASH_REMATCH but in Python.

            It's basically a list of all groups.
        :param group:
            The group to return when return_match is set to :code:`True`.
        :param return_match:
            Return the part that match the given regex string.
        """

        result = []
        to_match = re.compile(self.regex)

        if rematch:
            pre_result = to_match.findall(data)
        else:
            pre_result = to_match.search(data)

        if return_match and pre_result:
            if rematch:
                for res in pre_result:
                    if isinstance(res, tuple):
                        result.extend(list(res))
                    else:  # pragma: no cover ## Safety
                        result.append(res)

                if group != 0:
                    return result[group]
            else:
                result = pre_result.group(group).strip()

            return result

        if not return_match and pre_result:
            return True
        return False

    def replace_match(
        self,
        data: str,
        replacement: str,
        *,
        occurences: int = 0,
        multiline: bool = False,
    ) -> str:
        """
        Replaces the string which match the regex string with
        the given replacement.

        :param data: The data to work with.
        :param replacement: The replacement of the matched regex.
        :param occurences:
            The number of occurences to replace.

            .. note::
                :code:`0` means all occurences.
        """

        if isinstance(replacement, str):
            return re.sub(
                self.regex,
                replacement,
                data,
                occurences,
                flags=re.MULTILINE if multiline else 0,
            )
        return data

    def split(self, data: str) -> List[str]:
        """
        Split the reference of the given regex.

        :param str data: The data to work with.
        :rtype: list
        """

        return re.split(self.regex, data)
