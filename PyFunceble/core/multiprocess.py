"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the multiprocessing core interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import sys
from itertools import chain
from multiprocessing import Manager, Pipe, Process, active_children
from traceback import format_exc

from box import Box
from colorama import Fore, Style
from colorama import init as initiate_colorama
from domain2idna import get as domain2idna

import PyFunceble

from .api import APICore
from .file import FileCore


class OurProcessWrapper(Process):
    """
    Wrapper of Process.
    The object of this class is just to overwrite :code:`Process.run()`
    in order to catch exceptions.

    .. note::
        This class takes the same arguments as :code:`Process`.
    """

    def __init__(self, *args, **kwargs):
        super(OurProcessWrapper, self).__init__(*args, **kwargs)

        self.conn1, self.conn2 = Pipe()
        self._exception_receiver = None

    def run(self):
        """
        Overwrites :code:`Process.run()`.
        """

        try:
            # We run a normal process.
            Process.run(self)

            # We send None as message as there was no exception.
            self.conn2.send(None)
        except Exception as exception:  # pylint: disable=broad-except
            PyFunceble.LOGGER.exception()

            # We get the traceback.
            traceback = format_exc()

            # We send the exception and its traceback to the pipe.
            self.conn2.send((exception, traceback))

    @property
    def exception(self):
        """
        Provides a way to check if an exception was send.
        """

        try:
            if self.conn1.poll():
                # There is something to read.

                # We get and save the exception.
                self._exception_receiver = self.conn1.recv()
        except EOFError:
            pass

        self.conn2.close()

        return self._exception_receiver


