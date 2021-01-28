"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the duplicates cleanup.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

from sqlalchemy.exc import StatementError

import PyFunceble

from ..schemas.file import File
from ..schemas.status import Status
from ..schemas.whois_record import WhoisRecord
from .base import MigrationBase


class Duplicates2Single(MigrationBase):
    """
    Provides an interface which will cleanup duplicates in the migrated
    data.

    The reason behind this interface is the fact that we did an error
    in the past which created duplicated in the database.
    """

    @property
    def authorized(self):
        """
        Provides the authorization to run.
        """

        return PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"] and any(
            [self.does_table_exists(x) for x in self.old_tables]
        )

    def __delete(self, db_session, entries):
        """
        Deletes the given entries from the database.
        """

        for row in entries:
            try:
                db_session.delete(row)
                db_session.commit()
            except StatementError:
                pass

            if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                PyFunceble.LOGGER.info(f"Deleted {row}.")
                print(".", end="")
        self.handle_autosaving()

    def process_status_table(self):
        """
        Process the deletion of duplicate into the :code:`pyfunceble_status`
        table.
        """

        with PyFunceble.engine.database.loader.session.Session() as db_session:
            for row in db_session.query(File):
                for status in row.subjects:
                    if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                        PyFunceble.LOGGER.info(
                            f"Checking for duplicate of {status.tested}."
                        )
                        print(".", end="")

                    while True:
                        # pylint: disable=no-member
                        to_delete = (
                            db_session.query(Status)
                            .filter(Status.file_id == row.id)
                            .filter(Status.tested == status.tested)
                            .filter(Status.id != status.id)
                            .limit(20)
                            .all()
                        )

                        if not to_delete:
                            PyFunceble.LOGGER.info(
                                f"Continue. No duplicate (anymore) for {status.tested}."
                            )
                            break

                        self.__delete(
                            db_session,
                            to_delete,
                        )

                self.handle_autosaving()

    def process_whois_record_table(self):
        """
        Process the deletion of duplicate into the :code:`pyfunceble_status`
        table.
        """

        with PyFunceble.engine.database.loader.session.Session() as db_session:
            for row in db_session.query(WhoisRecord):
                if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                    PyFunceble.LOGGER.info(f"Checking for duplicate of {row.subject}.")
                    print(".", end="")

                while True:
                    # pylint: disable=no-member
                    to_delete = (
                        db_session.query(WhoisRecord)
                        .filter(WhoisRecord.subject == row.subject)
                        .filter(WhoisRecord.id != row.id)
                        .limit(20)
                        .all()
                    )

                    if not to_delete:
                        PyFunceble.LOGGER.info(
                            f"Continue. No duplicate (anymore) for {row.subject}."
                        )
                        break

                    self.__delete(
                        db_session,
                        to_delete,
                    )
                self.handle_autosaving()

    def start(self):
        """
        Starts the process.
        """

        if self.authorized:
            self.process_status_table()
            self.process_whois_record_table()
