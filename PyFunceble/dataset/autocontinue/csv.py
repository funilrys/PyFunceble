"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the CSV management.

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
import os
from datetime import datetime, timezone
from typing import Any, Generator, Optional, Tuple

import PyFunceble.cli.storage
import PyFunceble.facility
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.csv_base import CSVDatasetBase
from PyFunceble.helpers.file import FileHelper


class CSVContinueDataset(CSVDatasetBase, ContinueDatasetBase):
    """
    Provides the interface for the management of the continue
    CSV file.
    """

    source_file: Optional[str] = None

    _base_directory: Optional[str] = None

    def __init__(
        self,
        *,
        authorized: Optional[bool] = None,
        remove_unneeded_fields: Optional[bool] = None,
        base_directory: Optional[str] = None,
    ) -> None:
        if base_directory is not None:
            self.set_base_directory(base_directory)

        super().__init__(
            authorized=authorized, remove_unneeded_fields=remove_unneeded_fields
        )

    def __contains__(self, value: str) -> bool:
        for row in self.get_content():
            try:
                if value == row["idna_subject"]:
                    return True
            except KeyError:
                break

        return False

    def __getattr__(self, value: Any) -> Any:
        raise AttributeError(value)

    def __getitem__(self, value: Any) -> Any:
        raise KeyError(value)

    def update_source_file_afterwards(func):  # pylint: disable=no-self-argument
        """
        Updates the source file before launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.source_file = os.path.join(
                self.base_directory, PyFunceble.cli.storage.AUTOCONTINUE_FILE
            )

            return result

        return wrapper

    @property
    def base_directory(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_base_directory` attribute.
        """

        return self._base_directory

    @base_directory.setter
    @update_source_file_afterwards
    def base_directory(self, value: str) -> None:
        """
        Sets the given base directory.

        :param value:
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

        self._base_directory = value

    def set_base_directory(self, value: str) -> "CSVContinueDataset":
        """
        Sets the given base directory.

        :param value:
            The value to set.
        """

        self.base_directory = value

        return self

    @CSVDatasetBase.execute_if_authorized(None)
    def cleanup(self) -> "CSVContinueDataset":
        """
        Deletes the source file (completely).
        """

        if self.source_file:
            FileHelper(self.source_file).delete()
            PyFunceble.facility.Logger.debug("Deleted: %r", self.source_file)

        return self

    @CSVDatasetBase.execute_if_authorized(None)
    def get_to_test(self, session_id: str) -> Generator[Tuple[str], str, None]:
        min_days = 365.25 * 20

        for data in self.get_filtered_content({"session_id": session_id}):
            if (datetime.now(timezone.utc) - data["tested_at"]).days < min_days:
                continue

            if not data["idna_subject"]:
                continue

            yield data["idna_subject"]
