"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the migrator of the :code:`pyfunceble_file` and `pyfunceble_status`
tables.

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

import domain2idna
from sqlalchemy.sql import text

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.sessions
import PyFunceble.storage
from PyFunceble.cli.migrators.mariadb.base import MariaDBMigratorBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.cli.utils.testing import get_destination_from_origin


class FileAndStatusMigrator(MariaDBMigratorBase):
    """
    Provides the interface which provides the migration of the
    :code:`pyfunceble_file` and :code:`pyfunceble_status`.
    """

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to process.
        """

        if PyFunceble.cli.facility.CredentialLoader.is_already_loaded():
            for table in ["pyfunceble_file", "pyfunceble_status"]:
                if self.does_table_exists(table):
                    return True

        return False

    @MariaDBMigratorBase.execute_if_authorized(None)
    def migrate(self) -> "FileAndStatusMigrator":
        inactive_statuses = (
            PyFunceble.storage.STATUS.down,
            PyFunceble.storage.STATUS.invalid,
        )

        inactive_dataset = PyFunceble.cli.utils.testing.get_inactive_dataset_object()
        continue_dataset = PyFunceble.cli.utils.testing.get_continue_databaset_object()

        drop_table = True

        for file_info in self.get_rows("SELECT * from pyfunceble_file"):
            if (
                self.continuous_integration
                and self.continuous_integration.is_time_exceeded()
            ):
                drop_table = False
                break

            destination = get_destination_from_origin(file_info["path"])

            for status in self.get_rows(
                f"SELECT * from pyfunceble_status WHERE file_id = {file_info['id']}"
            ):
                if (
                    self.continuous_integration
                    and self.continuous_integration.is_time_exceeded()
                ):
                    drop_table = False
                    break

                to_send = {
                    "idna_subject": domain2idna.domain2idna(status["tested"]),
                    "checker_type": "AVAILABILITY",
                    "destination": destination,
                    "source": file_info["path"],
                    "tested_at": status["tested_at"],
                    "session_id": None,
                }

                if status["status"] in inactive_statuses:
                    inactive_dataset.update(to_send)

                    if self.print_action_to_stdout:
                        print_single_line()

                PyFunceble.facility.Logger.debug("Dataset: %r", to_send)

                continue_dataset.update(to_send)

                if self.print_action_to_stdout:
                    print_single_line()

                PyFunceble.facility.Logger.info(
                    "Added %r into %r", to_send["idna_subject"], continue_dataset
                )

                # pylint: disable=line-too-long
                self.db_session.execute(
                    text(f"DELETE from pyfunceble_status WHERE id = {status['id']}")
                )
                self.db_session.commit()

                PyFunceble.facility.Logger.debug(
                    "Deleted from pyfunceble_status: \n%r", status
                )

            if drop_table:
                # pylint: disable=line-too-long
                self.db_session.execute(
                    text(f"DELETE from pyfunceble_file WHERE id = {file_info['id']}")
                )
                self.db_session.commit()

                PyFunceble.facility.Logger.debug(
                    "Deleted from pyfunceble_file: \n%r", file_info
                )
            else:
                PyFunceble.facility.Logger.debug(
                    "Not deleted from pyfunceble_file (not authorized): \n%r", file_info
                )

        if drop_table:
            self.db_session.execute(text("DROP TABLE pyfunceble_file"))
            self.db_session.commit()

            PyFunceble.facility.Logger.debug("Deleted pyfunceble_file table.")

            self.db_session.execute(text("DROP TABLE pyfunceble_status"))
            self.db_session.commit()

            PyFunceble.facility.Logger.debug("Deleted pyfunceble_status table.")

            self.done = True
        else:
            PyFunceble.facility.Logger.debug(
                "No table deleted. Reason: not authorized."
            )

        return self
