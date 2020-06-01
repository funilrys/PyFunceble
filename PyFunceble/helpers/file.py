"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

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

from os import path, remove, stat
from shutil import copy as shutil_copy
from shutil import move as shutil_move

from .directory import Directory


class File:
    """
    Simplify the file manipulations.

    :param str file_path: The file path to work with.
    """

    def __init__(self, file_path=None):
        self.path = file_path

    def exists(self, file_path=None):
        """
        Checks if the given file path exists.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        :rtype: bool
        """
        if not file_path:
            file_path = self.path

        return path.isfile(file_path)

    def get_size(self, file_path=None):
        """
        Provides the size (in bytes) of the
        given file path.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        :rtype: int
        """

        if not file_path:
            file_path = self.path

        return stat(file_path).st_size

    def is_empty(self, file_path=None):
        """
        Checks if the given file path is empty.
        """

        return self.get_size(file_path=file_path) <= 0

    def delete(self, file_path=None):
        """
        Deletes the given file path if it exists.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.

        :return: The non existance state of the file.
        :rtype: bool
        """
        if not file_path:
            file_path = self.path

        if self.exists(file_path=file_path):
            remove(file_path)
        return not self.exists(file_path=file_path)

    def write(self, data, overwrite=False, encoding="utf-8", file_path=None):
        """
        Write the given data into the given file path.

        :param str data: The data to write.
        :param str encoding: The encoding to use while opening the file.
        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        """

        if not file_path:
            file_path = self.path

        if isinstance(data, str):
            if overwrite or not self.exists(file_path=file_path):
                Directory(path.dirname(file_path)).create()

                with open(file_path, "w", encoding=encoding) as file_stream:
                    file_stream.write(data)
            else:
                with open(file_path, "a", encoding=encoding) as file_stream:
                    file_stream.write(data)

    def read(self, file_path=None, encoding="utf-8"):
        """
        Read the given file path and return it's content.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        :param str encoding: The encoding to use.
        :rtype: str
        """

        if not file_path:
            file_path = self.path

        data = None

        if self.exists(file_path):
            with open(self.path, "r", encoding=encoding) as file_stream:
                data = file_stream.read()

        return data

    def copy(self, destination):
        """
        Copy the globaly given file path to the given destination.

        :param str destination: The destination of the copy.
        """

        if self.exists(self.path):
            shutil_copy(self.path, destination)

    def move(self, destination):  # pragma: no cover
        """
        Move the globally given file path to the given destination.

        :param str destination: The destination of the file.
        """

        if self.exists(self.path):
            shutil_move(self.path, destination)
