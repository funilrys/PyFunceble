# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provide the logic for a file test from the CLI with multiprocesses.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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
# pylint: enable=line-too-long

from itertools import chain
from multiprocessing import Manager, Pipe, Pool, Process, active_children
from traceback import format_exc

import PyFunceble
from PyFunceble.adblock import AdBlock
from PyFunceble.file_core import FileCore
from PyFunceble.helpers import Dict, File, List
from PyFunceble.sort import Sort


class OurProcessWrapper(Process):  # pragma: no cover
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
        except Exception as exception:  # pylint: disable= broad-except
            # We get the traceback.
            traceback = format_exc()

            # We send the exception and its traceback to the pipe.
            self.conn2.send((exception, traceback))

    @property
    def exception(self):
        """
        Provide a way to check if an exception was send.
        """

        if self.conn1.poll():
            # There is something to read.

            # We get and save the exception.
            self._exception_receiver = self.conn1.recv()

        return self._exception_receiver


class FileMultiprocessCore(FileCore):  # pragma: no cover
    """
    Brain of PyFunceble for file testing with multiprocesses.

    :param str file: The file we are testing.
    :param str file_type:
        The file type.
        Should be one of the following.

            - :code:`domain`

            - :code:`url`
    """

    def __init__(self, file, file_type="domain"):
        super(FileMultiprocessCore, self).__init__(file, file_type=file_type)

    @classmethod
    def __sort_generated_files(cls):
        """
        Sort the content of all files we generated.
        """

        for root, _, files in PyFunceble.walk(
            PyFunceble.OUTPUT_DIRECTORY + PyFunceble.OUTPUTS["parent_directory"]
        ):
            # We loop through the list of directories of the output directory.

            for file in files:
                # We loop through the list of file of the
                # currently read directory.

                if file.endswith(".json"):
                    # The currently read filename ends
                    # with .json.

                    # We continue the loop.
                    continue

                if file in [".keep", ".gitignore"]:
                    # The currently read filename is
                    # into a list of filename that are not relevant
                    # for us.

                    # We continue the loop.
                    continue

                # We create an instance of our File().
                file_instance = File(
                    "{0}{1}{2}".format(root, PyFunceble.directory_separator, file)
                )
                # We get the content of the current file.
                file_content = file_instance.read().splitlines()

                if not PyFunceble.CONFIGURATION["hierarchical_sorting"]:
                    # We do not have to sort hierarchicaly.

                    # We sort the lines of the file standarly.
                    formatted = List(file_content[3:]).custom_format(Sort.standard)
                else:
                    # We do have to sort hierarchicaly.

                    # We sort the lines of the file hierarchicaly.
                    formatted = List(file_content[3:]).custom_format(Sort.hierarchical)

                # We finally put the formatted data in place.
                file_instance.write(
                    "\n".join(file_content[:3] + formatted), overwrite=True
                )

    def __process_exception(self, processes, manager_data):
        """
        Check if an exception is present into the given pool of processes.

        :param list processes: A list of processes.
        """

        exception_present = False

        for process in processes:
            # We loop through the list of processes.

            if exception_present:
                # We kill the process.
                process.terminate()

            if process.exception:
                # There in an exception in the currently
                # read process.

                # We get the traceback
                _, traceback = process.exception

                # We print the traceback.
                print(traceback)

                exception_present = True

        if exception_present:
            # We finally exit.
            self.__merge_processes_data(manager_data)

            exit(1)

    def __run_multiprocess_test(self, to_test, manager):
        """
        Test the given list to test with multiple process.

        :param itertools.chain to_test: A chain representing a list of subject to test.
        :param multiprocessing.Manager manager: A Server process.
        """

        # We initiate a variable which will tell us if we
        # finished to test every subject of the given list
        # to test.
        finished = False
        # We initiate a variable for the case that no list of tuple is
        # given.
        #
        # Indeed, as we allow the mining subsystem to run with multiprocess,
        # this is needed.
        index = "funilrys"

        # We create the manager data.
        manager_data = manager.list()

        while True:
            # We get the list of active process.
            active = active_children()
            # We initiate a variable which will save the process which are still running.
            processes = []

            while (
                len(active) <= PyFunceble.CONFIGURATION["maximal_processes"]
                and len(processes) <= PyFunceble.CONFIGURATION["maximal_processes"]
                and not self.autosave.is_time_exceed()
            ):
                # We loop untill we reach the maximal number of processes.

                try:
                    # We get the subject we are going to work with..
                    subject = next(to_test)

                    if isinstance(subject, tuple):
                        # The subject is a tuple.

                        # We spread the index from the subject.
                        index, subject = subject

                    # We initiate a process.
                    process = OurProcessWrapper(
                        target=self._test_line, args=(subject, manager_data)
                    )
                    # # We save it into our list of process.
                    processes.append(process)
                    # We then start the job.
                    process.start()

                    if index != "funilrys":
                        # An index was given, we remove the index and subject from
                        # the mining database.
                        self.mining.remove(index, subject)

                    # We increase the process number.
                    active = active_children()
                    # And we continue the loop.
                    continue
                except StopIteration:
                    # There is no subject into the list to test.

                    finished = True
                    active = active_children()

                    # We break the loop
                    break

            while len(active) != 1:
                active = active_children()

            if finished or self.autosave.is_time_exceed():

                self.__merge_processes_data(manager_data)
                break

        self.__process_exception(processes, manager_data)

    def __merge_processes_data(self, manager_data):
        """
        Assemble the data saved into the server process.

        :param multiprocessing.Manager.list manager_data: A Server process.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "json":
            if not self.autosave.authorized:
                print(
                    PyFunceble.Fore.MAGENTA
                    + PyFunceble.Style.BRIGHT
                    + "\nMerging cross processes data... This process might take some time."
                )

            for data in manager_data:
                # We loop through the server process list members.

                if self.autosave.authorized:
                    print(
                        PyFunceble.Fore.MAGENTA
                        + PyFunceble.Style.BRIGHT
                        + "Merging process data ..."
                    )

                if self.autocontinue.authorized:
                    # We are authorized to operate with the
                    # autocontinue subsystem.

                    # We assemble the currenlty read data with the data of the current
                    # session.
                    self.autocontinue.database = Dict(self.autocontinue.database).merge(
                        data["autocontinue"], strict=False
                    )

                if self.inactive_db.authorized:
                    # We are authorized to operate with the
                    # inactive database subsystem.

                    # We assemble the currenlty read data with the data of the current
                    # session.
                    self.inactive_db.database = Dict(self.inactive_db.database).merge(
                        data["inactive_db"], strict=False
                    )

                if self.mining.authorized:
                    # We are authorized to operate with the
                    # mining subsystem.

                    # We assemble the currenlty read data with the data of the current
                    # session.
                    self.mining.database = Dict(self.mining.database).merge(
                        data["mining"], strict=False
                    )

            # We save the autocontinue database.
            self.autocontinue.save()
            # We save the inactive database.
            self.inactive_db.save()
            # We save the mining database.
            self.mining.save()

        if self.autosave.is_time_exceed():
            # The operation end time was exceeded.

            # We update all counters.
            self.autocontinue.update_counters()

            # We sort the content of all files we generated.
            self.__sort_generated_files()

            # We process the saving of everything.
            self.autosave.process()
        else:
            # We are not auto saving.

            # We update all counters.
            self.autocontinue.update_counters()

            # We sort the content of all files we generated.
            self.__sort_generated_files()

    def generate_json_format(self):
        """
        Generate the JSON formatted file.

        .. note::
            This is needed because otherwise we might get a format issue.
        """

        if PyFunceble.CONFIGURATION["generate_json"]:
            # We have to generate the JSON format.

            for status, data in self.autocontinue.database[self.file].items():
                # We loop through the autocontinue data.

                # We save the data at their final location.
                Dict(data).to_json(
                    PyFunceble.OUTPUT_DIRECTORY
                    + PyFunceble.OUTPUTS["parent_directory"]
                    + PyFunceble.OUTPUTS["json"]["directory"]
                    + status
                    + PyFunceble.OUTPUTS["json"]["filename"]
                )

    def read_and_test_file_content(self):  # pragma: no cover
        """
        Read a file block by block and test its content.
        """

        # We print the CLI header.
        PyFunceble.CLICore.print_header()

        with open(self.file, "r", encoding="utf-8") as file:
            # We open the file we have to test.

            already_tested_continue = self.autocontinue.get_already_tested()
            already_tested_inactive_db = self.inactive_db.get_already_tested()

            with Pool(PyFunceble.CONFIGURATION["maximal_processes"]) as pool:
                if not PyFunceble.CONFIGURATION["adblock"]:
                    formatted_subjects = set(pool.map(self._format_line, file))
                else:
                    formatted_subjects = {x for x in AdBlock(file).decode()}

                subjects_to_test = formatted_subjects - already_tested_continue
                subjects_to_test -= already_tested_inactive_db

                if not subjects_to_test:
                    subjects_to_test = list(formatted_subjects)
                else:
                    subjects_to_test = list(subjects_to_test)

                to_test = chain(subjects_to_test, self.inactive_db.get_to_retest())

            with Manager() as manager:
                # We initiate a server process.

                # We process the test/save of the original list to test.
                self.__run_multiprocess_test(to_test, manager)

                # We get the list of mined data to test.
                to_test = chain(self.mining.list_of_mined())

                # We process the test/save of the mined data to test.
                self.__run_multiprocess_test(to_test, manager)

                # We get the list of complements to test.
                complements = self.get_complements()

                if complements:
                    # We process the test/save of the original list to test.
                    to_test = chain(complements)

                    self.__run_multiprocess_test(to_test, manager)

                    # We inform all subsystem that we are not testing for complements anymore.
                    self.complements_test_started = False

        # We generate the JSON formatted files if needed.
        self.generate_json_format()
        # We clean the autocontinue subsystem, we finished
        # the test.
        self.autocontinue.clean()
        # We process the autosaving if necessary.
        self.autosave.process(test_completed=True)
