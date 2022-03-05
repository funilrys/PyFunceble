"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the migrator manager.

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

from typing import Optional

import colorama
from sqlalchemy.orm import Session

import PyFunceble.checker.utils.whois
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.migrators.alembic import Alembic
from PyFunceble.cli.migrators.csv_file.inactive_source_delete import (
    InactiveDatasetDeleteSourceColumnMigrator,
)
from PyFunceble.cli.migrators.csv_file.whois_registrar_add import (
    WhoisDatasetAddRegistrarColumnMigrator,
)
from PyFunceble.cli.migrators.file_cleanup.hashes_file import HashesFileCleanupMigrator
from PyFunceble.cli.migrators.file_cleanup.mining_file import MiningFileCleanupMigrator
from PyFunceble.cli.migrators.file_cleanup.production_config_file import (
    ProductionConfigFileCleanupMigrator,
)
from PyFunceble.cli.migrators.json2csv.inactive import InactiveJSON2CSVMigrator
from PyFunceble.cli.migrators.json2csv.whois import WhoisJSON2CSVMigrator
from PyFunceble.cli.migrators.mariadb.file_and_status import FileAndStatusMigrator
from PyFunceble.cli.migrators.mariadb.whois_record_idna_subject import (
    WhoisRecordIDNASubjectMigrator,
)
from PyFunceble.cli.processes.base import ProcessesManagerBase
from PyFunceble.cli.processes.workers.migrator import MigratorWorker
from PyFunceble.helpers.file import FileHelper


