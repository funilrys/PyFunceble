"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our registrar extrator.

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

from typing import Any, List, Optional

from PyFunceble.helpers.regex import RegexHelper
from PyFunceble.query.whois.converter.base import ConverterBase


class RegistarExtractor(ConverterBase):
    """
    Provides an interface for the extration of the registrar.
    """

    PATTERNS: List[str] = [
        r"authorized\s+agency(\s+|):(.*)",
        r"domain\s+support(\s+|):(.*)",
        r"registrar\s+name(\s+|):(.*)",
        r"registrar_name(\s+|):(.*)",
        r"registrar(\s+|):(.*)",
        r"registrar\.+(\s+|):(.*)",
        r"registration\s+service\s+provider(\s+|):(.*)",
        r"sponsoring\s+registrar(\s+|):(.*)",
        r"sponsoring\s+registrar\s+organization(\s+|):(.*)",
    ]

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Sets the data to convert and work with.

        :param value:
            The record to work with.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        # pylint: disable=no-member
        super(RegistarExtractor, self.__class__).data_to_convert.fset(self, value)

    def __get_line(self) -> Optional[str]:
        """
        Tries to get the registrar line from the given record.
        """

        for regex in self.PATTERNS:
            registrar_line = RegexHelper(r"(?i)" + regex).match(
                self.data_to_convert, return_match=True, rematch=True, group=0
            )

            if not registrar_line:
                continue

            return registrar_line
        return None

    @ConverterBase.ensure_data_to_convert_is_given
    def get_converted(self) -> Optional[str]:
        """
        Provides the registrar of the record (if found).
        """

        registrar_line = self.__get_line()

        if registrar_line:
            try:
                return [x.strip() for x in registrar_line if x.strip()][0]
            except IndexError:
                pass

        return None
