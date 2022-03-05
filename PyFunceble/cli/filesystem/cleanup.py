"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to the cleanup of the filesystem.

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
from typing import List

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.cli.utils.testing
import PyFunceble.sessions
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.database.sqlalchemy.all_schemas import Continue, Inactive
from PyFunceble.helpers.file import FileHelper


class FilesystemCleanup(FilesystemDirBase):
    """
    Provides the interface for the cleanup of the filesystem.
    """

    file_helper: FileHelper = FileHelper()

    def clean_database(self) -> "FilesystemCleanup":
        """
        Cleanups the uneeded data that were stored in the database.

        .. warning::
            This method cleans everything except the WHOIS records.
        """

        if (
            PyFunceble.cli.facility.CredentialLoader.is_already_loaded()
            and self.db_session
        ):
            to_clean = [Continue, Inactive]

            for orm_obj in to_clean:
                # pylint: disable=line-too-long
                with PyFunceble.cli.factory.DBSession.get_db_session() as db_session:
                    db_session.query(orm_obj).delete(synchronize_session=False)
                    db_session.commit()

                    PyFunceble.facility.Logger.info(
                        "Deleted all entries in %r.", orm_obj
                    )

    @property
    def output_files_to_delete(self) -> List[str]:
        """
        Provides the list of output files to delete.
        """

        result = []
        files_to_ignore = [".gitignore", ".keep", ".gitkeep"]

        for root, _, files in os.walk(self.get_output_basedir()):
            for file in files:
                if file in files_to_ignore:
                    continue

                result.append(os.path.join(root, file))

        return result

    def clean_output_files(self) -> "FilesystemCleanup":
        """
        Cleanups the unneeded files from the output directory.
        """

        for file in self.output_files_to_delete:
            self.file_helper.set_path(file).delete()

            PyFunceble.facility.Logger.debug("Deleted: %r.", file)

        return self

    def start(self) -> "FilesystemCleanup":
        """
        Starts the cleanup of everything unneeded.
        """

        self.clean_output_files()

        return self
