"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all cleanup migrators.

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

import functools
from typing import Optional

import PyFunceble.facility
from PyFunceble.cli.migrators.base import MigratorBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.helpers.file import FileHelper


class FileClenupMigratorBase(MigratorBase):
    """
    Provides the base of all file cleanup related migration classes.
    """

    source_file: Optional[str] = None

    def ensure_source_file_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the source file is given before launching the decorated
        method.

        :raise RuntimeError:
            When the:code:`self.source_file` is not given.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.source_file, str):
                raise RuntimeError("<self.source_file> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @ensure_source_file_is_given
    def migrate(self) -> "FileClenupMigratorBase":
        """
        Provides the migrator (itself)
        """

        FileHelper(self.source_file).delete()

        PyFunceble.facility.Logger.debug("Deleted: %r", self.source_file)
        self.done = True

        if self.print_action_to_stdout:
            print_single_line()

    def start(self) -> "FileClenupMigratorBase":
        """
        Starts the migration and everything related to it.
        """

        PyFunceble.facility.Logger.info("Started migration.")

        self.migrate()

        PyFunceble.facility.Logger.info("Finished migration.")

        return self
