# pylint:disable=line-too-long,invalid-name,import-error
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.cli.execution_time

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
# pylint: enable=line-too-long

import sys
from collections import OrderedDict
from datetime import datetime, timedelta
from unittest import main as launch_tests
from unittest.mock import patch

from colorama import Fore, Style
from colorama import init as initiate_colorama

import PyFunceble
from PyFunceble.cli.execution_time import ExecutionTime
from stdout_base import StdoutBase


class TestExecutionTime(StdoutBase):
    """
    Tests of PyFunceble.cli.execution time
    """

    # pylint: disable=unsupported-assignment-operation, unsubscriptable-object

    def setUp(self):
        """
        Setups everything needed for the tests
        """

        PyFunceble.load_config(generate_directory_structure=False)

        initiate_colorama(True)

        StdoutBase.setUp(self)

    def tearDown(self):
        """
        Setups everything needed for after the tests.
        """

        StdoutBase.tearDown(self)

    def test_authorization(self):
        """
        Tests the authorization method.
        """

        PyFunceble.CONFIGURATION.show_execution_time = False
        expected = False

        actual = ExecutionTime.authorization()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.show_execution_time = False
        PyFunceble.CONFIGURATION.ci = True
        expected = True

        actual = ExecutionTime.authorization()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.show_execution_time = False
        PyFunceble.CONFIGURATION.ci = False
        expected = False

        actual = ExecutionTime.authorization()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.show_execution_time = True
        PyFunceble.CONFIGURATION.ci = False
        expected = True

        actual = ExecutionTime.authorization()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_stoping_time", lambda x: x)
    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_starting_time", lambda x: x)
    def test_calculate(self):
        """
        Tests the calculation method.
        """

        PyFunceble.CONFIGURATION.show_execution_time = True

        start_time = datetime.now()
        PyFunceble.INTERN["start"] = start_time.timestamp()
        PyFunceble.INTERN["end"] = (start_time + timedelta(seconds=15)).timestamp()

        expected = OrderedDict(
            zip(["days", "hours", "minutes", "seconds"], ["00", "00", "00", "15.0"])
        )

        actual = ExecutionTime("stop").calculate()

        self.assertEqual(expected, actual)

        actual = ExecutionTime("stop").calculate(
            start=start_time.timestamp(),
            end=(start_time + timedelta(seconds=15)).timestamp(),
        )

        self.assertEqual(expected, actual)

    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_stoping_time", lambda x: x)
    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_starting_time", lambda x: x)
    def test_calculate_consequent(self):
        """
        Tests the calculation method with more consequent data.
        """

        start_time = datetime.now()
        PyFunceble.INTERN["start"] = start_time.timestamp()
        PyFunceble.INTERN["end"] = (
            start_time + timedelta(days=1, hours=50)
        ).timestamp()

        expected = OrderedDict(
            zip(["days", "hours", "minutes", "seconds"], ["03", "02", "00", "0.0"])
        )

        actual = ExecutionTime("stop").calculate()

        self.assertEqual(expected, actual)

        actual = ExecutionTime("stop").calculate(
            start=start_time.timestamp(),
            end=(start_time + timedelta(days=1, hours=50)).timestamp(),
        )

        self.assertEqual(expected, actual)

    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_stoping_time", lambda x: x)
    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_starting_time", lambda x: x)
    def test_save(self):
        """
        Test the saving method.
        """

        expected_file_location = (
            PyFunceble.OUTPUT_DIRECTORY
            + PyFunceble.OUTPUTS.parent_directory
            + PyFunceble.OUTPUTS.logs.directories.parent
            + PyFunceble.OUTPUTS.logs.filenames.execution_time
        )

        PyFunceble.helpers.File(expected_file_location).delete()

        PyFunceble.CONFIGURATION.show_execution_time = True
        PyFunceble.CONFIGURATION.logs = True
        PyFunceble.CONFIGURATION.show_percentage = False
        PyFunceble.INTERN["file_to_test"] = "this_is_a_ghost"

        start_time = datetime.now()
        PyFunceble.INTERN["start"] = start_time.timestamp()
        PyFunceble.INTERN["end"] = (start_time + timedelta(seconds=15)).timestamp()

        expected = {
            "current_total": "00:00:00:15.0",
            "data": [
                [PyFunceble.INTERN["start"], PyFunceble.INTERN["end"]],
                [PyFunceble.INTERN["start"], PyFunceble.INTERN["end"]],
            ],
            "final_total": "00:00:00:15.0",
        }

        ExecutionTime("start")
        ExecutionTime("stop")

        expected_stdout = (
            f"{Fore.MAGENTA}{Style.BRIGHT }\n"
            f"Execution time: {expected['final_total']}\n"
        )
        self.assertEqual(expected_stdout, sys.stdout.getvalue())

        ExecutionTime("start")
        ExecutionTime("stop", last=True)

        expected_stdout += expected_stdout
        expected_stdout += (
            f"{Fore.MAGENTA}{Style.BRIGHT }"
            f"Global execution time: {expected['final_total']}\n"
        )
        self.assertEqual(
            expected_stdout,
            sys.stdout.getvalue(),
            f"{repr(sys.stdout.getvalue())}\n{repr(expected_stdout)}",
        )

        actual = PyFunceble.helpers.Dict().from_json_file(expected_file_location)
        self.assertEqual(expected, actual)

        del expected["final_total"]

        ExecutionTime("start")
        ExecutionTime("stop", last=True)

        expected["data"].extend(
            [[PyFunceble.INTERN["start"], PyFunceble.INTERN["end"]]]
        )
        expected["final_total"] = "00:00:00:15.0"

        actual = PyFunceble.helpers.Dict().from_json_file(expected_file_location)
        self.assertEqual(expected, actual)

    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_stoping_time", lambda x: x)
    @patch("PyFunceble.cli.execution_time.ExecutionTime.set_starting_time", lambda x: x)
    @patch("PyFunceble.cli.execution_time.ExecutionTime.calculate")
    def test_format_execution_time(self, calculate):
        """
        Tests of the date formatter method.
        """

        calculate.return_value = OrderedDict(
            zip(["days", "hours", "minutes", "seconds"], ["00", "00", "00", "15.0"])
        )
        expected = "00:00:00:15.0"
        actual = ExecutionTime("stop").format_execution_time()

        self.assertEqual(expected, actual)

        calculate.return_value = OrderedDict(
            zip(["days", "hours", "minutes", "seconds"], ["03", "02", "00", "0.0"])
        )

        expected = "03:02:00:0.0"
        actual = ExecutionTime("stop").format_execution_time()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
