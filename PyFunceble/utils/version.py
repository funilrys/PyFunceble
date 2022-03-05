"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an interface for version comparison or manipulation.

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

from typing import List, Optional, Tuple

import packaging.version

from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper


class VersionUtility:
    """
    Provides an interface to compare or manipulate a version.

    :param local_version:
        The local version to work with.

    :ivar local_version:
        The version we are currently working with.
    """

    _local_version: Optional[str] = None

    def __init__(self, local_version: Optional[str] = None) -> None:
        if local_version:
            self.local_version = local_version

    @property
    def local_version(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_local_version` attribute.
        """

        return self._local_version

    @local_version.setter
    def local_version(self, value: str) -> None:
        """
        Sets the local version to work with.

        :param value:
            The local version to work with.

        :raise TypeError:
            When :code:`value` is not :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._local_version = value

    @property
    def real_local_version(self) -> str:
        """
        Provides the real local version.
        """

        return self.get_real_parsed_version(self.local_version)

    def set_local_version(self, value: str) -> "VersionUtility":
        """
        Sets the local version to work with.

        :param value:
            The local version to work with.
        """

        self.local_version = value

        return self

    @staticmethod
    def get_splitted(version: str) -> Tuple[List[str], str]:
        """
        Splits the version from its code name.

        :param version:
            The version to split.

        :return:
            A tuple. The first index is the digit part of the version,
            when the second one is the the non-digit part of the
            version.

            As example if :code:`1.0.0. Hello World` is given, this method
            will output:

            ::

                ([1,0,0], " Hello World")
        """

        splitted_version: List[str] = version.split(".")

        def get_version_part() -> List[str]:
            """
            Provides the version part.
            """

            return [x for x in splitted_version if x.isdigit() or x[0].isdigit()]

        def get_codename_part() -> str:
            """
            Provides the codename part.
            """

            try:
                return [
                    x
                    for x in splitted_version
                    if not x.isdigit() and not x[0].isdigit()
                ][0]
            except IndexError:
                return ""

        return get_version_part(), get_codename_part()

    def get_real_parsed_version(self, version: str) -> str:
        """
        Provides the real version to work with.

        :param version:
            The version to parse.
        """

        return ".".join(self.get_splitted(version)[0])

    def literally_compare(self, upstream_version: str) -> bool:
        """
        Compares :code:`new_version` with the given base version.

        :param new_version:
            The new version to compare with.

        :return:
            - :code:`True`: base version == upstream version
            - :code:`False`: base version != upstream version
        """

        return self.local_version == upstream_version

    def is_older_than(self, upstream_version: str) -> bool:
        """
        Compares if the local version is older that the given one.
        """

        return packaging.version.parse(
            self.real_local_version
        ) < packaging.version.parse(self.get_real_parsed_version(upstream_version))

    def is_equal_to(self, upstream_version: str) -> bool:
        """
        Compares if the local version is equal the given one.
        """

        return packaging.version.parse(
            self.real_local_version
        ) == packaging.version.parse(self.get_real_parsed_version(upstream_version))

    def is_recent(self, upstream_version: str) -> bool:
        """
        Compares if the upstream version is older that the given one.
        """

        return packaging.version.parse(
            self.get_real_parsed_version(upstream_version)
        ) < packaging.version.parse(self.real_local_version)

    def is_dev(self) -> bool:
        """
        Checks if the local version is the dev one.
        """

        return self.get_splitted(self.local_version)[-1].strip().startswith("dev")

    def is_master(self) -> bool:
        """
        Checks if the local version is the master one.
        """

        return self.get_splitted(self.local_version)[-1].startswith(" ")

    @staticmethod
    def is_cloned() -> bool:  # pragma: no cover ## Only used by 1 thing for dev.
        """
        Checks if the local version is a cloned (from git) one.
        """

        file_helper = FileHelper()
        directory_helper = DirectoryHelper()

        if not directory_helper.set_path(".git").exists():
            return False

        list_of_files = [
            ".coveragerc",
            ".gitignore",
            "CODE_OF_CONDUCT.rst",
            "CONTRIBUTING.rst",
            "MANIFEST.in",
            "README.rst",
            "requirements.txt",
            "setup.py",
            "version.yaml",
        ]
        list_of_dirs = ["docs", "PyFunceble", "tests", ".github"]

        if not all(file_helper.set_path(x).exists() for x in list_of_files):
            return False

        if not all(directory_helper.set_path(x).exists() for x in list_of_dirs):
            return False

        return True
