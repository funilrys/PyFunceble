"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our WHOIS record migrator.

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

import domain2idna

import PyFunceble.cli.factory
import PyFunceble.facility
import PyFunceble.sessions
from PyFunceble.cli.migrators.mariadb.base import MariaDBMigratorBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.database.sqlalchemy.all_schemas import WhoisRecord


class WhoisRecordIDNASubjectMigrator(MariaDBMigratorBase):
    """
    Provides the interface which provides the completion of the missing
    IDNA subject column.
    """

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to process.
        """

        if PyFunceble.cli.facility.CredentialLoader.is_already_loaded():
            # pylint: disable=singleton-comparison
            return (
                self.db_session.query(WhoisRecord)
                .filter(WhoisRecord.idna_subject == None)
                .first()
                is not None
            )
        return False

    @MariaDBMigratorBase.execute_if_authorized(None)
    def migrate(self) -> "WhoisRecordIDNASubjectMigrator":
        # pylint: disable=singleton-comparison

        broken = False

        for row in self.db_session.query(WhoisRecord).filter(
            WhoisRecord.idna_subject == None
        ):
            if (
                self.continuous_integration
                and self.continuous_integration.is_time_exceeded()
            ):
                broken = True
                break

            PyFunceble.facility.Logger.info(
                "Started to fix idna_subject field of %r", row.subject
            )
            row.idna_subject = domain2idna.domain2idna(row.subject)

            self.db_session.add(row)

            if self.print_action_to_stdout:
                print_single_line()

            PyFunceble.facility.Logger.info(
                "Finished to fix idna_subject field of %r", row.subject
            )

        self.db_session.commit()

        if not broken:
            self.done = True

        return self
