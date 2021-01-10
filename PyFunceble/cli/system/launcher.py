"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the system launcher.
From here, it's all about real testing.

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

import argparse
import copy
import datetime
import multiprocessing
import os
import secrets
import sys
from typing import List, Optional

import colorama
import domain2idna

import PyFunceble.checker.utils.whois
import PyFunceble.cli.storage
import PyFunceble.cli.utils.ascii_logo
import PyFunceble.cli.utils.sort
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.continuous_integration.exceptions import StopExecution
from PyFunceble.cli.continuous_integration.utils import ci_object
from PyFunceble.cli.execution_time import ExecutionTime
from PyFunceble.cli.filesystem.cleanup import FilesystemCleanup
from PyFunceble.cli.filesystem.counter import FilesystemCounter
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.cli.filesystem.dir_structure.restore import (
    DirectoryStructureRestoration,
)
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.filesystem.printer.stdout import StdoutPrinter
from PyFunceble.cli.processes.file_sorter import FileSorterProcessesManager
from PyFunceble.cli.processes.migrator import MigratorProcessesManager
from PyFunceble.cli.processes.miner import MinerProcessesManager
from PyFunceble.cli.processes.producer import ProducerProcessesManager
from PyFunceble.cli.processes.tester import TesterProcessesManager
from PyFunceble.cli.system.base import SystemBase
from PyFunceble.cli.utils.version import print_central_messages
from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject
from PyFunceble.converter.input_line2subject import InputLine2Subject
from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject
from PyFunceble.converter.rpz_policy2subject import RPZPolicy2Subject
from PyFunceble.converter.subject2complements import Subject2Complements
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.converter.wildcard2subject import Wildcard2Subject
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.list import ListHelper


