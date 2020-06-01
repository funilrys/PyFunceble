"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

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

from os import getcwd, makedirs, path
from os import sep as directory_separator
from shutil import rmtree


class Directory:
    """
    Simplify the directories manipulation.

    :param str dir_path the path to work with.
    """

    def __init__(self, dir_path=None):
        self.path = dir_path

    @classmethod
    def get_current(cls, with_end_sep=False):
        """
        Returns the current directory path.

        :param bool with_end_sep:
            Add a directory separator at the end.
        """

        if with_end_sep:
            return getcwd() + directory_separator
        return getcwd()  # pragma: no cover

    def fix_path(self, dir_path=None, splited_path=None):
        """
        Fix the path of the given path.

        .. note::
            We consider a path as fixed if it ends with the right
            directory separator.
        """

        if not dir_path:
            dir_path = self.path

        if not splited_path:
            if dir_path:
                # The parsed directory is not empty or equal to None.

                # We initate a variable which will save the splited path.
                split_path = []

                if "/" in dir_path:
                    # We split the separator.
                    split_path = dir_path.split("/")
                elif "\\" in dir_path:
                    # We split the separator.
                    split_path = dir_path.split("\\")
                else:
                    split_path = [dir_path]
                # We join the splited element with the directory separator as glue.
                return self.fix_path(splited_path=[x for x in split_path if x])

            # We return the directory.
            return dir_path
        return directory_separator.join(splited_path) + directory_separator

    def exists(self, dir_path=None):
        """
        Checks if the given directory exists.
        """

        if not dir_path:
            dir_path = self.path

        return path.isdir(dir_path)

    def create(self, dir_path=None):  # pragma: no cover
        """
        Creates the given directory path.

        :return: The output of :code:`self.exists` after the directory creation.
        :rtype: bool
        """

        if not dir_path:
            dir_path = self.path

        try:
            if dir_path and not self.exists(dir_path=dir_path):
                makedirs(dir_path)
        except FileExistsError:
            pass

        return self.exists(dir_path=dir_path)

    def delete(self, dir_path=None):  # pragma: no cover
        """
        Deletes the given directory path.

        :return: :code:`not self.exists` after the directory deletion.
        :rtypt: bool
        """

        if not dir_path:
            dir_path = self.path

        if self.exists(dir_path=dir_path):
            rmtree(dir_path)

        return not self.exists(dir_path=dir_path)
