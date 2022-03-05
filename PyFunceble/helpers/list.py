"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the list helpers

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

import copy
from typing import Any, List, Optional


class ListHelper:
    """
    Simplify the list manipulation.

    :param subject:
        The list to work with.
    :param bool remove_empty: Process the deletion of empty strings.
    """

    _subject: Optional[List[Any]] = None

    def __init__(self, subject: Optional[List[Any]] = None):
        if subject is not None:
            self.subject = subject

    @property
    def subject(self):
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    def subject(self, value: List[Any]) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`list`.
        """

        if not isinstance(value, list):
            raise TypeError(f"<value> should be {list}, {type(value)} given.")

        self._subject = copy.deepcopy(value)

    def set_subject(self, value: List[Any]) -> "ListHelper":
        """
        Sets the subject to work with.

        :param value:
            The subject to work with.
        """

        self.subject = value

        return self

    def remove_empty(self) -> "ListHelper":
        """
        Removes the empty entries of the given list.
        """

        self.subject = [x for x in self.subject if x is None or x]

        return self

    def remove_duplicates(self) -> "ListHelper":
        """
        Removes the duplicates of the current list.
        """

        result = []

        for element in self.subject:
            if element not in result:
                result.append(element)

        self.subject = result

        return self

    def sort(self, *, reverse: bool = False) -> "ListHelper":
        """
        Sorts the given list (of string preferably).

         :param bool reverse: Tell us if we have to reverse the list.
        """

        self.custom_sort(str.lower, reverse=reverse)

        return self

    def custom_sort(self, key_method: Any, *, reverse: bool = False) -> "ListHelper":
        """
        Sorts the list with the given key method.

        :param key_method:
            A function or method to use to format the
            readed element before sorting.
        :type key_method: function|method

        :param bool reverse: Tell us if we have to reverse the list.
        """

        self.subject = sorted(self.subject, key=key_method, reverse=reverse)

        return self
