"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a common base to the manipulation of the output directory.

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
from typing import Optional

import PyFunceble.cli.storage
from PyFunceble.database.session import DBSession


class FilesystemDirBase:
    """
    Provides a common base for the manipulation of our output directory.
    """

    _parent_dirname: Optional[str] = None
    db_session: Optional[DBSession] = None

    def __init__(
        self,
        parent_dirname: Optional[str] = None,
        *,
        db_session: Optional[DBSession] = None,
    ) -> None:
        if parent_dirname is not None:
            self.parent_dirname = parent_dirname
        else:
            self.parent_dirname = PyFunceble.cli.storage.STD_PARENT_DIRNAME

        self.db_session = db_session

    @property
    def parent_dirname(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_parent_dirname` attribute.
        """

        return self._parent_dirname

    @parent_dirname.setter
    def parent_dirname(self, value: str) -> None:
        """
        Sets the parent dirname. The parent dirname is a directory which
        acts a parent into the output directory.

        :parm value:
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

        self._parent_dirname = value

    def set_parent_dirname(self, value: str) -> "FilesystemDirBase":
        """
        Sets the parent dirname. The parent dirname is a directory which
        acts a parent into the output directory.

        :parm value:
            The value to set.
        """

        self.parent_dirname = value

        return self

    def get_output_basedir(self) -> str:
        """
        Provides the output base directory.

        :param create_if_missing:
            Authorizes the creation of the directory if it's missing.
        """

        if self.parent_dirname:
            return os.path.join(
                PyFunceble.cli.storage.OUTPUT_DIRECTORY, self.parent_dirname
            )
        return PyFunceble.cli.storage.OUTPUT_DIRECTORY
