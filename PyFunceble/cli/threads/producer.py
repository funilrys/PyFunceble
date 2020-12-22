"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to generate outputs.

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

import datetime
import os
import queue
from typing import Optional

import domain2idna
from sqlalchemy.exc import IntegrityError

import PyFunceble.checker.utils.whois
import PyFunceble.cli.storage
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.filesystem.counter import FilesystemCounter
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.filesystem.printer.stdout import StdoutPrinter
from PyFunceble.cli.filesystem.status_file import StatusFileGenerator
from PyFunceble.cli.threads.base import ThreadsBase
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.dataset.whois.base import WhoisDatasetBase


class ProducerThread(ThreadsBase):
    """
    Provides our producer thread logic.

    The thread behind this object, will read :code:`the_queue`, and procude
    the outputs.
    """

    thread_name: str = "pyfunceble_producer"

    status_file_generator: Optional[StatusFileGenerator] = None
    stdout_printer: Optional[StdoutPrinter] = None
    file_printer: Optional[FilePrinter] = None
    counter: Optional[FilesystemCounter] = None

    whois_dataset: Optional[WhoisDatasetBase] = None
    inactive_dataset: Optional[InactiveDatasetBase] = None

    header_already_printed: bool = False

    block_printer: bool = False
    """
    We use this variable to block the printing if the subject was already and
    is still inactive.

    .. note::
        This variable should be reseted to :py:class:`False` before reading
        the queue.

    .. warning::
        You should never use this variable in your statement if not
        for anything related to the stdout or file result printers.
    """

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        self.whois_dataset = PyFunceble.checker.utils.whois.get_whois_dataset_object()
        self.inactive_dataset = (
            PyFunceble.cli.utils.testing.get_inactive_dataset_object()
        )

        self.status_file_generator = StatusFileGenerator()
        self.stdout_printer = StdoutPrinter()
        self.file_printer = FilePrinter()
        self.counter = FilesystemCounter()

        super().__init__(output_queue=output_queue)

    @staticmethod
    def run_autosave(test_dataset: dict, test_result: CheckerStatusBase) -> None:
        """
        Reads the given test dataset, interpret it and add the given test
        result to the dataset if needed.

        :param test_dataset:
            The test dataset as per protocol.

        :param test_result_dict:
            The test result object.
        """

        to_save = test_result.to_dict()
        to_save.update(test_dataset)

        continue_object = PyFunceble.cli.utils.testing.get_continue_databaset_object()

        if to_save["output_dir"]:
            # Note: This handles the case that someone try to test a single subject.
            # In fact, we should not generate any file if the output directory
            # is not given.
            #
            # The exception handler is just there to catch the case that the
            # method is not implemented because we are more likely using an
            # alternative backup (for example mariadb).

            try:
                continue_object.set_base_directory(test_dataset["output_dir"])
            except NotImplementedError:
                pass

        try:
            continue_object.update(to_save)
        except TypeError:
            # Example: File generation from non-controlled ressources.
            pass
        except IntegrityError:
            # Example: Trying to add a domain which does not have a destination.
            pass

    def run_stdout_printer(self, test_result: CheckerStatusBase) -> None:
        """
        Runs the stdout printer if necessary.

        :param test_result_dict:
            The test result object.
        """

        if not self.block_printer:
            if not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
                self.stdout_printer.template_to_use = (
                    PyFunceble.cli.utils.stdout.get_template_to_use()
                )

                if not self.header_already_printed:
                    self.stdout_printer.print_header()
                    self.header_already_printed = True

                self.stdout_printer.set_dataset(
                    test_result.to_dict()
                ).print_interpolated_line()
            else:
                PyFunceble.cli.utils.stdout.print_single_line()

    def run_file_printer(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> None:
        """
        Runs the file printer if necessary.

        :param test_dataset:
            The test dataset as per protocol.

        :param test_result_dict:
            The test result object.
        """

        if (
            not self.block_printer
            and test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
        ):
            self.status_file_generator.guess_all_settings()

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

        :param test_dataset:
            The test dataset as per protocol.

        :param test_result_dict:
            The test result object.
        """

        if (
            not self.block_printer
            and test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
        ):
            # Note: We don't want hiden data to be counted.

            self.counter.set_parent_dirname(test_dataset["destination"]).count(
                test_result
            )

    def run_whois_backup(self, test_result: CheckerStatusBase) -> None:
        """
        Runs the WHOIS record backup.

        :param test_result:
            The test result object.
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

    def send_for_mining(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> None:
        """
        Sends the test dataset to the mining queue (if given).
        """

        self.add_to_output_queue((test_dataset, test_result))

    def run_ignored_file_printer(self, test_dataset: dict, test_result: str) -> None:
        """
        Runs the file printer assuming that the given test dataset has been
        ignored by the test runner.
        """

        if (
            test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
            and test_result == "ignored_inactive"
        ):
            if "idna_subject" not in test_dataset:
                # The printer always prints the idna subject.
                test_dataset["idna_subject"] = domain2idna.domain2idna(
                    test_dataset["subject"]
                )

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

    def run_inactive(self, test_dataset: dict, test_result: CheckerStatusBase) -> None:
        """
        Processes the update of a dataset which was previously inactive.

        The idea is that if the status is OK, we just remove it from the
        database. Otherwise, we just keep it in there :-)
        """

        inactive_statuses = (
            PyFunceble.storage.STATUS.down,
            PyFunceble.storage.STATUS.invalid,
        )
        dataset = test_result.to_dict()
        dataset.update(test_dataset)

        PyFunceble.facility.Logger.debug("Test Dataset: %r", test_dataset)
        PyFunceble.facility.Logger.debug("Test Result: %r", test_result)

        if "from_inactive" in dataset:
            if test_result.status in inactive_statuses:
                if dataset["destination"]:
                    # Note: This handles the case that someone try to test a
                    # single subject.
                    # In fact, we should not generate any file if the output
                    # directory is not given.

                    self.inactive_dataset.update(dataset)
                    self.block_printer = True
            else:
                self.inactive_dataset.remove(dataset)
        elif test_result.status in inactive_statuses and dataset["destination"]:
            self.inactive_dataset.update(dataset)

    def target(self) -> None:
        """int
        This is our core logic. Everything starts here!
        """

        stop_message_caught = False

        while True:
            if self.the_queue.empty():
                continue

            consumed = self.the_queue.get()

            PyFunceble.facility.Logger.debug("Got: %r", consumed)

            if consumed == "stop":
                PyFunceble.facility.Logger.info(
                    "Got stop message. Stopping reading from the queue."
                )

                stop_message_caught = True
                break

            if not isinstance(consumed, tuple):
                continue

            PyFunceble.facility.Logger.debug("Got: %r", consumed)

            test_dataset, test_result = consumed
            self.block_printer = False

            if isinstance(test_result, str) and test_result.startswith("ignored_"):
                self.run_ignored_file_printer(test_dataset, test_result)
            else:
                self.send_for_mining(test_dataset, test_result)

                self.run_autosave(test_dataset, test_result)
                self.run_inactive(test_dataset, test_result)

                PyFunceble.facility.Logger.debug(
                    "Printer Blocked: %r", self.block_printer
                )

                ## WARNING: DO NOT RUN PRINTER BEFORE the `run_inactive` or
                ## `run_autosave` methods.

                self.run_stdout_printer(test_result)
                self.run_file_printer(test_dataset, test_result)
                self.run_counter(test_dataset, test_result)
                self.run_whois_backup(test_result)

        if stop_message_caught:
            self.add_to_output_queue("stop")
