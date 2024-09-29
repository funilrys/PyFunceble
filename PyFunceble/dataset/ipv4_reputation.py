"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an interface which let us interact with the IPv4 reputation database.

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

from PyFunceble.dataset.base import DatasetBase
from PyFunceble.downloader.ipv4_reputation import IPV4ReputationDownloader
from PyFunceble.helpers.file import FileHelper


class IPV4ReputationDataset(DatasetBase):
    """
    Provides the interface for the lookup of the IPv4 reputation.
    """

    STORAGE_INDEX: Optional[str] = None
    downloader: Optional[IPV4ReputationDownloader] = None

    def __init__(self) -> None:
        self.downloader = IPV4ReputationDownloader()
        self.source_file = self.downloader.destination

    def __contains__(self, value: Any) -> bool:
        with self.get_content() as file_stream:
            for line in file_stream:
                line = line.strip()

                if line.startswith(f"{value}#"):
                    return True

        return False

    @DatasetBase.ensure_source_file_exists
    def get_content(self) -> open:
        """
        Provides a file handler which does let you read the content line by
        line.

        :raise FileNotFoundError:
            When the declared file does not exists.
        """

        file_helper = FileHelper(self.source_file)

        if not file_helper.exists() and bool(self.downloader):  # pragma: no cover
            ## pragma reason: Safety.
            self.downloader.start()

            if not file_helper.exists():
                raise FileNotFoundError(file_helper.path)

        return file_helper.open("r", encoding="utf-8")
