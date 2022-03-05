"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the directory helpers.

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

import os
import shutil
from typing import List, Optional

from PyFunceble.helpers.list import ListHelper


class DirectoryHelper:
    """
    Simplify the directories manipulation.

    :param str dir_path the path to work with.
    """

    _path: Optional[str] = None

    def __init__(self, path: Optional[str] = None) -> None:
        if path is not None:
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
        Sets the directory path to work with.

        :param value:
            The path to set.

        :raise TypeError:
            When :code:`value` is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._path = value

    def set_path(self, value: str) -> "DirectoryHelper":
        """
        Sets the directory path to work with.

        :param value:
            The path to set.
        """

        self.path = value

        return self

    @staticmethod
    def get_current(*, with_end_sep: bool = False) -> str:
        """
        Returns the current directory path.

        :param bool with_end_sep:
            Add a directory separator at the end.
        """

        if with_end_sep:
            return os.getcwd() + os.sep
        return os.getcwd()

    @property
    def realpath(self) -> str:
        """
        Returns the real path of the current path.
        """

        return os.path.realpath(self.path)

    def join_path(self, *args) -> str:
        """
        Joins the given arguments with the given path.
        """

        return os.path.join(self.path, *args)

    def exists(self) -> bool:
        """
        Checks if the given directory exists.
        """

        return os.path.isdir(self.path)

    def create(self) -> "DirectoryHelper":
        """
        Creates the given directory path.

        :return: The output of :code:`self.exists` after the directory creation.
        """

        if self.path and not self.exists():
            os.makedirs(self.path)

        return self

    def delete(self) -> "DirectoryHelper":
        """
        Deletes the given directory path.

        :return: :code:`not self.exists` after the directory deletion.
        """

        if self.exists():
            shutil.rmtree(self.path)

        return self

    def list_all_subdirectories(self) -> List[str]:
        """
        Provides the list of all subdirectories of the current path.
        """

        result = []

        if self.exists():
            for root, directories, _ in os.walk(self.path):
                for directory in directories:
                    result.append(os.path.join(root, directory))

        return ListHelper(result).remove_duplicates().sort().subject

    def list_all_files(self) -> List[str]:
        """
        Lists all files of the current path.
        """

        result = []

        if self.exists():
            for directory in self.list_all_subdirectories():
                for element in os.listdir(directory):
                    possible_element = os.path.join(directory, element)

                    if not os.path.isfile(possible_element):
                        continue

                    result.append(possible_element)

        return ListHelper(result).sort().subject
