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

import os
from typing import Optional, Union

import PyFunceble.cli.storage
from PyFunceble.database.session import DBSession
from PyFunceble.helpers.directory import DirectoryHelper


class FilesystemDirBase:
    """
    Provides a common base for the manipulation of our output directory.
    """

    _parent_dirname: Optional[str] = None
    db_session: Optional[DBSession] = None
    # Setting this to true will let you differ to the inline directory.
    _differ_to_inline: bool = False

    INLINE_DEST: str = "_inline_"

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
    def parent_dirname(self, value: Union[str, None]) -> None:
        """
        Sets the parent dirname. The parent dirname is a directory which
        acts a parent into the output directory.

        :parm value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str` or :py:class:`None`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, (str, type(None))):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if value is not None and not value:
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

    @property
    def differ_to_inline(self) -> bool:
        """
        Provides the current state of the :code:`_differ_to_inline` attribute.
        """

        return self._differ_to_inline

    @differ_to_inline.setter
    def differ_to_inline(self, value: bool) -> None:
        """
        Allows/Disallow the split to the inline directory. The attribute can be set
        when you want to overwrite the behavior of the :code:`get_output_basedir`
        method.

        :parm value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._differ_to_inline = value

    def set_differ_to_inline(self, value: bool) -> "FilesystemDirBase":
        """
        Allows/Disallow the split to the inline directory. The attribute can be set
        when you want to overwrite the behavior of the :code:`get_output_basedir`
        method.

        :parm value:
            The value to set.
        """

        self.differ_to_inline = value

        return self

    def get_output_basedir(self) -> str:
        """
        Provides the output base directory.

        :param create_if_missing:
            Authorizes the creation of the directory if it's missing.
        """

        if self.parent_dirname:
            result = os.path.join(
                PyFunceble.cli.storage.OUTPUT_DIRECTORY, self.parent_dirname
            )
        elif self.differ_to_inline:
            result = os.path.join(
                PyFunceble.cli.storage.OUTPUT_DIRECTORY, self.INLINE_DEST
            )
        else:
            result = PyFunceble.cli.storage.OUTPUT_DIRECTORY

        DirectoryHelper(result).create()
        return result