class MigratorProcessesManager(ProcessesManagerBase):
    """
    Provides the migrator manager.
    """

    WORKER_OBJ: MigratorWorker = MigratorWorker

    @staticmethod
    def json2csv_inactive_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the inactive database migrator.
        """

        migrator = InactiveJSON2CSVMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration

        if FileHelper(migrator.source_file).exists():
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                "Started migration (json2csv) of the inactive dataset."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"\n{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    "Finished migration (json2csv) of the inactive dataset."
                )
            else:
                print(
                    f"\n{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    "Unfinished migration (json2csv) of the inactive dataset."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped json2csv_inactive_target. File does not exist."
            )

    @staticmethod
    def json2csv_whois_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the whois database migrator.
        """

        migrator = WhoisJSON2CSVMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration

        if FileHelper(migrator.source_file).exists():
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                "Started migration (json2csv) of the whois dataset."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"\n{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    "Finished migration (json2csv) of the whois dataset."
                )
            else:
                print(
                    f"\n{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    "Unfinished migration (json2csv) of the whois dataset."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped json2csv_whois_target. File does not exist."
            )

    @staticmethod
    def mariadb_whois_record_idna_subject_target(
        continuous_integration: ContinuousIntegrationBase,
        *,
        db_session: Optional[Session] = None,
    ) -> None:
        """
        Provides the target for the whois addition of the missing
        idna_subject column.
        """

        migrator = WhoisRecordIDNASubjectMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration
        migrator.db_session = db_session

        if migrator.authorized:
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                "Started completion of NULL idna_subject(s) into the whois dataset."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    "Finished completion of NULL idna_subject(s) into "
                    "the whois dataset."
                )
            else:
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    "Unfinished completion of NULL idna_subject(s) into "
                    "the whois dataset."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped mariadb_whois_record_idna_subject_target. Not authorized."
            )

    @staticmethod
    def mariadb_file_and_status_target(
        continuous_integration: ContinuousIntegrationBase,
        *,
        db_session: Optional[Session] = None,
    ) -> None:
        """
        Provides the target for the migration of the :code:`pyfunceble_file`
        and :code:`pyfunceble_status` tables.
        """

        migrator = FileAndStatusMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration
        migrator.db_session = db_session

        if migrator.authorized:
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                "Started migration of the pyfunceble_file and "
                "pyfunceble_status tables."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    "Finished migration of the pyfunceble_file and "
                    "pyfunceble_status tables."
                )
            else:
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    "Unfinished migration of the pyfunceble_file and "
                    "pyfunceble_status tables."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped mariadb_file_and_status_target. Not authorized."
            )

    @staticmethod
    def hashes_file_cleanup_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the cleanup of the hashes file.
        """

        migrator = HashesFileCleanupMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration

        if FileHelper(migrator.source_file).exists():
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                f"Started deletion of {migrator.source_file!r}."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    f"Finished deletion of {migrator.source_file!r}."
                )
            else:
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    f"Unfinished deletion of {migrator.source_file!r}."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped hashes_file_cleanup_target. File does not exist."
            )

    @staticmethod
    def production_config_file_cleanup_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the cleanup of the production configuration file.
        """

        migrator = ProductionConfigFileCleanupMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration

        if FileHelper(migrator.source_file).exists():
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                f"Started deletion of {migrator.source_file!r}."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    f"Finished deletion of {migrator.source_file!r}."
                )
            else:
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    f"Unfinished deletion of {migrator.source_file!r}."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped production_config_file_cleanup_target. File does not exist."
            )

    @staticmethod
    def mining_file_cleanup_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the cleanup of the mining file.
        """

        migrator = MiningFileCleanupMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration

        if FileHelper(migrator.source_file).exists():
            print(
                f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                f"Started deletion of {migrator.source_file!r}."
            )

            migrator.start()

            if migrator.done:
                print(
                    f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                    f"Finished deletion of {migrator.source_file!r}."
                )
            else:
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    f"Unfinished deletion of {migrator.source_file!r}."
                )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped hashes_file_cleanup_target. File does not exist."
            )

    @staticmethod
    def csv_file_delete_source_column_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the deletion of the source column.
        """

        migrator = InactiveDatasetDeleteSourceColumnMigrator(
            print_action_to_stdout=True
        )
        migrator.continuous_integration = continuous_integration

        file_helper = FileHelper(migrator.source_file)

        if file_helper.exists():
            with file_helper.open("r", encoding="utf-8") as file_stream:
                first_line = next(file_stream)

            if any(x in first_line for x in migrator.TO_DELETE):
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    "Started deletion of the 'source' column into "
                    f"{migrator.source_file!r}."
                )

                migrator.start()

                if migrator.done:
                    print(
                        f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                        "Finished deletion of the 'source' column into "
                        f"{migrator.source_file!r}."
                    )
                else:
                    print(
                        f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                        "unfinished deletion of the 'source' column into "
                        f"{migrator.source_file!r}."
                    )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped csv_file_delete_source_column_target. File does not exist."
            )

    @staticmethod
    def csv_file_add_registrar_column_target(
        continuous_integration: ContinuousIntegrationBase,
    ) -> None:
        """
        Provides the target for the addition of the registrar column.
        """

        migrator = WhoisDatasetAddRegistrarColumnMigrator(print_action_to_stdout=True)
        migrator.continuous_integration = continuous_integration

        file_helper = FileHelper(migrator.source_file)

        if file_helper.exists():
            with file_helper.open("r", encoding="utf-8") as file_stream:
                first_line = next(file_stream)

            if any(x not in first_line for x in migrator.TO_ADD):
                print(
                    f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                    "Started addition of the 'registrar' column into "
                    f"{migrator.source_file!r}."
                )

                migrator.start()

                if migrator.done:
                    print(
                        f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                        "Finished addition of the 'registrar' column into "
                        f"{migrator.source_file!r}."
                    )
                else:
                    print(
                        f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                        "unfinished addition of the 'registrar' column into "
                        f"{migrator.source_file!r}."
                    )
        else:
            PyFunceble.facility.Logger.info(
                "Stopped csv_file_add_registrar_column_target. File does not exist."
            )

    def create(self) -> "ProcessesManagerBase":
        for method in dir(self):
            if not method.endswith("_target"):
                continue

            worker = MigratorWorker(
                None,
                name=f"pyfunceble_{method}",
                daemon=True,
                continuous_integration=self.continuous_integration,
            )

            worker.target = getattr(self, method)

            self._created_workers.append(worker)
            PyFunceble.facility.Logger.info("Created worker for %r", method)

    @ProcessesManagerBase.ensure_worker_obj_is_given
    @ProcessesManagerBase.create_workers_if_missing
    def start(self) -> "ProcessesManagerBase":
        # We start the migration (as a standalone)
        Alembic(self._created_workers[0].db_session).upgrade()

        return super().start()
