"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all directory structure classes.

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
from typing import Optional

try:
    import importlib.resources as package_resources
except ImportError:  # pragma: no cover ## Retro compatibility
    import importlib_resources as package_resources


import PyFunceble.storage
from PyFunceble.cli.filesystem.cleanup import FilesystemCleanup
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase


class DirectoryStructureBase(FilesystemDirBase):
    """
    Provides the base of all dir structure classes.
    """

    std_source_file: Optional[str] = None

    _source_file: Optional[str] = None

    def __init__(
        self, parent_dirname: Optional[str] = None, source_file: Optional[str] = None
    ) -> None:
        with package_resources.path(
            "PyFunceble.data.infrastructure",
            PyFunceble.storage.DISTRIBUTED_DIR_STRUCTURE_FILENAME,
        ) as file_path:
            self.std_source_file = str(file_path)

        if source_file is not None:
            self.source_file = source_file
        else:
            self.source_file = self.std_source_file

        super().__init__(parent_dirname=parent_dirname)

    @property
    def source_file(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_source_file` attribute.
        """

        return self._source_file

    @source_file.setter
    def source_file(self, value: str) -> None:
        """
        Sets the value of the source file to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given value is not a :py:class:`str`.
        :raise ValueError:
            When the given value is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._source_file = value

    def set_source_file(self, value: str) -> "DirectoryStructureBase":
        """
        Sets the value of the source file to use.

        :param value:
            The value to set.
        """

        self.source_file = value

        return self

    def get_path_without_base_dir(self, full_path: str) -> str:
        """
        Given a full path, we remove the base dir.
        """

        to_replace = os.path.join(self.get_output_basedir(), "")

        return full_path.replace(to_replace, "")

    def cleanup(self) -> "DirectoryStructureBase":
        """
        Cleans the output directory.
        """

        FilesystemCleanup(self.parent_dirname).clean_output_files()

        return self

    def get_backup_data(self) -> dict:
        """
        Provides the data to manipulate.
        """

        raise NotImplementedError()

    def start(self) -> "DirectoryStructureBase":
        """
        Starts the whole process.
        """

        raise NotImplementedError()
