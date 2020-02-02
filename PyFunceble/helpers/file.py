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
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from os import path, remove, stat
from shutil import copy as shutil_copy
from shutil import move as shutil_move


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
