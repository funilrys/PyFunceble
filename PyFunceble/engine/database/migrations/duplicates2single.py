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

from sqlalchemy.exc import StatementError
from sqlalchemy.orm.exc import ObjectDeletedError

import PyFunceble

from ..schemas.file import File
from ..schemas.whois_record import WhoisRecord


class Duplicates2Single:
    """
    Provides an interface which will cleanup duplicates in the migrated
    data.

    The reason behind this interface is the fact that we did an error
    in the past which created duplicated in the database.
    """

    def __init__(self):
        self.autosave = PyFunceble.engine.AutoSave()

    def __delete(self, db_session, entries):
        """
        Deletes the given entries from the database.
        """

        for row in entries:
            try:
                db_session.delete(row)
                db_session.commit()

                if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                    PyFunceble.LOGGER.info(f"Deleted {row}.")
                    print(".", end="")
            except StatementError:
                continue

    def process_status_table(self):
        """
        Process the deletion of duplicate into the :code:`pyfunceble_status`
        table.
        """

        with PyFunceble.engine.database.loader.session.Session() as db_session:
            for row in db_session.query(File):
                subjects = [x.tested for x in row.subjects]

                for status in row.subjects:
                    positions = []

                    for index, subject in enumerate(subjects):
                        try:
                            if subject == status.tested:
                                positions.append(index)
                        except ObjectDeletedError:
                            continue

                    if len(positions) > 1:
                        to_delete = []

                        for position in positions:
                            try:
                                to_delete.append(row.subjects[position])
                            except IndexError:
                                continue

                        self.__delete(db_session, to_delete)

                if self.autosave.is_time_exceed():
                    self.autosave.process()

    def process_whois_record_table(self):
        """
        Process the deletion of duplicate into the :code:`pyfunceble_status`
        table.
        """

        with PyFunceble.engine.database.loader.session.Session() as db_session:
            for row in db_session.query(WhoisRecord):
                # pylint: disable=no-member
                self.__delete(
                    db_session,
                    db_session.query(WhoisRecord)
                    .filter(WhoisRecord.subject == row.subject)
                    .filter(WhoisRecord.id != row.id)
                    .all(),
                )

                if self.autosave.is_time_exceed():
                    self.autosave.process()

    def start(self):
        """
        Starts the process.
        """

        self.process_status_table()
        self.process_whois_record_table()