class MultiprocessCore(
    FileCore
):  # pragma: no cover pylint: disable=too-many-instance-attributes
    """
    Brain of PyFunceble for file testing with multiple processes.s.

    :param str file: The file we are testing.
    :param str file_type:
        The file type.
        Should be one of the following.

            - :code:`domain`

            - :code:`url`
    """

    def __init__(self, file, file_content_type="domain"):
        super().__init__(file, file_content_type=file_content_type)

    # pylint: disable=arguments-differ
    def test(self, subject, file_content_type, configuration, manager_data, intern):
        """
        Tests the given subject and return the result.
        """

        PyFunceble.CONFIGURATION = None
        PyFunceble.INTERN = {
            "counter": {
                "number": {"down": 0, "invalid": 0, "tested": 0, "up": 0},
                "percentage": {"down": 0, "invalid": 0, "up": 0},
            }
        }

        initiate_colorama(True)

        PyFunceble.load_config(custom=configuration)

        PyFunceble.INTERN.update(intern)

        if PyFunceble.CONFIGURATION.idna_conversion:
            subject = domain2idna(subject)

        if isinstance(PyFunceble.CONFIGURATION.cooldown_time, (float, int)):
            PyFunceble.sleep(PyFunceble.CONFIGURATION.cooldown_time)

        if PyFunceble.CONFIGURATION.syntax:
            result = APICore(
                subject, complete=True, is_parent=False, db_file_name=self.file
            ).syntax(file_content_type)
        elif PyFunceble.CONFIGURATION.reputation:
            result = APICore(
                subject, complete=True, is_parent=False, db_file_name=self.file
            ).reputation(file_content_type)
        else:
            result = APICore(
                subject, complete=True, is_parent=False, db_file_name=self.file
            ).availability(file_content_type)

        self.generate_complement_status_file(result["tested"], result["status"])
        self.save_into_database(result, self.file, self.mysql_db)

        if manager_data is not None:
            manager_data.append(result)
        else:
            self.post_test_treatment(
                result,
                self.file_type,
                complements_test_started=self.complements_test_started,
                auto_continue_db=self.autocontinue,
                inactive_db=self.inactive_db,
                mining=self.mining,
                whois_db=self.whois_db,
            )

        return result

    def __merge_processes_data(self, manager_data):
        """
        Reads all results and put them at the right location.
        """

        if manager_data is not None:
            if not self.autosave.authorized:
                print(
                    Fore.MAGENTA
                    + Style.BRIGHT
                    + "\nMerging cross processes data... This process may take some time."
                )

            for test_output in manager_data:
                if self.autosave.authorized:
                    print(Fore.MAGENTA + Style.BRIGHT + "Merging process data ...")

                self.post_test_treatment(
                    test_output,
                    self.file_type,
                    complements_test_started=self.complements_test_started,
                    auto_continue_db=self.autocontinue,
                    inactive_db=self.inactive_db,
                    mining=self.mining,
                    whois_db=self.whois_db,
                )

            manager_data[:] = []

        self.autocontinue.save()
        self.inactive_db.save()
        self.mining.save()

        self.cleanup(self.autocontinue, self.autosave, test_completed=False)

    def __check_exception(self, processes, manager_data):
        """
        Checks if an exception is present into the given pool of processes.

        :param list processes. A list of running processes.
        """

        exception_present = False

        for process in processes:
            # We loop through the list of processes.

            try:
                if process.exception and not exception_present:
                    # There in an exception in the currently
                    # read process.

                    # We get the traceback
                    _, traceback = process.exception

                    # We print the traceback.
                    print(traceback)
                    PyFunceble.LOGGER.error(traceback)

                    exception_present = True

                if exception_present:
                    # We kill the process.
                    process.terminate()
            except AttributeError:
                continue

        if exception_present:
            # We finally exit.
            self.__merge_processes_data(manager_data)

            sys.exit(1)

    def __start_process(self, subject, manager_data, ignore_inactive_db_check=False):
        """
        Starts a new process.
        """

        original_config = Box(
            PyFunceble.CONFIGURATION.copy(), default_box=True, default_box_attr=None
        )
        original_intern = PyFunceble.INTERN.copy()

        configuration = PyFunceble.CONFIGURATION.copy()

        configuration = Box(
            PyFunceble.helpers.Merge(
                {
                    "api_file_generation": PyFunceble.CONFIGURATION.db_type == "json",
                    "inactive_database": False,
                    "auto_continue": False,
                }
            ).into(configuration),
            default_box=True,
            default_box_attr=None,
        )

        if not self.should_be_ignored(
            subject,
            self.autocontinue,
            self.inactive_db,
            ignore_inactive_db_check=ignore_inactive_db_check,
        ):
            process = OurProcessWrapper(
                target=self.test,
                args=(
                    subject,
                    self.file_type,
                    configuration,
                    manager_data,
                    original_intern,
                ),
            )
            process.name = f"PyF {subject}"
            process.start()
        elif self.autosave.authorized:
            print(".", end="")

        PyFunceble.CONFIGURATION.update(original_config)
        PyFunceble.INTERN.update(original_intern)

    # pylint: disable=too-many-nested-blocks,too-many-branches
    def __run_multiprocess_test(self, stream, manager, ignore_inactive_db_check=False):
        """
        Tests the content of the given file.
        """

        finished = False
        index = "funilrys"

        if PyFunceble.CONFIGURATION.db_type == "json":
            manager_data = manager.list()
        else:
            manager_data = None

        while True:
            active = active_children()

            while (
                len(active) <= PyFunceble.CONFIGURATION.maximal_processes
                and not self.autosave.is_time_exceed()
            ):
                try:
                    line = next(stream)

                    if isinstance(line, tuple):
                        index, line = line

                    if PyFunceble.CONFIGURATION.adblock:
                        subjects = PyFunceble.converter.AdBlock(
                            line, aggressive=PyFunceble.CONFIGURATION.aggressive
                        ).get_converted()
                    else:
                        subjects = PyFunceble.converter.File(line).get_converted()

                    if isinstance(subjects, list):
                        for subject in subjects:
                            self.__start_process(
                                subject,
                                manager_data,
                                ignore_inactive_db_check=ignore_inactive_db_check,
                            )

                            if index != "funilrys":
                                # An index was given, we remove the index and subject from
                                # the mining database.
                                self.mining.remove(index, subject)
                    else:
                        self.__start_process(
                            subjects,
                            manager_data,
                            ignore_inactive_db_check=ignore_inactive_db_check,
                        )

                        if index != "funilrys":
                            # An index was given, we remove the index and subject from
                            # the mining database.
                            self.mining.remove(index, subjects)

                    active = active_children()
                    continue
                except StopIteration:
                    finished = True
                    active = active_children()

                    break

            self.__check_exception(active_children(), manager_data)

            while len(
                active
            ) >= PyFunceble.CONFIGURATION.maximal_processes and "PyF" in " ".join(
                [x.name for x in reversed(active)]
            ):
                active = active_children()

                PyFunceble.LOGGER.info(
                    f"Active processes: {[x.name for x in reversed(active)]}"
                )

            if PyFunceble.CONFIGURATION.multiprocess_merging_mode == "live":
                if not finished and not self.autosave.is_time_exceed():
                    while "PyF" in " ".join([x.name for x in reversed(active)]):
                        active = active_children()

                    self.__merge_processes_data(manager_data)
                    continue

            if finished or self.autosave.is_time_exceed():
                while "PyF" in " ".join([x.name for x in reversed(active)]):
                    active = active_children()

                self.__merge_processes_data(manager_data)
                break

    def run_test(self):
        """
        Runs the test of the content of the given file.
        """

        self.print_header()

        with open(self.file, "r", encoding="utf-8") as file_stream:
            with Manager() as manager:
                self.__run_multiprocess_test(file_stream, manager)

        if self.autocontinue.is_empty():
            with open(self.file, "r", encoding="utf-8") as file_stream:
                with Manager() as manager:
                    self.__run_multiprocess_test(
                        file_stream, manager, ignore_inactive_db_check=True
                    )

        with Manager() as manager:
            self.__run_multiprocess_test(
                chain(self.inactive_db.get_to_retest()), manager
            )

        with Manager() as manager:
            self.complements_test_started = True
            self.__run_multiprocess_test(
                self.get_complements(self.autocontinue), manager
            )
            self.complements_test_started = False

        with Manager() as manager:
            self.__run_multiprocess_test(chain(self.mining.list_of_mined()), manager)

        self.cleanup(self.autocontinue, self.autosave, test_completed=True)