class SystemLauncher(SystemBase):
    """
    Provides the system tests launcher.
    """

    testing_protocol: List[dict] = []
    """
    Saves the protocol which we are going to generate.
    The protocol will saves a set of information about what to test,
    what kind of output to produce and most importantly where.
    """

    subject2complements: Subject2Complements = Subject2Complements()
    inputline2subject: InputLine2Subject = InputLine2Subject()
    adblock_inputline2subject: AdblockInputLine2Subject = AdblockInputLine2Subject()
    wildcard2subject: Wildcard2Subject = Wildcard2Subject()
    rpz_policy2subject: RPZPolicy2Subject = RPZPolicy2Subject()
    rpz_inputline2subject: RPZInputLine2Subject = RPZInputLine2Subject()
    url2netloc: Url2Netloc = Url2Netloc()

    stdout_printer: StdoutPrinter = StdoutPrinter()
    file_printer: FilePrinter = FilePrinter()
    counter: FilesystemCounter = FilesystemCounter()

    execution_time_holder: Optional[ExecutionTime] = None

    manager: Optional[multiprocessing.Manager]
    tester_process_manager: Optional[TesterProcessesManager] = None
    producer_process_manager: Optional[ProducerProcessesManager] = None
    miner_process_manager: Optional[MinerProcessesManager] = None
    file_sorter_process_manager: Optional[FileSorterProcessesManager] = None
    migrator_process_manager: Optional[MigratorProcessesManager] = None

    inactive_dataset: Optional[InactiveDatasetBase] = None
    continuous_integration: Optional[ContinuousIntegrationBase] = None

    checker_type: Optional[str] = None

    sessions_id: dict = dict()

    def __init__(self, args: Optional[argparse.Namespace] = None) -> None:
        self.execution_time_holder = ExecutionTime().set_start_time()
        self.checker_type = PyFunceble.cli.utils.testing.get_testing_mode()
        self.inactive_dataset = (
            PyFunceble.cli.utils.testing.get_inactive_dataset_object()
        )
        self.continuous_integration = ci_object()

        if self.continuous_integration.authorized:
            self.continuous_integration.init()

        self.stdout_printer.guess_allow_coloration()

        self.manager = multiprocessing.Manager()

        self.tester_process_manager = TesterProcessesManager(
            self.manager,
            max_worker=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
            continuous_integration=self.continuous_integration,
            daemon=True,
        )
        self.producer_process_manager = ProducerProcessesManager(
            self.manager,
            max_worker=1,
            continuous_integration=self.continuous_integration,
            input_queue=self.tester_process_manager.output_queue,
            daemon=True,
        )
        self.file_sorter_process_manager = FileSorterProcessesManager(
            self.manager,
            max_worker=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
            continuous_integration=self.continuous_integration,
            daemon=True,
        )
        self.migrator_process_manager = MigratorProcessesManager(
            self.manager,
            continuous_integration=self.continuous_integration,
            daemon=True,
            generate_input_queue=False,
            generate_output_queue=False,
        )

        if PyFunceble.storage.CONFIGURATION.cli_testing.mining:
            self.miner_process_manager = MinerProcessesManager(
                self.manager,
                max_worker=1,
                continuous_integration=self.continuous_integration,
                output_queue=self.tester_process_manager.input_queue,
                daemon=True,
            )

            del self.producer_process_manager.output_queue

            self.producer_process_manager.output_queue = (
                self.miner_process_manager.input_queue
            )

        if self.continuous_integration.authorized:
            self.continuous_integration.set_start_time()

        super().__init__(args)

    @staticmethod
    def print_home_ascii() -> None:
        """
        Prints our ASCII home logo.
        """

        if not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
            if PyFunceble.cli.utils.stdout.get_template_to_use() != "simple":
                print(PyFunceble.cli.utils.ascii_logo.get_home_representation())

    @SystemBase.ensure_args_is_given
    def fill_protocol(self) -> "SystemLauncher":
        """
        Fills the protocol with the information about what we are supposed to test.
        """

        filesytem_dirbase = FilesystemDirBase()

        if self.args.domains:
            for domain in self.args.domains:
                to_append = {
                    "type": "single",
                    "subject_type": "domain",
                    "destination": None,
                    "subject": domain,
                    "idna_subject": domain2idna.domain2idna(domain),
                    "source": None,
                    "output_dir": None,
                    "checker_type": self.checker_type,
                    "session_id": None,
                }

                self.testing_protocol.append(to_append)

                PyFunceble.facility.Logger.debug(
                    "Added to the protocol:\n%r", to_append
                )

        if self.args.urls:
            for url in self.args.urls:
                to_append = {
                    "type": "single",
                    "subject_type": "url",
                    "destination": None,
                    "subject": url,
                    "idna_subject": domain2idna.domain2idna(url),
                    "source": None,
                    "output_dir": None,
                    "checker_type": self.checker_type,
                    "session_id": None,
                }

                self.testing_protocol.append(to_append)

                PyFunceble.facility.Logger.debug(
                    "Added to the protocol:\n%r", to_append
                )

        if self.args.files:
            for file in self.args.files:
                to_append = {
                    "type": "file",
                    "subject_type": "domain",
                    # pylint: disable=line-too-long
                    "destination": PyFunceble.cli.utils.testing.get_destination_from_origin(
                        file
                    ),
                    "source": file,
                    "subject": file,
                    "checker_type": self.checker_type,
                    "session_id": None,
                }

                to_append["output_dir"] = filesytem_dirbase.set_parent_dirname(
                    to_append["destination"]
                ).get_output_basedir()

                self.testing_protocol.append(to_append)

                PyFunceble.facility.Logger.debug(
                    "Added to the protocol:\n%r", to_append
                )

        if self.args.url_files:
            for file in self.args.url_files:
                to_append = {
                    "type": "file",
                    "subject_type": "url",
                    # pylint: disable=line-too-long
                    "destination": PyFunceble.cli.utils.testing.get_destination_from_origin(
                        file
                    ),
                    "source": file,
                    "subject": file,
                    "checker_type": self.checker_type,
                    "session_id": None,
                }

                to_append["output_dir"] = filesytem_dirbase.set_parent_dirname(
                    to_append["destination"]
                ).get_output_basedir()

                self.testing_protocol.append(to_append)

                PyFunceble.facility.Logger.debug(
                    "Added to the protocol:\n%r", to_append
                )

    def ci_stop_in_the_middle_if_time_exceeded(self) -> "SystemLauncher":
        """
        Stops our processes as soon as the time is exceeded.
        """

        if self.continuous_integration.is_time_exceeded():
            self.run_ci_saving_instructions()

        return self

    # pylint: disable=too-many-statements
    def fill_to_test_queue_from_protocol(self) -> "SystemLauncher":
        """
        Read the protocol and fill the testing queue.
        """

        def download_file(file: str, destination: str) -> bool:
            """
            Downloads the given file (if it's an URL).

            :param file:
                The file to download.
            :param destination.
                The file to write.

            :return:
                A boolean which represent the action state.
            """

            if URLSyntaxChecker(file).is_valid():
                DownloadHelper(file).download_text(destination=destination)
                return True
            return False

        def get_subjects_from_line(line: str) -> List[str]:
            """
            Provides the list of subject to test.
            """

            result = []

            if PyFunceble.storage.CONFIGURATION.cli_decoding.adblock:
                result.extend(
                    # pylint: disable=line-too-long
                    self.adblock_inputline2subject.set_aggressive(
                        bool(
                            PyFunceble.storage.CONFIGURATION.cli_decoding.adblock_aggressive
                        )
                    )
                    .set_data_to_convert(line)
                    .get_converted()
                )
            elif PyFunceble.storage.CONFIGURATION.cli_decoding.wildcard:
                result.append(
                    self.wildcard2subject.set_data_to_convert(line).get_converted()
                )
            elif PyFunceble.storage.CONFIGURATION.cli_decoding.rpz:
                result.extend(
                    [
                        self.rpz_policy2subject.set_data_to_convert(x).get_converted()
                        for x in self.rpz_inputline2subject.set_data_to_convert(
                            line
                        ).get_converted()
                    ]
                )
            else:
                result.extend(
                    self.inputline2subject.set_data_to_convert(line).get_converted()
                )

            if PyFunceble.storage.CONFIGURATION.cli_testing.complements:
                result.extend(
                    [
                        y
                        for x in result
                        for y in self.subject2complements.set_data_to_convert(
                            x
                        ).get_converted()
                    ]
                )

            if self.checker_type.lower() != "syntax":
                for index, subject in enumerate(result):
                    netloc = self.url2netloc.set_data_to_convert(
                        subject
                    ).get_converted()

                    result[index] = subject.replace(netloc, netloc.lower())

            return ListHelper(result).remove_duplicates().remove_empty().subject

        def cleanup_if_necessary(parent_dirname: str) -> None:
            """
            Process the cleanup if it's necessary.
            """

            cleanup_tool = FilesystemCleanup(parent_dirname)
            running_file_helper = FileHelper(
                os.path.join(
                    cleanup_tool.get_output_basedir(),
                    PyFunceble.cli.storage.TEST_RUNNING_FILE,
                )
            )

            trigger_file_helper = FileHelper(
                os.path.join(
                    cleanup_tool.get_output_basedir(),
                    PyFunceble.cli.storage.CI_TRIGGER_FILE,
                )
            )

            if not running_file_helper.exists():
                self.sessions_id[parent_dirname] = secrets.token_hex(12)

                cleanup_tool.clean_output_files()
                running_file_helper.write(
                    f"{self.sessions_id[parent_dirname]} "
                    f"{datetime.datetime.utcnow().isoformat()}",
                    overwrite=True,
                )
            else:
                possible_session_id = running_file_helper.read().split()[0]

                try:
                    _ = datetime.datetime.fromisoformat(possible_session_id)
                    self.sessions_id[parent_dirname] = None
                except (ValueError, TypeError):
                    self.sessions_id[parent_dirname] = possible_session_id

            if self.continuous_integration.authorized:
                # Ensures that we always have somethin
                trigger_file_helper.write(
                    f"{self.sessions_id[parent_dirname]} "
                    f"{datetime.datetime.utcnow().isoformat()}",
                    overwrite=True,
                )

        def match_output_directory_if_necessary(parent_dirname: str) -> None:
            """
            Restore missing directories from the current directory.
            """

            if not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file:
                DirectoryStructureRestoration(parent_dirname).restore_from_backup()

        def handle_file(protocol: dict) -> None:
            """
            Given a protocol related to a given file, we handle every
            possible decoding case before submitting a new subject to the queue.
            """

            cleanup_if_necessary(protocol["destination"])
            match_output_directory_if_necessary(protocol["destination"])

            if download_file(protocol["subject"], protocol["destination"]):
                protocol["subject"] = os.path.abspath(protocol["destination"])
            else:
                protocol["subject"] = os.path.abspath(protocol["subject"])

            protocol["source"] = os.path.abspath(protocol["destination"])

            with FileHelper(protocol["subject"]).open(
                "r", encoding="utf-8"
            ) as file_stream:
                for line in file_stream:
                    self.ci_stop_in_the_middle_if_time_exceeded()

                    line = line.strip()

                    if "SOA" in line:
                        self.rpz_policy2subject.set_soa(line.split()[0])

                    subjects = get_subjects_from_line(line)
                    subjects = [x for x in subjects if x]

                    for subject in subjects:
                        to_send = copy.deepcopy(protocol)
                        to_send["subject"] = subject
                        to_send["idna_subject"] = domain2idna.domain2idna(subject)
                        to_send["session_id"] = self.sessions_id[
                            protocol["destination"]
                        ]

                        self.tester_process_manager.add_to_input_queue(
                            to_send, worker_name="main"
                        )

                # Now, let's handle the inactive one :-)
                if bool(PyFunceble.storage.CONFIGURATION.cli_testing.inactive_db):
                    for dataset in self.inactive_dataset.get_to_retest(
                        protocol["source"],
                        protocol["checker_type"],
                        # pylint: disable=line-too-long
                        min_days=PyFunceble.storage.CONFIGURATION.cli_testing.days_between.db_retest,
                    ):
                        self.ci_stop_in_the_middle_if_time_exceeded()

                        to_send = copy.deepcopy(protocol)
                        to_send["from_inactive"] = True

                        # Note: Our test infrastructure need a subject
                        # but there is no subject in the table.
                        to_send["subject"] = dataset["idna_subject"]
                        to_send["idna_subject"] = dataset["idna_subject"]

                        to_send["session_id"] = self.sessions_id[
                            protocol["destination"]
                        ]

                        self.tester_process_manager.add_to_input_queue(
                            to_send, worker_name="main"
                        )

                self.file_sorter_process_manager.add_to_input_queue(protocol)

        for protocol in self.testing_protocol:
            self.ci_stop_in_the_middle_if_time_exceeded()

            if protocol["type"] == "single":
                for subject in get_subjects_from_line(protocol["idna_subject"]):
                    to_send = copy.deepcopy(protocol)
                    to_send["subject"], to_send["idna_subject"] = (
                        subject,
                        domain2idna.domain2idna(subject),
                    )

                    self.tester_process_manager.add_to_input_queue(
                        to_send, worker_name="main"
                    )
            elif protocol["type"] == "file":
                handle_file(protocol)

        return self

    def generate_waiting_files(self) -> "SystemLauncher":
        """
        Generates all the files that needs to be generated when all status
        are proceeses.
        """

        def generate_percentage_file(parent_dirname: str) -> None:
            """
            Generates the percentage file.
            """

            if not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file:
                self.counter.set_parent_dirname(parent_dirname)

                destination = os.path.join(
                    self.counter.get_output_basedir(),
                    PyFunceble.cli.storage.OUTPUTS.logs.directories.parent,
                    PyFunceble.cli.storage.OUTPUTS.logs.directories.percentage,
                    PyFunceble.cli.storage.OUTPUTS.logs.filenames.percentage,
                )

                stdout_header_printed = False

                self.stdout_printer.template_to_use = "percentage"
                self.file_printer.template_to_use = "percentage"
                self.file_printer.destination = destination

                for data in self.counter.get_dataset_for_printer():
                    self.file_printer.set_dataset(data).print_interpolated_line()

                    # pylint: disable=line-too-long
                    if (
                        PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.percentage
                        and not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet
                    ):
                        self.stdout_printer.dataset = data

                        if not stdout_header_printed:
                            self.stdout_printer.print_header()
                            stdout_header_printed = True

                        self.stdout_printer.print_interpolated_line()

        for protocol in self.testing_protocol:
            if protocol["destination"]:
                generate_percentage_file(protocol["destination"])

        return self

    def remove_unwanted_files(self) -> "SystemLauncher":
        """
        Deletes some unwanted files that needs to be deleted when all status
        are processed.
        """

        def remove_running_file(parent_dirname: str) -> None:
            """
            Removes the running file.

            :param parent_dirname:
                The name of the directory to work from (under the output
                directory).
            """

            cleanup_tool = FilesystemCleanup(parent_dirname)

            file_helper.set_path(
                os.path.join(
                    cleanup_tool.get_output_basedir(),
                    PyFunceble.cli.storage.TEST_RUNNING_FILE,
                )
            ).delete()
            PyFunceble.facility.Logger.debug("Deleted: %r.", file_helper.path)

        def remove_trigger_file(parent_dirname: str) -> None:
            """
            Removes the trigger file.

            :param parent_dirname:
                The name of the directory to work from (under the output
                directory).
            """

            cleanup_tool = FilesystemCleanup(parent_dirname)

            file_helper.set_path(
                os.path.join(
                    cleanup_tool.get_output_basedir(),
                    PyFunceble.cli.storage.CI_TRIGGER_FILE,
                )
            ).delete()
            PyFunceble.facility.Logger.debug("Deleted: %r.", file_helper.path)

        def remove_continue_dataset(protocol: dict) -> None:
            """
            Removes the continue file.

            :param protocol:
                The protocol to work with.
            """

            continue_object = (
                PyFunceble.cli.utils.testing.get_continue_databaset_object()
            )

            if "set_base_directory" in dir(continue_object):
                # CSV file :-)
                continue_object.set_base_directory(protocol["output_dir"])
                file_helper.set_path(continue_object.source_file).delete()

                PyFunceble.facility.Logger.debug("Deleted: %r.", file_helper.path)
            else:
                # MariaDB / MySQL

                #   ## We specially have different signature.
                continue_object.cleanup(  # pylint: disable=unexpected-keyword-arg
                    session_id=self.sessions_id[protocol["destination"]]
                )

        file_helper = FileHelper()

        for protocol in self.testing_protocol:
            if protocol["destination"]:
                remove_running_file(protocol["destination"])
                remove_trigger_file(protocol["destination"])

            if protocol["output_dir"]:
                remove_continue_dataset(protocol)

        return self

    def run_standard_end_instructions(self) -> "SystemLauncher":
        """
        Runns our standard "end" instructions.

        The instructions executed by this method are the one we execute normally.

        The purpose of this method is to make our standard end instructions
        available to everybody instead of hiding them into the :code:`start`
        method. :-)

        .. warning::
            This is the standard "end" instructions. Do not call this method
            if you are trying to run an action after the CI execution time
            exceeded.
        """

        # Just make sure that all processes are stopped :-)
        self.stop_and_wait_for_all_manager()

        self.generate_waiting_files()
        self.remove_unwanted_files()

        return self

    def run_ci_saving_instructions(self) -> "SystemLauncher":
        """
        Runns our CI "saving" instructions.

        The instructions executed by this method are the one we execute
        before ending a testing session under one of the supported CI engines.

        The purpose of this method is to make our instructions
        available to everybody instead of hiding them into the :code:`start`
        method. :-)

        .. warning::
            This is the standard "end" instructions. Do not call this method
            if you are trying to run an action after the CI execution time
            exceeded.
        """

        self.stop_and_wait_for_all_manager()

        if self.continuous_integration.authorized:
            self.continuous_integration.apply_commit()

        return self

    def run_ci_end_saving_instructions(self) -> "SystemLauncher":
        """
        Runns our CI END "saving" instructions.

        The instructions executed by this method are the one we execute
        before ending a testing session under one of the supported CI engines.

        The purpose of this method is to make our instructions
        available to everybody instead of hiding them into the :code:`start`
        method. :-)

        .. warning::
            This is the standard "end" instructions. Do not call this method
            if you are trying to run an action after the CI execution time
            exceeded.
        """

        self.run_standard_end_instructions()

        if self.continuous_integration.authorized:
            self.continuous_integration.apply_end_commit()

        return self

    def stop_and_wait_for_all_manager(self) -> "SystemLauncher":
        """
        Sends our stop signal and wait until all managers are finished.
        """

        # The idea out here is to propate the stop signal.
        # Meaning that the tester will share it's stop signal to all
        # subsequencial queues after all submitted tasks are done.
        self.tester_process_manager.send_stop_signal(worker_name="main")

        if self.miner_process_manager:
            self.miner_process_manager.wait()

        self.tester_process_manager.wait()
        self.producer_process_manager.wait()

        try:
            # From here, we are sure that every test and files are produced.
            # We now format the generated file(s).
            self.file_sorter_process_manager.start()
            self.file_sorter_process_manager.send_stop_signal()
            self.file_sorter_process_manager.wait()
        except AssertionError:
            # Example: Already started previously.
            pass

        if self.execution_time_holder.authorized:
            self.execution_time_holder.set_end_time()

            self.stdout_printer.set_template_to_use("execution_time").set_dataset(
                self.execution_time_holder.get_info()
            ).print_interpolated_line()

        return self

    @SystemBase.ensure_args_is_given
    def start(self) -> "SystemLauncher":
        try:
            self.print_home_ascii()

            print_central_messages(check_force_update=True)

            # This tries to bypass the execution when the continuous integration
            # is given and the last commit message (the one we are testing for)
            # match any of our known marker. Please report to the method itself
            # for more information about the markers.
            self.continuous_integration.bypass()

            if self.args.files or self.args.url_files:
                self.migrator_process_manager.start()

                self.migrator_process_manager.wait()

            del self.migrator_process_manager

            self.producer_process_manager.start()
            self.tester_process_manager.send_feeding_signal(worker_name="main")

            self.tester_process_manager.start()

            if self.miner_process_manager:
                self.miner_process_manager.start()

            self.fill_protocol()
            self.fill_to_test_queue_from_protocol()

            if self.continuous_integration.is_time_exceeded():
                # Does not includes the run_standard_end_instructions call.
                # Reason: We have to continue.
                self.run_ci_saving_instructions()
            elif self.continuous_integration.authorized:
                # Includes the run_standard_end_instructions call.
                self.run_ci_end_saving_instructions()
            else:
                self.run_standard_end_instructions()
        except (KeyboardInterrupt, StopExecution):
            pass
        except Exception as exception:  # pylint: disable=broad-except
            PyFunceble.facility.Logger.critical(
                "Fatal error.",
                exc_info=True,
            )
            print(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}Fatal Error: {exception}")
            sys.exit(1)

        PyFunceble.cli.utils.stdout.print_thanks()

        return self
