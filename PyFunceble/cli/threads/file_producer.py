"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to generate outputs to
the files or other formats.

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

import os
import queue
from typing import Optional

import domain2idna

import PyFunceble.checker.utils.whois
import PyFunceble.cli.storage
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.filesystem.counter import FilesystemCounter
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.filesystem.status_file import StatusFileGenerator
from PyFunceble.cli.threads.producer_base import ProducerThreadBase


class FileProducerThread(ProducerThreadBase):
    """
    Provides our file producer thread logic.

    The thread behind this object, will read :code:`the_queue`, and procude
    the outputs to the files or other storage formats.
    """

    thread_name: str = "pyfunceble_file_producer"

    status_file_generator: Optional[StatusFileGenerator] = None

    file_printer: Optional[FilePrinter] = None
    counter: Optional[FilesystemCounter] = None

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        self.status_file_generator = StatusFileGenerator()
        self.file_printer = FilePrinter()
        self.counter = FilesystemCounter()

        super().__init__(output_queue=output_queue)

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
            test_dataset["destination"]
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
            test_dataset["destination"]
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file
        ):
            # Note: We don't want hiden data to be counted.

            self.counter.set_parent_dirname(test_dataset["destination"]).count(
                test_result
            )

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

            if self.should_we_ignore(test_result):
                self.run_ignored_file_printer(test_dataset, test_result)

                continue

            if self.should_we_block_printer(test_dataset, test_result):
                continue

            self.run_file_printer(test_dataset, test_result)
            self.run_counter(test_dataset, test_result)

        if stop_message_caught:
            self.add_to_output_queue("stop")
