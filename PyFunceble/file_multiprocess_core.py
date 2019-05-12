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
from multiprocessing import Manager, Pipe, Process
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

    def __run_multiprocess_test(self, to_test, manager_data):
        """
        Test the given list to test with multiple process.

        :param itertools.chain to_test: A chain representing a list of subject to test.
        :param multiprocessing.Manager.list manager_data: A Server process.
        """

        # We initiate the process counter.
        i = 1
        # We initiate a variable which will tell us if we
        # finished to test every subject of the given list
        # to test.
        finished = False
        # We initiate a variable which will save the process which are still running.
        processes = []
        # We initiate a variable for the case that no list of tuple is
        # given.
        #
        # Indeed, as we allow the mining subsystem to run with multiprocess,
        # this is needed.
        index = "funilrys"

        while i <= PyFunceble.CONFIGURATION["maximal_processes"]:
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
                # We save it into our list of process.
                processes.append(process)
                # We then start the job.
                process.start()

                if index != "funilrys":
                    # An index was given, we remove the index and subject from
                    # the mining database.
                    self.mining.remove(index, subject)

                # We increase the process number.
                i += 1
                # And we continue the loop.
                continue
            except StopIteration:
                # There is no subject into the list to test.

                # We update the finished "flag"
                finished = True

                # We break the loop
                break

        # We check if an exception is present into one process
        # and we then save the process index.
        exception_present = [x for x, y in enumerate(processes) if y.exception]

        if exception_present:
            # One or more exception is present.

            for process in processes:
                # We loop through the list of processes.

                if process.exception:
                    # There in an exception in the currently
                    # read process.

                    # We get the traceback
                    _, traceback = process.exception

                    # We print the traceback.
                    print(traceback)

                # We kill the process.
                process.kill()

            # We finally exit.
            exit(1)

        else:
            # There was no exception.

            for process in processes:
                # We loop through the list of processes.

                # We then wait until all processes are done.
                process.join()

                # We continue the loop
                continue

        return finished

    def __loop_test(self, to_test, manager_data):
        """
        Process the test of each subject of the list to test.

        :param list to_test: The list of subjects we have to test.
        :param multiprocessing.Manager.list manager_data: A Server process.
        """

        if self.autosave.authorized:
            # We have to save at one point.

            while not self.autosave.is_time_exceed():
                # We loop untill the end time is not exceed.

                if not self.__run_multiprocess_test(to_test, manager_data):
                    # Untill the test is completly done, we continue the loop.
                    continue
                else:
                    # Otherwise we break the loop as the test is finished.
                    break
        else:
            # We do not have to save at one point.

            while not self.__run_multiprocess_test(to_test, manager_data):
                # We test untill the test is finished.

                continue

    def __auto_save_process(self, manager_data):
        """
        Assemble the data saved into the server process.

        :param multiprocessing.Manager.list manager_data: A Server process.
        """

        for data in manager_data:
            # We loop through the server process list members.

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

        # We update all counters.
        self.autocontinue.update_counters()
        # We save the autocontinue database.
        self.autocontinue.save()
        # We save the inactive database.
        self.inactive_db.save()
        # We save the mining database.
        self.mining.save()
        # We sort the content of all files we generated.
        self.__sort_generated_files()

        if self.autosave.is_time_exceed():
            # The operation end time was exceeded.

            # We process the saving of everything.
            self.autosave.process()

    def read_and_test_file_content(self):  # pragma: no cover
        """
        Read a file block by block and test its content.
        """

        # We print the CLI header.
        PyFunceble.CLICore.print_header()

        with open(self.file, "r", encoding="utf-8") as file:
            # We open the file we have to test.

            if not PyFunceble.CONFIGURATION["hierarchical_sorting"]:
                # We do not have to sort hierarchicaly.

                # We sort the lines standarly.
                file = List(file).custom_format(Sort.standard)
            else:
                # We do have to sort hierarchicaly.

                # We sort the lines hierarchicaly.
                file = List(file).custom_format(Sort.hierarchical)

            if not PyFunceble.CONFIGURATION["adblock"]:
                # We do not have to adblock decode the content
                # of the file.

                to_test = chain(file, self.inactive_db["to_test"])
            else:
                # We do have to decode the content of the file.

                to_test = chain(AdBlock(file).decode(), self.inactive_db["to_test"])

            with Manager() as manager:
                # We initiate a server process.

                manager_data = manager.list()

                # We process the test/save of the original list to test.
                self.__loop_test(to_test, manager_data)
                self.__auto_save_process(manager_data)

                # We get the list of mined data to test.
                to_test = chain(self.mining.list_of_mined())

                # We process the test/save of the mined data to test.
                self.__loop_test(to_test, manager_data)
                self.__auto_save_process(manager_data)

                # We get the list of complements to test.
                complements = self.get_complements()

                if complements:
                    # We process the test/save of the original list to test.
                    to_test = chain(complements)

                    self.__loop_test(to_test, manager_data)
                    self.__auto_save_process(manager_data)

                    # We inform all subsystem that we are not testing for complements anymore.
                    self.complements_test_started = False

        # We clean the autocontinue subsystem, we finished
        # the test.
        self.autocontinue.clean()
        # We process the autosaving if necessary.
        self.autosave.process(test_completed=True)
