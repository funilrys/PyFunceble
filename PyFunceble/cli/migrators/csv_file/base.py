"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all CSV file-s migrators.

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

import csv
import functools
import tempfile
from typing import List, Optional

import PyFunceble.facility
from PyFunceble.cli.migrators.base import MigratorBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.helpers.file import FileHelper


class CSVFileMigratorBase(MigratorBase):
    """
    Provides the base of all CSV file migrator classes.
    """

    source_file: Optional[str] = None

    FIELDS: Optional[List[str]] = None

    TO_DELETE: Optional[List[str]] = None
    TO_ADD: Optional[List[str]] = None

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
    def migrate(self) -> "MigratorBase":
        """
        Provides the migrator (itself).
        """

        file_helper = FileHelper(self.source_file)

        if file_helper.exists():
            with file_helper.open("r", encoding="utf-8") as file_stream:
                first_line = next(file_stream)

            if any(x in first_line for x in self.TO_DELETE) or any(
                x not in first_line for x in self.TO_ADD
            ):
                temp_destination = tempfile.NamedTemporaryFile(
                    "a+", newline="", encoding="utf-8", delete=False
                )

                file_handler = file_helper.open(newline="")
                reader = csv.DictReader(file_handler)
                writer = csv.DictWriter(
                    temp_destination,
                    fieldnames=[x for x in self.FIELDS if x not in self.TO_DELETE]
                    + [x for x in self.TO_ADD if x not in self.FIELDS],
                )
                writer.writeheader()

                keys_found = False
                for row in reader:
                    row = dict(row)

                    for key in self.TO_DELETE:
                        if key in row:
                            del row[key]
                            keys_found = True

                    for key in self.TO_ADD:
                        if key not in row:
                            row[key] = ""
                            keys_found = True

                    writer.writerow(row)

                    if not keys_found:
                        break

                    writer.writerow(row)

                    if self.print_action_to_stdout:
                        print_single_line()

                temp_destination.seek(0)

                FileHelper(temp_destination.name).move(self.source_file)

        self.done = True

    def start(self) -> "MigratorBase":
        """
        Starts the migration and everything related to it.
        """

        PyFunceble.facility.Logger.info("Started migration.")

        self.migrate()

        PyFunceble.facility.Logger.info("Finished migration.")

        return self
