"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our public suffix file generator.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import concurrent.futures
from typing import Optional

import PyFunceble.facility
from PyFunceble.converter.wildcard2subject import Wildcard2Subject
from PyFunceble.dataset.public_suffix import PublicSuffixDataset
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.list import ListHelper


class PublicSuffixGenerator:
    """
    Provides an interface for the generation of the public suffix file.
    """

    UPSTREAM_LINK: str = (
        "https://raw.githubusercontent.com/publicsuffix/list/%s/public_suffix_list.dat"
        % "master"
    )
    """
    Provides the upstream stream.
    """

    COMMENT_SIGN: str = ["//", "!"]
    """
    The sign which we should consider as comment.
    """

    _destination: Optional[str] = None

    database: dict() = dict()
    """
    An internal storage of our map.
    """

    wildacrd2subject: Wildcard2Subject = Wildcard2Subject()

    def __init__(self, destination: Optional[str] = None) -> None:
        if destination is not None:
            self.destination = destination
        else:
            self.destination = PublicSuffixDataset().source_file

    @property
    def destination(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_destination` attribute.
        """

        return self._destination

    @destination.setter
    def destination(self, value: str) -> None:
        """
        Sets the destination to write.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._destination = value

    def set_destination(self, value: str) -> "PublicSuffixGenerator":
        """
        Sets the destination to write.

        :param value:
            The value to set.
        """

        self.destination = value

        return self

    def parse_line(self, line: str) -> dict:
        """
        Parses and provides the dataset to save.
        """

        line = line.strip()
        result = dict()

        if not any(line.startswith(x) for x in self.COMMENT_SIGN) and "." in line:
            lines = [line, line.encode("idna").decode("utf-8")]
            lines = [
                self.wildacrd2subject.set_data_to_convert(x).get_converted()
                for x in lines
            ]
            extension = lines[0].rsplit(".", 1)[-1]

            for suffix in lines:
                if extension in result:
                    result[extension].append(suffix)
                else:
                    result[extension] = [suffix]

        return result

    def start(self, max_workers: Optional[int] = None):
        """
        Starts the generation of the dataset file.
        """

        raw_data = DownloadHelper(self.UPSTREAM_LINK).download_text().split("\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(self.parse_line, raw_data):
                for extension, suffixes in result.items():
                    if extension not in self.database:
                        self.database[extension] = suffixes
                    else:
                        self.database[extension].extend(suffixes)

                    PyFunceble.facility.Logger.debug(
                        "Got: extension: %r ; suffixes: %r.", extension, suffixes
                    )

        for extension, suffixes in self.database.items():
            self.database[extension] = (
                ListHelper(suffixes).remove_duplicates().remove_empty().sort().subject
            )

        DictHelper(self.database).to_json_file(self.destination)

        return self
