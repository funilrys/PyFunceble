"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to get an unified month format.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

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

from PyFunceble.exceptions import WrongParameterType

from .base import ConverterBase


class Month(ConverterBase):
    """
    Converts a given month to a unified format.
    """

    # We map the different month and their possible representation.
    months = {
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

    def __init__(self, data_to_convert):
        if not isinstance(data_to_convert, str):
            raise WrongParameterType(
                f"<data_to_convert> should be {str}, {type(data_to_convert)} given."
            )

        super().__init__(data_to_convert)

        for to_return, possibilities in self.months.items():
            if self.data_to_convert.lower() in possibilities:
                self.converted_data = to_return
                break
