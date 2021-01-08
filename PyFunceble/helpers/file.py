"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the file helpers.

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

import os
import shutil
from typing import Any, Optional

from PyFunceble.helpers.directory import DirectoryHelper


class FileHelper:
    """
    Simplify the file manipulations.

    :param str path: The file path to work with.
    """

    _path: Optional[str] = None

    def __init__(self, path: Optional[str] = None):
        if path:
            self.path = path

    @property
    def path(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_path` attribute.
        """

        return self._path

    @path.setter
    def path(self, value: str) -> None:
        """
        Sets the path to work with.

        :param value:
            The path to work with.

        :raise TypeError:
            When :code:`value` is a :py:class:`value`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} is given.")

        self._path = value

    def set_path(self, value: str) -> "FileHelper":
        """
        Sets the path to work with.

        :param value:
            The path to work with.
        """

        self.path = value

        return self

    def join_path(self, *args) -> str:
        """
        Joins the given arguments with the given path.
        """

        return os.path.join(self.path, *args)

    def exists(self) -> bool:
        """
        Checks if the given file path exists.
        """

        return os.path.isfile(self.path)

    def get_size(self) -> int:
        """
        Provides the size (in bytes) of the
        given file path.
        """

        return os.stat(self.path).st_size

    def is_empty(self) -> bool:
        """
        Checks if the given file path is empty.
        """

        return self.get_size() <= 0

    def delete(self) -> "FileHelper":
        """
        Deletes the given file path if it exists.
        """

        if self.exists():
            os.remove(self.path)
        return self

    def write(
        self, data: Any, *, overwrite: bool = False, encoding: str = "utf-8"
    ) -> "FileHelper":
        """
        Write the given data into the given file path.

        :param data: The data to write.
        :param encoding: The encoding to use while opening the file.
        """

        if overwrite or not self.exists():
            DirectoryHelper(os.path.dirname(self.path)).create()

            with self.open("w", encoding=encoding) as file_stream:
                file_stream.write(data)
        else:
            with self.open("a", encoding=encoding) as file_stream:
                file_stream.write(data)

        return self

    def read(self, *, encoding: str = "utf-8") -> Optional[str]:
        """
        Read the given file path and return it's content.

        :param str encoding: The encoding to use.
        """

        data = None

        if self.exists():
            with self.open("r", encoding=encoding) as file_stream:
                data = file_stream.read()

        return data

    def read_bytes(self) -> Optional[bytes]:
        """
        Read the given file ath and returns it's bytes contetn.
        """

        data = None

        if self.exists():
            with self.open("rb") as file_stream:
                data = file_stream.read()

        return data

    def open(self, *args, **kwargs) -> "open":
        """
        A wrapper for the built-in :py:class:`open` function.
        """

        return open(self.path, *args, **kwargs)

    def copy(self, destination: str) -> "FileHelper":
        """
        Copy the globaly given file path to the given destination.

        :param str destination: The destination of the copy.
        """

        if self.exists():
            shutil.copy(self.path, destination)

        return self

    def move(self, destination) -> "FileHelper":
        """
        Move the globally given file path to the given destination.

        :param str destination: The destination of the file.
        """

        if self.exists():
            shutil.move(self.path, destination)

        return self
