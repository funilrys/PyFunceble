"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an interface for the backup of the directory structure.

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

import PyFunceble.cli.storage
from PyFunceble.cli.filesystem.dir_structure.base import DirectoryStructureBase
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.utils.platform import PlatformUtility


class DirectoryStructureRestoration(DirectoryStructureBase):
    """
    Provides the base of all dir structure classes.
    """

    def get_backup_data(self) -> dict:
        """
        Stores the backup at the current destination.
        """

        data = DictHelper().from_json_file(self.source_file)

        if PlatformUtility.is_windows():
            result = {}

            for directory, files in data.items():
                result[os.path.normpath(directory)] = files

            PyFunceble.facility.Logger.debug("Backup (read) data:\n%r", result)

            return result

        PyFunceble.facility.Logger.debug("Backup (read) data:\n%r", data)
        return data

    def restore_from_backup(self) -> "DirectoryStructureRestoration":
        """
        Restores or reconstruct the output directory.
        """

        # pylint: disable=too-many-locals

        PyFunceble.facility.Logger.info(
            "Started restoration of the directory structure"
        )

        backup = self.get_backup_data()

        base_dir = self.get_output_basedir()
        dir_helper = DirectoryHelper()
        file_helper = FileHelper()

        if dir_helper.set_path(base_dir).exists():
            for root, _, files in os.walk(dir_helper.path):
                reduced_path = self.get_path_without_base_dir(root)

                if reduced_path not in backup and root != reduced_path:

                    dir_helper.set_path(root).delete()

                    PyFunceble.facility.Logger.debug(
                        "Added %r into the list of directories to delete. "
                        "Reason: not found in own dataset.",
                        root,
                    )
                    continue

        for directory, files in backup.items():
            dir_helper.set_path(os.path.join(base_dir, directory)).create()

            for file, dataset in files.items():
                file_full_path = os.path.join(dir_helper.path, file)

                if (
                    file == ".gitignore"
                    and PyFunceble.cli.storage.STD_PARENT_DIRNAME not in file_full_path
                ):
                    to_delete = file_full_path

                    file_helper.set_path(to_delete).delete()

                    PyFunceble.facility.Logger.debug(
                        "(If exists) Deleted: %r. Reason: We are going to "
                        "replace it with .gitkeep",
                        to_delete,
                    )

                    file_full_path = file_full_path.replace(".gitignore", ".gitkeep")

                file_helper.set_path(file_full_path)

                if not file_helper.exists():
                    file_helper.write(dataset["content"], overwrite=True)

        PyFunceble.facility.Logger.info(
            "Finished restoration of the directory structure"
        )

        return self

    def start(self) -> "DirectoryStructureRestoration":
        """
        Starts the restoration process.
        """

        return self.cleanup().restore_from_backup()
