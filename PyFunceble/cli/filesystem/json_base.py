"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a base for the manipulation of JSON files.

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

import copy
import functools
import os
from typing import Dict, Optional, Union

from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper


class FilesystemJSONBase(FilesystemDirBase):
    """
    A base interface for the manipulation of JSON files.
    """

    dataset: Dict[str, int] = {}
    source_file_path: Optional[str] = None

    SOURCE_FILE: Optional[str] = None
    STD_DATASET: Union[dict, list] = {}

    def update_source_file_path_beforehand(func):  # pylint: disable=no-self-argument
        """
        Updates the source file before launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.source_file_path = os.path.join(
                self.get_output_basedir(), self.SOURCE_FILE
            )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def fetch_dataset_beforehand(func):  # pylint: disable=no-self-argument
        """
        Updates the dataset to work with before launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.fetch_dataset()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def save_dataset_afterwards(func):  # pylint: disable=no-self-argument
        """
        Saves the dataset after launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.save_dataset()

            return result

        return wrapper

    @update_source_file_path_beforehand
    def fetch_dataset(self) -> "FilesystemJSONBase":
        """
        Fetch the dataset from the source file.
        """

        file_helper = FileHelper(self.source_file_path)

        if file_helper.exists():
            self.dataset = DictHelper().from_json_file(file_helper.path)
        else:
            self.dataset = copy.deepcopy(self.STD_DATASET)

        return self

    def save_dataset(self) -> "FilesystemJSONBase":
        """
        Saves the current dataset into it's final destination.
        """

        DictHelper(self.dataset).to_json_file(self.source_file_path)

        return self
