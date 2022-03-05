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

# pylint: disable=too-many-lines

import argparse
import copy
import datetime
import multiprocessing
import os
import secrets
import sys
import traceback
from typing import List, Optional, Union

import colorama
import domain2idna
from sqlalchemy.orm import Session

import PyFunceble.checker.utils.whois
import PyFunceble.cli.storage
import PyFunceble.cli.utils.ascii_logo
import PyFunceble.cli.utils.sort
import PyFunceble.cli.utils.stdout
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.continuous_integration.exceptions import StopExecution
from PyFunceble.cli.continuous_integration.utils import ci_object
from PyFunceble.cli.execution_time import ExecutionTime
from PyFunceble.cli.file_preloader import FilePreloader
from PyFunceble.cli.filesystem.cleanup import FilesystemCleanup
from PyFunceble.cli.filesystem.counter import FilesystemCounter
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.cli.filesystem.dir_structure.restore import (
    DirectoryStructureRestoration,
)
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.cli.filesystem.printer.stdout import StdoutPrinter
from PyFunceble.cli.filesystem.registrar_counter import RegistrarCounter
from PyFunceble.cli.processes.chancy_producer import ChancyProducerProcessesManager
from PyFunceble.cli.processes.chancy_tester import ChancyTesterProcessesManager
from PyFunceble.cli.processes.dir_files_sorter import DirFileSorterProcessesManager
from PyFunceble.cli.processes.migrator import MigratorProcessesManager
from PyFunceble.cli.processes.miner import MinerProcessesManager
from PyFunceble.cli.processes.producer import ProducerProcessesManager
from PyFunceble.cli.processes.tester import TesterProcessesManager
from PyFunceble.cli.system.base import SystemBase
from PyFunceble.cli.utils.testing import (
    get_continue_databaset_object,
    get_destination_from_origin,
    get_inactive_dataset_object,
    get_subjects_from_line,
    get_testing_mode,
)
from PyFunceble.cli.utils.version import print_central_messages
from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject
from PyFunceble.converter.cidr2subject import CIDR2Subject
from PyFunceble.converter.input_line2subject import InputLine2Subject
from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject
from PyFunceble.converter.rpz_policy2subject import RPZPolicy2Subject
from PyFunceble.converter.subject2complements import Subject2Complements
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.converter.wildcard2subject import Wildcard2Subject
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper


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
    cidr2subject: CIDR2Subject = CIDR2Subject()

    stdout_printer: StdoutPrinter = StdoutPrinter()
    file_printer: FilePrinter = FilePrinter()
    counter: FilesystemCounter = FilesystemCounter()
    registrar_counter: RegistrarCounter = RegistrarCounter()

    execution_time_holder: Optional[ExecutionTime] = None
    file_preloader: Optional[FilePreloader] = None

    manager: Optional[multiprocessing.Manager]
    tester_process_manager: Optional[
        Union[TesterProcessesManager, ChancyTesterProcessesManager]
    ] = None
    producer_process_manager: Optional[
        Union[ProducerProcessesManager, ChancyProducerProcessesManager]
    ] = None
    miner_process_manager: Optional[MinerProcessesManager] = None
    dir_files_sorter_process_manager: Optional[DirFileSorterProcessesManager] = None
    migrator_process_manager: Optional[MigratorProcessesManager] = None

    continue_dataset: Optional[ContinueDatasetBase] = None
    inactive_dataset: Optional[InactiveDatasetBase] = None
    continuous_integration: Optional[ContinuousIntegrationBase] = None

    db_session: Optional[Session] = None

    checker_type: Optional[str] = None

    sessions_id: dict = {}

    def __init__(self, args: Optional[argparse.Namespace] = None) -> None:
        try:
            self.db_session = (
                PyFunceble.cli.factory.DBSession.get_db_session().get_new_session()()
            )
        except TypeError:
            self.db_session = None

        self.execution_time_holder = ExecutionTime().set_start_time()
        self.checker_type = get_testing_mode()
        self.continue_dataset = get_continue_databaset_object(
            db_session=self.db_session
        )
        self.inactive_dataset = get_inactive_dataset_object(db_session=self.db_session)
        self.continuous_integration = ci_object()

        if self.continuous_integration.authorized:
            self.continuous_integration.init()

        self.stdout_printer.guess_allow_coloration()

        self.manager = multiprocessing.Manager()

        if not PyFunceble.storage.CONFIGURATION.cli_testing.chancy_tester:
            self.tester_process_manager = TesterProcessesManager(
                self.manager,
                max_worker=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
                continuous_integration=self.continuous_integration,
                daemon=True,
                output_workers_count=1,
                output_queue_num=2,
            )
            self.producer_process_manager = ProducerProcessesManager(
                self.manager,
                max_worker=1,
                continuous_integration=self.continuous_integration,
                input_queue=self.tester_process_manager.output_queue[0],
                daemon=True,
                generate_output_queue=False,
            )
        else:
            self.tester_process_manager = ChancyTesterProcessesManager(
                self.manager,
                max_worker=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
                continuous_integration=self.continuous_integration,
                daemon=True,
                output_workers_count=1,
                output_queue_num=2,
            )
            self.producer_process_manager = ChancyProducerProcessesManager(
                self.manager,
                max_worker=1,
                continuous_integration=self.continuous_integration,
                input_queue=self.tester_process_manager.output_queue[0],
                daemon=True,
                generate_output_queue=False,
            )

        self.dir_files_sorter_process_manager = DirFileSorterProcessesManager(
            self.manager,
            max_worker=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
            continuous_integration=self.continuous_integration,
            daemon=True,
            generate_output_queue=False,
            output_workers_count=0,
        )
        self.migrator_process_manager = MigratorProcessesManager(
            self.manager,
            continuous_integration=self.continuous_integration,
            daemon=True,
            generate_input_queue=False,
            generate_output_queue=False,
            output_workers_count=0,
        )

        if PyFunceble.storage.CONFIGURATION.cli_testing.mining:
            self.miner_process_manager = MinerProcessesManager(
                self.manager,
                max_worker=1,
                continuous_integration=self.continuous_integration,
                input_queue=self.tester_process_manager.output_queue[1],
                output_queue=self.tester_process_manager.input_queue,
                generate_input_queue=False,
                generate_output_queue=False,
                daemon=True,
                output_workers_count=self.tester_process_manager.max_worker,
            )

        if self.continuous_integration.authorized:
            self.continuous_integration.set_start_time()

        self.file_preloader = FilePreloader(
            continuous_integration=self.continuous_integration,
            checker_type=self.checker_type,
            adblock_inputline2subject=self.adblock_inputline2subject,
            wildcard2subject=self.wildcard2subject,
            rpz_policy2subject=self.rpz_policy2subject,
            rpz_inputline2subject=self.rpz_inputline2subject,
            inputline2subject=self.inputline2subject,
            subject2complements=self.subject2complements,
            url2netloc=self.url2netloc,
            continue_dataset=self.continue_dataset,
            inactive_dataset=self.inactive_dataset,
        )

        super().__init__(args)

    def __del__(self) -> None:
        if self.db_session is not None:
            self.db_session.close()

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
                # pylint: disable=line-too-long
                if (
                    not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.merge_output_dirs
                ):
                    destination = get_destination_from_origin(file)
                else:
                    destination = get_destination_from_origin(
                        PyFunceble.cli.storage.OUTPUTS.merged_directory
                    )

                to_append = {
                    "type": "file",
                    "subject_type": "domain",
                    # pylint: disable=line-too-long
                    "destination": destination,
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
                # pylint: disable=line-too-long
                if (
                    not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.merge_output_dirs
                ):
                    destination = get_destination_from_origin(file)
                else:
                    destination = get_destination_from_origin(
                        PyFunceble.cli.storage.OUTPUTS.merged_directory
                    )

                to_append = {
                    "type": "file",
                    "subject_type": "url",
                    # pylint: disable=line-too-long
                    "destination": destination,
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

        def create_trigger_file_if_necessary(parent_dirname: str) -> None:
            """
            Create the trigger file if necessary. The purpose of the trigger
            file is to have a file that is always updated until a test is
            completed done.
            """

            if self.continuous_integration.authorized:
                cleanup_tool = FilesystemCleanup(parent_dirname)

                trigger_file_helper = FileHelper(
                    os.path.join(
                        cleanup_tool.get_output_basedir(),
                        PyFunceble.cli.storage.CI_TRIGGER_FILE,
                    )
                )

                # Ensures that we always have something to commit.
                trigger_file_helper.write(
                    f"{self.sessions_id[parent_dirname]} " f"{secrets.token_hex(8)}",
                    overwrite=True,
                )

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
            create_trigger_file_if_necessary(protocol["destination"])
            match_output_directory_if_necessary(protocol["destination"])

            if download_file(protocol["subject"], protocol["destination"]):
                protocol["subject"] = os.path.relpath(protocol["destination"])
            else:
                protocol["subject"] = os.path.relpath(protocol["subject"])

            protocol["source"] = os.path.relpath(protocol["source"])
            protocol["session_id"] = self.sessions_id[protocol["destination"]]

            if isinstance(self.continue_dataset, CSVContinueDataset):
                self.continue_dataset.set_base_directory(protocol["output_dir"])

            if self.file_preloader.authorized:
                if not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
                    print(
                        f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}"
                        f"Started preloading of {protocol['source']}..."
                    )

                self.file_preloader.set_protocol(protocol).start(
                    # pylint: disable=line-too-long
                    print_dots=(
                        PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet
                        or bool(
                            PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.dots
                        )
                    )
                )

                if not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
                    print(
                        f"\n{colorama.Fore.GREEN}{colorama.Style.BRIGHT}"
                        f"Finished preloading of {protocol['source']}."
                    )

                self.__start_core_processes()

                for subject in self.continue_dataset.get_to_test(
                    protocol["session_id"]
                ):

                    self.ci_stop_in_the_middle_if_time_exceeded()

                    to_send = copy.deepcopy(protocol)
                    to_send["subject"], to_send["idna_subject"] = subject, subject
                    to_send["from_preload"] = True

                    self.tester_process_manager.add_to_input_queue(
                        to_send, worker_name="main"
                    )

            else:
                with FileHelper(protocol["subject"]).open(
                    "r", encoding="utf-8"
                ) as file_stream:
                    for line in file_stream:
                        self.ci_stop_in_the_middle_if_time_exceeded()

                        line = line.strip()

                        if "SOA" in line:
                            self.rpz_policy2subject.set_soa(line.split()[0])

                        for subject in get_subjects_from_line(
                            line,
                            self.checker_type,
                            adblock_inputline2subject=self.adblock_inputline2subject,
                            wildcard2subject=self.wildcard2subject,
                            rpz_policy2subject=self.rpz_policy2subject,
                            rpz_inputline2subject=self.rpz_inputline2subject,
                            inputline2subject=self.inputline2subject,
                            subject2complements=self.subject2complements,
                            url2netloc=self.url2netloc,
                            cidr2subject=self.cidr2subject,
                        ):
                            to_send = copy.deepcopy(protocol)
                            to_send["subject"] = subject
                            to_send["idna_subject"] = domain2idna.domain2idna(subject)

                            self.tester_process_manager.add_to_input_queue(
                                to_send, worker_name="main"
                            )

            # Now, let's handle the inactive one :-)
            if bool(PyFunceble.storage.CONFIGURATION.cli_testing.inactive_db):
                for dataset in self.inactive_dataset.get_to_retest(
                    protocol["destination"],
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

                    self.tester_process_manager.add_to_input_queue(
                        to_send, worker_name="main"
                    )

            self.dir_files_sorter_process_manager.input_datasets.append(
                {"directory": protocol["output_dir"]}
            )

        for protocol in self.testing_protocol:
            self.ci_stop_in_the_middle_if_time_exceeded()

            if protocol["type"] == "single":
                for subject in get_subjects_from_line(
                    protocol["idna_subject"],
                    self.checker_type,
                    adblock_inputline2subject=self.adblock_inputline2subject,
                    wildcard2subject=self.wildcard2subject,
                    rpz_policy2subject=self.rpz_policy2subject,
                    rpz_inputline2subject=self.rpz_inputline2subject,
                    inputline2subject=self.inputline2subject,
                    subject2complements=self.subject2complements,
                    url2netloc=self.url2netloc,
                    cidr2subject=self.cidr2subject,
                ):
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

        def generate_registrar_file(parent_dirname: str) -> None:
            """
            Generates the registrar file.
            """

            if not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.no_file:
                self.registrar_counter.set_parent_dirname(parent_dirname)

                destination = os.path.join(
                    self.counter.get_output_basedir(),
                    PyFunceble.cli.storage.OUTPUTS.logs.directories.parent,
                    PyFunceble.cli.storage.OUTPUTS.logs.directories.percentage,
                    PyFunceble.cli.storage.OUTPUTS.logs.filenames.registrar,
                )

                stdout_header_printed = False

                self.stdout_printer.template_to_use = "registrar"
                self.file_printer.template_to_use = "registrar"
                self.file_printer.destination = destination

                registrar_limit = 0
                for data in self.registrar_counter.get_dataset_for_printer():
                    self.file_printer.set_dataset(data).print_interpolated_line()

                    # pylint: disable=line-too-long
                    if (
                        PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.registrar
                        and not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet
                        and registrar_limit
                        < PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.max_registrar
                    ):
                        self.stdout_printer.dataset = data

                        if not stdout_header_printed:
                            self.stdout_printer.print_header()
                            stdout_header_printed = True

                        self.stdout_printer.print_interpolated_line()
                        registrar_limit += 1

        for protocol in self.testing_protocol:
            if not protocol["destination"]:
                continue

            generate_percentage_file(protocol["destination"])

            if protocol["checker_type"] in self.registrar_counter.SUPPORTED_TEST_MODES:
                generate_registrar_file(protocol["destination"])

            # pylint: disable=line-too-long
            if (
                PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.merge_output_dirs
            ):
                break

        return self

    def remove_unwanted_files(self) -> "SystemLauncher":
        """
        Deletes some unwanted files that needs to be deleted when all status
        are processed.
        """

        def remove_running_file(protocol: str) -> None:
            """
            Removes the running file.
            :param parent_dirname:
                The name of the directory to work from (under the output
                directory).
            """

            if protocol["output_dir"]:
                file_helper.set_path(
                    os.path.join(
                        protocol["output_dir"],
                        PyFunceble.cli.storage.TEST_RUNNING_FILE,
                    )
                ).delete()
                PyFunceble.facility.Logger.debug("Deleted: %r.", file_helper.path)

        def remove_trigger_file(protocol: str) -> None:
            """
            Removes the trigger file.

            :param protocol:
                The protocol to work with.
            """

            if protocol["output_dir"]:
                file_helper.set_path(
                    os.path.join(
                        protocol["output_dir"],
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

            if (
                isinstance(self.continue_dataset, CSVContinueDataset)
                and protocol["output_dir"]
            ):
                # CSV file :-)
                self.continue_dataset.set_base_directory(protocol["output_dir"])
                file_helper.set_path(self.continue_dataset.source_file).delete()

                PyFunceble.facility.Logger.debug("Deleted: %r.", file_helper.path)
            elif protocol["destination"]:
                # MariaDB / MySQL

                #   ## We specially have different signature.
                self.continue_dataset.cleanup(  # pylint: disable=unexpected-keyword-arg
                    session_id=self.sessions_id[protocol["destination"]]
                )

        def remove_preload_dataset(protocol: dict) -> None:
            """
            Removes the preloader dataset file.

            :param protocol:
                The protocol to work with.
            """

            if self.file_preloader.authorized and protocol["output_dir"]:
                file_helper.set_path(
                    os.path.join(
                        protocol["output_dir"],
                        PyFunceble.cli.storage.PRE_LOADER_FILE,
                    )
                ).delete()
                PyFunceble.facility.Logger.debug("Deleted: %r.", file_helper.path)

        file_helper = FileHelper()

        for protocol in self.testing_protocol:
            if "destination" in protocol or "output_dir" in protocol:
                remove_running_file(protocol)
                remove_trigger_file(protocol)

                remove_continue_dataset(protocol)
                remove_preload_dataset(protocol)

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
            self.dir_files_sorter_process_manager.start()
            self.dir_files_sorter_process_manager.send_stop_signal()
            self.dir_files_sorter_process_manager.wait()
        except AssertionError:
            # Example: Already started previously.
            pass

        if self.execution_time_holder.authorized:
            self.execution_time_holder.set_end_time()

            self.stdout_printer.set_template_to_use("execution_time").set_dataset(
                self.execution_time_holder.get_info()
            ).print_interpolated_line()

        return self

    def __start_core_processes(self):
        """
        Starts our core processes.
        """

        if not self.producer_process_manager.is_running():
            self.producer_process_manager.start()

            self.tester_process_manager.start()

            if self.miner_process_manager:
                self.miner_process_manager.start()

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

            if not self.file_preloader.authorized or (
                not self.args.files and not self.args.url_files
            ):
                self.__start_core_processes()

            self.fill_protocol()
            self.fill_to_test_queue_from_protocol()

            self.stop_and_wait_for_all_manager()

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
            print(
                f"{colorama.Fore.RED}{colorama.Style.BRIGHT}Fatal Error: "
                f"{exception}"
            )

            print(traceback.format_exc())
            sys.exit(1)

        PyFunceble.cli.utils.stdout.print_thanks()

        return self
