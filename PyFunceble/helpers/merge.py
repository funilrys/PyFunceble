"""
The tool to check the availability or syntax of dosubject, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the merging helpers.

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


class Merge:
    """
    Simplify the merging of dict and list.

    :param subject:
        The subject to work with.
    """

    _subject: Optional[Any] = None

    def __init__(self, subject: Optional[Any] = None):
        if subject is not None:
            self.subject = subject

    @property
    def subject(self) -> Optional[Any]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    def subject(self, value: Any) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`list`.
        """

        self._subject = copy.deepcopy(value)

    def set_subject(self, value: Any) -> "Merge":
        """
        Sets the subject to work with.

        :param value:
            The subject to work with.

        :raise TypeError:
            When :code:`value` is not a :py:class:`list`.
        """

        self.subject = value

        return self

    def __list(self, origin: Any, strict: bool = True) -> List[Any]:
        """
        Process the list merging.

        :param strict:
            Activates the strict mode.
        """

        result = []

        if strict:
            for index, element in enumerate(self.subject):
                try:
                    if isinstance(element, dict) and isinstance(origin[index], dict):
                        result.append(Merge(element).into(origin[index], strict=strict))
                    elif isinstance(element, list) and isinstance(origin[index], list):
                        result.append(Merge(element).into(origin[index], strict=strict))
                    else:
                        result.append(element)
                except IndexError:  # pragma: no cover ## Safety
                    result.append(element)
        else:
            result = origin

            for element in self.subject:
                if element not in result:
                    result.append(element)

        return result

    def __dict(self, origin: Any, strict: bool = True) -> dict:
        """
        Process the dict merging.

        :param bool strict:
            Activates the strict mode.
        """

        result = {}

        for index, data in self.subject.items():
            if index in origin:
                if isinstance(data, dict) and isinstance(origin[index], dict):
                    result[index] = Merge(data).into(origin[index], strict=strict)
                elif isinstance(data, list) and isinstance(origin[index], list):
                    result[index] = Merge(data).into(origin[index], strict=strict)
                else:
                    result[index] = data
            else:
                result[index] = data

        for index, data in origin.items():
            if index not in result:
                result[index] = data

        return result

    def into(self, origin: Any, strict: bool = True) -> Any:
        """
        Process the mergin.

        :param origin: The original data.
        :param strict:
            Activates the strict mode.
        """

        origin = copy.deepcopy(origin)

        if isinstance(self.subject, list) and isinstance(origin, list):
            return self.__list(origin, strict=strict)

        if isinstance(self.subject, dict) and isinstance(origin, dict):
            return self.__dict(origin, strict=strict)

        return self.subject
