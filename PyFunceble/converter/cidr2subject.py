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

Provides the converter of CIDR to subjects.

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

from ipaddress import IPv4Network
from typing import Any, List, Optional

from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.converter.base import ConverterBase


class CIDR2Subject(ConverterBase):
    """
    Converts/Extracts the subjects of from the given CIDR.
    """

    ip_syntax_checker: Optional[IPSyntaxChecker] = None

    def __init__(self, data_to_convert: Optional[Any] = None) -> None:
        super().__init__(data_to_convert=data_to_convert)

        self.ip_syntax_checker = IPSyntaxChecker()

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Overrites the default behavior.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        # pylint: disable=no-member
        super(CIDR2Subject, self.__class__).data_to_convert.fset(self, value)

    def get_converted(self) -> List[str]:
        """
        Provides the subject-s to test.
        """

        result = set()

        subject = self.data_to_convert.strip()

        if subject:
            try:
                self.ip_syntax_checker.set_subject(subject)
                if self.ip_syntax_checker.is_valid_v4_range():
                    result.update(
                        str(x) for x in IPv4Network(self.ip_syntax_checker.subject)
                    )
                elif self.ip_syntax_checker.is_valid_v6_range():
                    # Not Implemented yet.
                    result.add(subject)
                else:
                    result.add(subject)
            except ValueError:
                result.add(subject)

        return list(result)
