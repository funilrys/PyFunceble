#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the execution time logic.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble.helpers import Dict, File


class ExecutionTime:  # pylint: disable=too-few-public-methods
    """
    Set and return the exection time of the program.

    :param action:
        The action related the execution time.
        Can be `start` or `stop`.
    :type action: str

    :param last:
        Tell the subsystem if we are at the very end of the file testing.
    :type last: bool
    """

    def __init__(self, action="start", last=False):
        # We parse the action to the class scope.
        self.action = action

        if self._authorization():
            # * The execution time disaply is activated.
            # or
            # * The Travis CI mode is activated.

            if self.action == "start":
                # The action is equal to `start`.

                # We set the starting time.
                self._starting_time()
            elif self.action == "stop":
                # * The action is not equal to `start`.
                # and
                # * The action is equal to `stop`

                # We set the ending time.
                self._stoping_time()

                # And we print the execution time.
                print(
                    PyFunceble.Fore.MAGENTA
                    + PyFunceble.Style.BRIGHT
                    + "\nExecution time: "
                    + self.format_execution_time()
                )

        self._save(last=last)

    @classmethod
    def _authorization(cls):  # pragma: no cover
        """
        Check the execution authorization.

        :return: The authorization status.
        :rtype: bool
        """

        if (
            PyFunceble.CONFIGURATION["show_execution_time"]
            or PyFunceble.CONFIGURATION["travis"]
        ):
            return True

        return False

    def _save(self, last=False):  # pragma: no cover
        """
        Save the current time to the file.

        :param last:
            Tell us if we are at the very end of the file testing.
        :type last: bool
        """

        if (
            self._authorization()
            and PyFunceble.CONFIGURATION["logs"]
            and "file_to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["file_to_test"]
        ):
            # * We are authorized to work.
            # and
            # * The generation of logs is activated.
            # and
            # * We are not testing a domain.

            # We set the location of the file we are working with.
            self.file = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                + PyFunceble.OUTPUTS["logs"]["filenames"]["execution_time"]
            )

            if PyFunceble.path.isfile(self.file):
                # The file we are working with exist.

                # We get its content so we can directly work with it.
                content = Dict().from_json(File(self.file).read())
            else:
                # The file we are working with does not exist.

                # We generate a dummy content.
                content = {}

            if self.action == "start":
                # The action is equal to `start`.

                if "final_total" in content and content["final_total"]:
                    # The final total index exist.

                    # We delete it.
                    del content["final_total"]

                if "data" in content:
                    # The data index exist.

                    # We append the current start time inside it at
                    # a new sublist.
                    content["data"].append([PyFunceble.CONFIGURATION["start"]])
                else:
                    # The data index does not exist.

                    # We create the index along with the current start time.
                    content["data"] = [[PyFunceble.CONFIGURATION["start"]]]
            elif self.action == "stop":
                # The action is equal to `stop`.

                try:
                    # We try to work with the data index.

                    # We append the end time at the end of the last element
                    # of data.
                    #
                    # Note: It is at the end because we should have as first
                    # the star time.
                    content["data"][-1].append(PyFunceble.CONFIGURATION["end"])

                    # We get the start time.
                    start = content["data"][0][0]
                    # We get the end time.
                    end = content["data"][-1][-1]

                    # We calculate the execution time of the test.
                    content["current_total"] = self.format_execution_time(start, end)

                    if last:
                        # We are at the very end of the file testing.

                        # We initiate the global execution time.
                        content["final_total"] = content["current_total"]

                        # We inform the user about the global execution time.
                        print(
                            PyFunceble.Fore.MAGENTA
                            + PyFunceble.Style.BRIGHT
                            + "Global execution time: "
                            + content["final_total"]
                        )
                except KeyError:
                    # It is not possible to work with the data index because
                    # it does not exist.

                    # We ignore the problem.
                    pass

            # We save the whole data at its final location.
            Dict(content).to_json(self.file)

    @classmethod
    def _starting_time(cls):  # pragma: no cover
        """
        Set the starting time.
        """

        # We set the starting time as the current time.
        PyFunceble.CONFIGURATION["start"] = int(PyFunceble.time())

    @classmethod
    def _stoping_time(cls):  # pragma: no cover
        """
        Set the ending time.
        """

        # We set the ending time as the current time.
        PyFunceble.CONFIGURATION["end"] = int(PyFunceble.time())

    @classmethod
    def _calculate(cls, start=None, end=None):
        """
        calculate the difference between starting and ending time.

        :param start: A starting time.
        :type start: int|str

        :param stop: A ending time.
        :type stop: int|str

        :return:
            A dict with following as index.

                * :code:`days`
                * :code:`hours`
                * :code:`minutes`
                * :code:`seconds`

            as index.
        :rtype: dict
        """

        if start and end:
            # The start and end time is explicitly given.

            # We get the difference between the ending and the starting time.
            time_difference = int(end) - int(start)
        else:
            # The start and end time is not explicitly given.

            # We get the difference between the ending and the starting time.
            time_difference = (
                PyFunceble.CONFIGURATION["end"] - PyFunceble.CONFIGURATION["start"]
            )

        # We initiate an OrderedDict.
        # Indeed, we use an ordered dict because we want the structuration and the
        # order to stay always the same.
        # As a dictionnary is always unordered, we can use it. Otherwise the time will
        # not be shown correctly.
        data = PyFunceble.OrderedDict()

        # We calculate and append the day to our data.
        data["days"] = str(time_difference // (24 * 60 * 60)).zfill(2)

        # We calculate and append the hours to our data.
        data["hours"] = str((time_difference // (60 * 60)) % 24).zfill(2)

        # We calculate and append the minutes to our data.
        data["minutes"] = str((time_difference % 3600) // 60).zfill(2)

        # We calculate and append the minutes to our data.
        data["seconds"] = str(time_difference % 60).zfill(2)

        # We finaly return our data.
        return data

    def format_execution_time(self, start=None, end=None):
        """
        Format the calculated time into a human readable format.

        :param start: A starting time.
        :type start: int|str

        :param stop: A ending time.
        :type stop: int|str

        :return: A human readable date.
        :rtype: str
        """

        # We return the formatted execution time.
        return ":".join(list(self._calculate(start, end).values()))
