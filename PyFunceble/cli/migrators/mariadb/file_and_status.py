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
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

import domain2idna

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.cli.utils.testing
import PyFunceble.storage
from PyFunceble.cli.migrators.mariadb.base import MariaDBMigratorBase
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

        for file_info in self.get_rows("SELECT * from pyfunceble_file"):
            destination = get_destination_from_origin(file_info["path"])

            for status in self.get_rows(
                f"SELECT * from pyfunceble_status WHERE file_id = {file_info['id']}"
            ):
                to_send = {
                    "idna_subject": domain2idna.domain2idna(status["tested"]),
                    "checker_type": "AVAILABILITY",
                    "destination": destination,
                    "source": file_info["path"],
                    "tested_at": status["tested_at"],
                }

                if status["status"] in inactive_statuses:
                    inactive_dataset.update(to_send)

                continue_dataset.update(to_send)

                # pylint: disable=line-too-long
                with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
                    db_session.execute(
                        f"DELETE from pyfunceble_status WHERE id = {status['id']}"
                    )
                    db_session.commit()

            with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
                db_session.execute(
                    f"DELETE from pyfunceble_file WHERE id = {file_info['id']}"
                )
                db_session.commit()

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            db_session.execute("DROP TABLE pyfunceble_file")
            db_session.commit()

        with PyFunceble.cli.factory.DBSession.get_new_db_session() as db_session:
            db_session.execute("DROP TABLE pyfunceble_status")
            db_session.commit()

        return self
