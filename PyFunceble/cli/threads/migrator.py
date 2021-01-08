"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to run all our migrators.

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

import concurrent.futures
import time
from typing import List, Optional

import colorama

import PyFunceble.checker.utils.whois
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.migrators.alembic import Alembic
from PyFunceble.cli.migrators.file_cleanup.hashes_file import HashesFileCleanupMigrator
from PyFunceble.cli.migrators.file_cleanup.mining_file import MiningFileCleanupMigrator
from PyFunceble.cli.migrators.json2csv.inactive import InactiveJSON2CSVMigrator
from PyFunceble.cli.migrators.json2csv.whois import WhoisJSON2CSVMigrator
from PyFunceble.cli.migrators.mariadb.file_and_status import FileAndStatusMigrator
from PyFunceble.cli.migrators.mariadb.whois_record_idna_subject import (
    WhoisRecordIDNASubjectMigrator,
)
from PyFunceble.cli.threads.base import ThreadsBase
from PyFunceble.cli.threads.utils import wait_until_completion
from PyFunceble.helpers.file import FileHelper


class MigratorThread(ThreadsBase):
    """
    Provides our migrator thread logic. The main idea is that we start all our
    migrator inside multiple threads and wait for them to run.
    """

    thread_name: str = "pyfunceble_migrator"

    continuous_integration: Optional[ContinuousIntegrationBase] = None

    @staticmethod
    def done_callback(func: concurrent.futures.Future) -> None:
        """
        This method will be executed after each task run.

        :raise Exception:
            The the task has some exception.
        """

        if func.cancelled():
            PyFunceble.facility.Logger.debug("Cancelled a task")
        elif func.done() and func.exception():
            PyFunceble.facility.Logger.critical(
                "Fatal error while processing migration.",
                exc_info=True,
            )

    def json2csv_inactive_target(self) -> None:
        """
        Provides the target for the inactive database migrator.
        """

        migrator = InactiveJSON2CSVMigrator()
        migrator.continuous_integration = self.continuous_integration

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

    def json2csv_whois_target(self) -> None:
        """
        Provides the target for the whois database migrator.
        """

        migrator = WhoisJSON2CSVMigrator()
        migrator.continuous_integration = self.continuous_integration

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

    def mariadb_whois_record_idna_subject_target(self) -> None:
        """
        Provides the target for the whois addition of the missing
        idna_subject column.
        """

        migrator = WhoisRecordIDNASubjectMigrator()
        migrator.continuous_integration = self.continuous_integration

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

    def mariadb_file_and_status_target(self) -> None:
        """
        Provides the target for the migration of the :code:`pyfunceble_file`
        and :code:`pyfunceble_status` tables.
        """

        migrator = FileAndStatusMigrator()
        migrator.continuous_integration = self.continuous_integration

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

    def hashes_file_cleanup_target(self) -> None:
        """
        Provides the target for the cleanup of the hashes file.
        """

        migrator = HashesFileCleanupMigrator()
        migrator.continuous_integration = self.continuous_integration

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

    def mining_file_cleanup_target(self) -> None:
        """
        Provides the target for the cleanup of the mining file.
        """

        migrator = MiningFileCleanupMigrator()
        migrator.continuous_integration = self.continuous_integration

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

    def target(self) -> None:
        """
        This is our new target.
        """

        # We start the migration (as a standalone)
        Alembic().upgrade()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
            thread_name_prefix=self.thread_name,
        ) as executor:
            submitted_list: List[concurrent.futures.Future] = []

            for method in dir(self):
                if not method.endswith("_target"):
                    continue

                PyFunceble.facility.Logger.info("Submitted %r", method)

                submitted = executor.submit(getattr(self, method))
                submitted.add_done_callback(self.done_callback)
                submitted_list.append(submitted)

            while any(x.running() for x in submitted_list):
                PyFunceble.cli.utils.stdout.print_single_line(".", force=True)
                time.sleep(float(PyFunceble.storage.CONFIGURATION.lookup.timeout))

                if (
                    self.continuous_integration
                    and self.continuous_integration.is_time_exceeded()
                ):
                    break

            if (
                self.continuous_integration
                and self.continuous_integration.is_time_exceeded()
            ):
                for submitted in submitted_list:
                    submitted.cancel()

            wait_until_completion(submitted_list, raise_exc=True)
