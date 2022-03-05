"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to convert a given month to our unified format.

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

from typing import Any, Dict, List

from PyFunceble.query.whois.converter.base import ConverterBase


class Month2Unified(ConverterBase):
    """
    Converts the given month into our unified format.
    """

    MAP: Dict[str, List[str]] = {
        "jan": [str(1), "01", "jan", "january", "jan."],
        "feb": [str(2), "02", "feb", "february", "feb."],
        "mar": [str(3), "03", "mar", "march", "mar."],
        "apr": [str(4), "04", "apr", "april", "apr."],
        "may": [str(5), "05", "may"],
        "jun": [str(6), "06", "jun", "june", "jun."],
        "jul": [str(7), "07", "jul", "july", "jul."],
        "aug": [str(8), "08", "aug", "august", "aug."],
        "sep": [str(9), "09", "sep", "september", "sep.", "sept", "sept."],
        "oct": [str(10), "oct", "october", "oct."],
        "nov": [str(11), "nov", "november", "nov."],
        "dec": [str(12), "dec", "december", "dec."],
    }

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
        super(Month2Unified, self.__class__).data_to_convert.fset(self, value)

    @ConverterBase.ensure_data_to_convert_is_given
    def get_converted(self) -> str:
        """
        Provides the converted data (after conversion)

        .. warning::
            If no month is found, the given data is given as response.
        """

        for to_return, possibilities in self.MAP.items():
            if self.data_to_convert.lower() in possibilities:
                return to_return

        return self.data_to_convert
