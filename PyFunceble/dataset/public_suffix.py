"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an interface which let us interact with the Public Suffix List.

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

from typing import Any, List, Optional

from PyFunceble.dataset.base import DatasetBase
from PyFunceble.downloader.public_suffix import PublicSuffixDownloader


class PublicSuffixDataset(DatasetBase):
    """
    Provides the dataset handler for the Public Suffix List dataset.
    """

    STORAGE_INDEX: str = "PUBLIC_SUFFIX"
    downloader: Optional[PublicSuffixDownloader] = None

    def __init__(self) -> None:
        self.downloader = PublicSuffixDownloader()
        self.source_file = self.downloader.destination

    def __contains__(self, value: Any) -> bool:
        if value.startswith("."):
            value = value[1:]

        return value in self.get_content()

    def __getattr__(self, value: Any) -> List[str]:
        if value.startswith("."):
            value = value[1:]

        if value in self:
            return self.get_content()[value]

        return []

    def __getitem__(self, value: Any) -> List[str]:
        return self.__getattr__(value)

    def is_extension(self, extension: str) -> bool:
        """
        Checks if the given extension is registered.

        :raise TypeError:
            When :code:`extension` is not a :py:class:`str`.
        """

        if not isinstance(extension, str):
            raise TypeError(f"<extension> should be {str}, {type(extension)} given.")

        return extension in self

    def get_available_suffix(self, extension: str) -> List[str]:
        """
        Provides the available suffix for the extension.
        """

        if self.is_extension(extension):
            return self[extension]
        return []
