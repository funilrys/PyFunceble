"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our producer worker. This is the description of a single producer worker.

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

import datetime
import os
from typing import Any, Optional, Tuple

from domain2idna import domain2idna

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.checker.utils.whois import get_whois_dataset_object
from PyFunceble.cli.filesystem.counter import FilesystemCounter
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.filesystem.printer.stdout import StdoutPrinter
from PyFunceble.cli.filesystem.status_file import StatusFileGenerator
from PyFunceble.cli.processes.workers.base import WorkerBase
from PyFunceble.cli.utils.stdout import get_template_to_use, print_single_line
from PyFunceble.cli.utils.testing import (
    get_continue_databaset_object,
    get_inactive_dataset_object,
)
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.dataset.whois.base import WhoisDatasetBase


class ProducerWorker(WorkerBase):
    """
    Provides our producer worker. The objective of this worker is to provides
    a single worker (or process if you prefer) which will be used to handle
    the production of output to stdout or files.
    """

    STD_NAME: str = "pyfunceble_producer_worker"

    stdout_printer: Optional[StdoutPrinter] = None
    file_printer: Optional[FilePrinter] = None
    whois_dataset: Optional[WhoisDatasetBase] = None
    inactive_dataset: Optional[InactiveDatasetBase] = None
    continue_dataset: Optional[ContinueDatasetBase] = None
    status_file_generator: Optional[StatusFileGenerator] = None
    counter: Optional[FilesystemCounter] = None

    header_already_printed: Optional[bool] = None

    INACTIVE_STATUSES: Tuple[str, ...] = (
        PyFunceble.storage.STATUS.down,
        PyFunceble.storage.STATUS.invalid,
    )

    def __post_init__(self) -> None:
        self.stdout_printer = StdoutPrinter()
        self.file_printer = FilePrinter()
        self.whois_dataset = get_whois_dataset_object(db_session=self.db_session)
        self.inactive_dataset = get_inactive_dataset_object(db_session=self.db_session)
        self.continue_dataset = get_continue_databaset_object(
            db_session=self.db_session
        )
        self.status_file_generator = StatusFileGenerator().guess_all_settings()
        self.counter = FilesystemCounter()

        self.header_already_printed = False

        return super().__post_init__()

    @staticmethod
    def should_we_ignore(test_result: CheckerStatusBase) -> bool:
        """
        Checks if we should ignore the given datasets.

        :param test_result:
            The test result to check.
        """

        return isinstance(test_result, str) and test_result.startswith("ignored_")

    @staticmethod
    def should_we_print_status_to_stdout(status: str) -> bool:
        """
        Checks if we are allows to print the given status (to stdout).

        :param status:
            The status to check.
        """

        if isinstance(
            PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.status, list
        ):
            to_keep = PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.status
        else:
            to_keep = [PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.status]

        to_keep = [x.upper() for x in to_keep]
        status = status.upper()

        return "ALL" in to_keep or status in to_keep

    def should_we_block_status_file_printer(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> bool:
        """
        Checks if we should block the file printer.

        The reason behindn this is that we don't want to generate an output
        when a subject was already into the inactive database.
        """

        return (
            "from_inactive" in test_dataset
            and test_result.status in self.INACTIVE_STATUSES
        )

    def run_stdout_printer(self, test_result: CheckerStatusBase) -> None:
        """
        Runs the stdout printer (if necessary).

        :param test_result:
            The rest result dataset.
        """

        if not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
            # pylint: disable=line-too-long

            if self.should_we_print_status_to_stdout(test_result.status):
                self.stdout_printer.template_to_use = get_template_to_use()

                if not self.header_already_printed:
                    self.stdout_printer.print_header()
                    self.header_already_printed = True

                self.stdout_printer.set_dataset(
                    test_result.to_dict()
                ).print_interpolated_line()
            else:
                print_single_line()
        else:
            print_single_line()

    def run_whois_backup(self, test_result: CheckerStatusBase) -> None:
        """
        Runs the backup or update of the WHOIS record in our dataset storage.

        :param test_result:
            The test result.
        """

        if (
            hasattr(test_result, "expiration_date")
            and test_result.expiration_date
            and test_result.whois_record
        ):
            # Note: The whois record is always given if the status does not come
            # from the database.

            self.whois_dataset.update(
                {
                    "subject": test_result.subject,
                    "idna_subject": test_result.idna_subject,
                    "expiration_date": test_result.expiration_date,
                    "epoch": str(
                        datetime.datetime.strptime(
                            test_result.expiration_date, "%d-%b-%Y"
                        ).timestamp()
                    ),
                }
            )

    def run_inactive_backup(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> None:
        """
        Runs the backup or update of the Inactive dataset storage.

        The idea is that if the status is OK (active), we just remove it from
        the dataset storage. Otherwise, we just keep it in there :-)
        """

        if test_dataset["type"] != "single":
            dataset = test_result.to_dict()
            dataset.update(test_dataset)

            PyFunceble.facility.Logger.debug("Test Dataset: %r", test_dataset)
            PyFunceble.facility.Logger.debug("Test Result: %r", test_result)

            if "from_inactive" in dataset:
                if test_result.status in self.INACTIVE_STATUSES:
                    if dataset["destination"]:
                        # Note: This handles the case that someone try to test a
                        # single subject.
                        # In fact, we should not generate any file if the output
                        # directory is not given.
                        self.inactive_dataset.update(dataset)
                else:
                    self.inactive_dataset.remove(dataset)
            elif (
                test_result.status in self.INACTIVE_STATUSES and dataset["destination"]
            ):
                self.inactive_dataset.update(dataset)

    def run_continue_backup(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> None:
        """
        Runs the backup or update of the auto-continue dataset storage.
        """

        if test_dataset["type"] != "single":
            dataset = test_result.to_dict()
            dataset.update(test_dataset)

            if (
                isinstance(self.continue_dataset, CSVContinueDataset)
                and dataset["output_dir"]
            ):
                # Note: This handles the case that someone try to test a single subject.
                # In fact, we should not generate any file if the output directory
                # is not given.
                #
                # The exception handler is just there to catch the case that the
                # method is not implemented because we are more likely using an
                # alternative backup (for example mariadb).

                self.continue_dataset.set_base_directory(dataset["output_dir"])
            self.continue_dataset.update(dataset)

    def run_ignored_file_printer(self, test_dataset: dict, test_result: str) -> None:
        """
        Runs the analytic behind the file printer.

        .. warning::
            Thie method assume that the givne dataset is ignored from the normal
            file printer.
        """

        if (
            test_result == "ignored_inactive"
            and test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
        ):
            if "idna_subject" not in test_dataset:
                # The printer always prints the idna subject.
                test_dataset["idna_subject"] = domain2idna(test_dataset["subject"])

            # We use this object just to get the output directory :-)
            self.status_file_generator.set_parent_dirname(test_dataset["destination"])

            # We now generate the file which let the end-user know that
            # we ignored the test of the current test dataset because there
            # is no need to retest it yet.
            # pylint: disable=line-too-long
            self.file_printer.destination = os.path.join(
                self.status_file_generator.get_output_basedir(),
                PyFunceble.cli.storage.OUTPUTS.logs.directories.parent,
                PyFunceble.cli.storage.OUTPUTS.logs.filenames.inactive_not_retested,
            )

            self.file_printer.template_to_use = "plain"
            self.file_printer.dataset = test_dataset
            self.file_printer.print_interpolated_line()

    def run_status_file_printer(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> None:
        """
        Runs the status file printer.
        """

        if (
            test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
        ):
            previous_allow_hosts_file = self.status_file_generator.allow_hosts_files
            previous_allow_plain_file = self.status_file_generator.allow_plain_files

            self.status_file_generator.parent_dirname = test_dataset["destination"]
            self.status_file_generator.status = test_result
            self.status_file_generator.test_dataset = test_dataset

            if test_dataset["subject_type"] == "url":
                self.status_file_generator.allow_hosts_files = False
                self.status_file_generator.allow_plain_files = True

            self.status_file_generator.start()
            self.status_file_generator.allow_hosts_files = previous_allow_hosts_file
            self.status_file_generator.allow_plain_files = previous_allow_plain_file

    def run_counter(self, test_dataset: dict, test_result: CheckerStatusBase) -> None:
        """
        Runs the counter of the current file.
        """

        if (
            test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
        ):
            # Note: We don't want hiden data to be counted.

            self.counter.set_parent_dirname(test_dataset["destination"]).count(
                test_result
            )

    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        if not isinstance(consumed, tuple):
            PyFunceble.facility.Logger.info(
                "Skipping latest dataset because consumed data was not a tuple."
            )
            return None

        # Just for human brain.
        test_dataset, test_result = consumed

        if not isinstance(test_dataset, dict):
            PyFunceble.facility.Logger.info(
                "Skipping because test dataset is not a dictionnary."
            )
            return None

        if self.should_we_ignore(test_result):
            PyFunceble.facility.Logger.info(
                "Ignored test dataset. Reason: No output wanted."
            )
            self.run_ignored_file_printer(test_dataset, test_result)
            return None

        if not isinstance(consumed[1], CheckerStatusBase):
            PyFunceble.facility.Logger.info(
                "Skipping latest dataset because consumed status is not "
                "a status object.."
            )
            return None

        self.run_whois_backup(test_result)
        self.run_inactive_backup(test_dataset, test_result)
        self.run_continue_backup(test_dataset, test_result)

        if not self.should_we_block_status_file_printer(test_dataset, test_result):
            self.run_status_file_printer(test_dataset, test_result)
            self.run_counter(test_dataset, test_result)

        self.run_stdout_printer(test_result)
        test_dataset["from_producer"] = True

        return test_dataset, test_result
