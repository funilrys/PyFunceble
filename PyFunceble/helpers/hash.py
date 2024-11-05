"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the hashing helpers.

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

import hashlib
from typing import Optional, Union

from PyFunceble.helpers.file import FileHelper


class HashHelper:
    """
    Simplify the hashing of data or file content.

    :param str algo:
        The algorithm to use for hashing.

    :raise ValueError: When the given algo is not known.
    """

    _algo: str = "sha512_224"

    def __init__(self, algo: Optional[str] = None):
        if algo is not None:
            self.algo = algo

    @property
    def algo(self) -> str:
        """
        Provides the current state fo the :code:`_algo` attribute.
        """

        return self._algo

    @algo.setter
    def algo(self, value: str) -> None:
        """
        Sets the algorithm to work with.

        :param value:
            The name of the hash to use.

        :raise TypeError:
            When :code:`value` is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        value = value.lower()

        if value not in hashlib.algorithms_available:
            raise ValueError(
                f"<value> ({value!r}) in an unknown algorithm "
                f"({hashlib.algorithms_available})."
            )

        self._algo = value

    def set_algo(self, value: str) -> "HashHelper":
        """
        Sets the algorithm to work with.

        :param value:
            The name of the hash to use.
        """

        self.algo = value

        return self

    def hash_file(self, file_path: str) -> str:
        """
        Hashes the content of the given file.

        :param file_path:
            The path of the file to read.
        """

        block_size = 4096

        digest = hashlib.new(self.algo)

        with FileHelper(file_path).open("rb") as file_stream:
            block = file_stream.read(block_size)

            while block:
                digest.update(block)
                block = file_stream.read(block_size)

        return digest.hexdigest()

    def hash_data(self, data: Union[str, bytes]) -> str:
        """
        Hashes the given data.

        :param data:
            The data to hash.

        :raise TypeError:
            When :code:`data` is not :py:class:`str` or :py:class:`bytes`.
        """

        if not isinstance(data, (bytes, str)):
            raise TypeError(f"<data> should be {bytes} or {str}, {type(data)}, given.")

        if isinstance(data, str):
            data = data.encode()

        digest = hashlib.new(self.algo)
        digest.update(data)

        return digest.hexdigest()
