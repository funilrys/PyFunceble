"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our converter class.

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

from typing import Any, Optional


class ConverterBase:
    """
    Provides the base of all converter class.
    """

    _aggressive: bool = False
    _data_to_convert: Optional[Any] = None

    def __init__(
        self,
        data_to_convert: Optional[Any] = None,
        *,
        aggressive: bool = None,
    ) -> None:
        if data_to_convert is not None:
            self.data_to_convert = data_to_convert

        if aggressive is not None:
            self.aggressive = aggressive

    @property
    def data_to_convert(self) -> Optional[Any]:
        """
        Provides the current state of the :code:`_data_to_convert` attribute.
        """

        return self._data_to_convert

    @data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Sets the data to convert / to work with.

        :param value:
            The value to set.
        """

        self._data_to_convert = value

    def set_data_to_convert(self, value: Any) -> "ConverterBase":
        """
        Sets the data to convert / to work with.

        :param value:
            The value to set.
        """

        self.data_to_convert = value

        return self

    @property
    def aggressive(self) -> bool:
        """
        Provides the state of the :code:`_aggressive` attribute.
        """

        return self._aggressive

    @aggressive.setter
    def aggressive(self, value: bool) -> None:
        """
        Provides a way to activate/deactivate the aggressive decoding.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._aggressive = value

    def set_aggressive(self, value: bool) -> "ConverterBase":
        """
        Provides a way to activate/deactivate the aggressive decoding.
        """

        self.aggressive = value

        return self

    def get_converted(self) -> Optional[Any]:
        """
        Provides the converted data.
        """

        raise NotImplementedError()

    def convert(self, data: Any, *, aggressive: bool = False) -> Optional[Any]:
        """
        Converts the given dataset.

        :param data:
            The data to convert.
        :param aggressive.
            Whether we should aggressively extract datasets.
        """

        raise NotImplementedError()
