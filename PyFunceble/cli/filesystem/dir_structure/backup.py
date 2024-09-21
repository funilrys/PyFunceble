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

import PyFunceble.facility
from PyFunceble.cli.filesystem.dir_structure.base import DirectoryStructureBase
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.hash import HashHelper


class DirectoryStructureBackup(DirectoryStructureBase):
    """
    Provides the base of all dir structure classes.
    """

    def get_backup_data(self) -> dict:
        """
        Provides the data which acts as a backup.
        """

        result = {}
        base_dir = self.get_output_basedir()
        file_helper = FileHelper()
        hash_helper = HashHelper()

        for file in DirectoryHelper(base_dir).list_all_files():
            file_helper.set_path(file)
            reduced_path = self.get_path_without_base_dir(file)

            directory, filename = reduced_path.rsplit(os.sep, 1)
            file_hash = hash_helper.hash_file(file_helper.path)

            dataset = {filename: {"content": file_helper.read(), "hash": file_hash}}

            if directory not in result:
                result[directory] = dataset
            else:
                result[directory].update(dataset)

        PyFunceble.facility.Logger.debug("Dir Structure to backup:\n%r", result)

        return result

    def store_backup(self) -> "DirectoryStructureBackup":
        """
        Stores the backup at the current destination.
        """

        DictHelper(self.get_backup_data()).to_json_file(self.source_file)

        PyFunceble.facility.Logger.info("Stored backup into: %r", self.source_file)

        return self

    def start(self) -> "DirectoryStructureBackup":
        """
        Starts the backup process.
        """

        return self.cleanup().store_backup()
