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
# pylint: enable=line-too-long

from typing import Any, List

from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.converter.base import ConverterBase


class Subject2Complements(ConverterBase):
    """
    Converts a given wildcard into a testable subject.
    """

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Overrites the default behavior.

        :raise TypeError:
            When the given data to convert is not :py:class:`str` or a
            :py:class:`list`.
        """

        if not isinstance(value, (str, list)):
            raise TypeError(f"<value> should be {str} or {list}, {type(value)} given.")

        # pylint: disable=no-member
        super(Subject2Complements, self.__class__).data_to_convert.fset(self, value)

    # pylint: disable=arguments-differ
    def get_converted(self, *, include_given: bool = False) -> List[str]:
        """
        Provides the converted data.
        """

        complements = []

        if isinstance(self.data_to_convert, str):
            checker = DomainSyntaxChecker(self.data_to_convert)

            if include_given and self.data_to_convert not in complements:
                complements.append(self.data_to_convert)

            if self.data_to_convert.startswith("www."):
                complements.append(self.data_to_convert[4:])
            elif checker.is_valid_second_level():
                complements.append(f"www.{self.data_to_convert}")
        elif isinstance(self.data_to_convert, (list, set)):
            for subj in self.data_to_convert:
                complements.extend(
                    Subject2Complements(subj).get_converted(include_given=include_given)
                )

        return complements
