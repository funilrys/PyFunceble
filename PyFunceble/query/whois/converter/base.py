"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all WHOIS converter/extracter class.

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

import functools
from typing import Any, Optional


class ConverterBase:
    """
    Provides the base of all converter class.
    """

    _data_to_convert: Optional[Any] = None

    def __init__(self, data_to_convert: Optional[Any] = None) -> None:
        if data_to_convert is not None:
            self.data_to_convert = data_to_convert

    def ensure_data_to_convert_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the data to convert is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.data_to_convert, str):
                raise TypeError(
                    f"<self.subject> should be {str}, "
                    f"{type(self.data_to_convert)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def data_to_convert(self) -> Optional[Any]:
        """
        Provides the current state of the :code:`_data_to_convert` attribute.
        """

        return self._data_to_convert

    @data_to_convert.setter
    def data_to_convert(self, value: Any) -> Any:
        """
        Sets the data to convert / to work with.

        :param value:
            The data to convert
        """

        self._data_to_convert = value

    def set_data_to_convert(self, value: Any) -> "ConverterBase":
        """
        Sets the data to convert / to work with.

        :param value:
            The data to convert
        """

        self.data_to_convert = value

        return self

    @ensure_data_to_convert_is_given
    def get_converted(self) -> Optional[Any]:
        """
        Provides the converted data.
        """

        raise NotImplementedError()
