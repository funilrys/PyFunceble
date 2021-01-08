# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an easy way to convert and get the complements of a subject.

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
# pylint: enable=line-too-long

from typing import Any, List, Optional

from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.converter.base import ConverterBase


class Subject2Complements(ConverterBase):
    """
    Converts a given wildcard into a testable subject.
    """

    _include_given: bool = False

    def __init__(
        self,
        data_to_convert: Optional[Any] = None,
        *,
        include_given: Optional[bool] = False,
    ) -> None:
        if include_given is not None:
            self.include_given = include_given

        super().__init__(data_to_convert=data_to_convert)

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Overrites the default behavior.

        :raise TypeError:
            When the given data to convert is not :py:class:`str` or a
            :py:class:`list`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        # pylint: disable=no-member
        super(Subject2Complements, self.__class__).data_to_convert.fset(self, value)

    @property
    def include_given(self) -> bool:
        """
        Provides the state of the :code:`_include_given` attribute.
        """

        return self._include_given

    @include_given.setter
    def include_given(self, value: bool) -> None:
        """
        Provides a way to activate/deactivate the inclusion of the given
        subject into the result.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._include_given = value

    def set_include_given(self, value: bool) -> "Subject2Complements":
        """
        Provides a way to activate/deactivate the inclusion of the given
        subject into the result.
        """

        self.include_given = value

        return self

    def get_converted(self) -> List[str]:
        """
        Provides the converted data.
        """

        result = []

        checker = DomainSyntaxChecker(self.data_to_convert)

        if self.include_given and self.data_to_convert not in result:
            result.append(self.data_to_convert)

        if self.data_to_convert.startswith("www."):
            result.append(self.data_to_convert[4:])
        elif checker.is_valid_second_level():
            result.append(f"www.{self.data_to_convert}")

        return result
