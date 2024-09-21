"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to convert/extract the network location of a given URL.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import urllib.parse
from typing import Any, Optional

from PyFunceble.converter.base import ConverterBase


class Url2Netloc(ConverterBase):
    """
    Provides the interface for the conversion/extration of the network location
    of a given URL.
    """

    parsed_url: Optional[urllib.parse.ParseResult] = None
    """
    Expose the parsed URL.
    """

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Overrites the default behavior.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`
        :raise ValueError:
            When the given data to convert is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        # pylint: disable=no-member
        super(Url2Netloc, self.__class__).data_to_convert.fset(self, value)

    @staticmethod
    def parse_single_url(data) -> Optional[urllib.parse.ParseResult]:
        """
        Parses the URL.
        """

        if data:
            if "[" in data and "]" not in data or "]" in data and "[" not in data:
                # Own wrapper around "Invalid IPv6 URL" when
                # http://example.org."] is given (for example.)
                data = data.replace("[", "").replace("]", "")

            return urllib.parse.urlparse(data)
        return None

    def parse_url(self) -> "Url2Netloc":
        """
        Parses the URL.
        """

        self.parsed_url = self.parse_single_url(self.data_to_convert)

        return self

    def get_converted(self) -> str:
        """
        Provides the converted data (after conversion)
        """

        # Retrocompatibility.
        self.parse_url()

        return self.convert(self.data_to_convert)

    def convert(self, data: Any, *, aggressive: bool = False) -> str:
        """
        Converts the given dataset.

        :param data:
            The data to convert.
        """

        _ = aggressive
        parsed_url = self.parse_single_url(data)

        if not parsed_url.netloc and parsed_url.path:
            netloc = parsed_url.path
        elif parsed_url.netloc:
            netloc = parsed_url.netloc
        else:  # pragma: no cover ## Safety
            netloc = data

        if "//" in netloc:
            netloc = netloc[netloc.find("//") + 2 :]

        if "/" in netloc:
            netloc = netloc[: netloc.find("/")]

        return netloc
