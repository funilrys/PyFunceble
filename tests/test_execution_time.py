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

This submodule will test PyFunceble.execution_time.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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
# pylint: disable=protected-access,ungrouped-imports
import unittest.mock as mock  # pylint: disable=useless-import-alias
from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout
from PyFunceble.config import Load
from PyFunceble.execution_time import ExecutionTime


class TestExecutionTime(BaseStdout):
    """
    Test PyFunceble.execution_time.
    """

    def setUp(self):
        """
        Setup everything needed for the tests
        """

        Load(PyFunceble.CURRENT_DIRECTORY)
        BaseStdout.setUp(self)
        PyFunceble.CONFIGURATION["show_execution_time"] = True
        PyFunceble.CONFIGURATION["start"] = int(PyFunceble.time())
        PyFunceble.CONFIGURATION["end"] = int(PyFunceble.time()) + 15

    @mock.patch("PyFunceble.execution_time.ExecutionTime._stoping_time")
    def test_calculate(self, _):
        """
        Test the calculation of the execution time.
        """

        expected = PyFunceble.OrderedDict(
            [("days", "00"), ("hours", "00"), ("minutes", "00"), ("seconds", "15")]
        )
        actual = ExecutionTime("stop")._calculate()

        self.assertEqual(expected, actual)

    @mock.patch("PyFunceble.execution_time.ExecutionTime._stoping_time")
    def test_calculate_consequent(self, _):
        """
        Test the calculation of the execution time for more consequent
        time.
        """

        day_in_second = 60 * 60 * 24
        fifty_hours_in_second = 60 * 60 * 50

        expected = PyFunceble.OrderedDict(
            [("days", "03"), ("hours", "02"), ("minutes", "00"), ("seconds", "00")]
        )

        end = int(PyFunceble.time()) + day_in_second + fifty_hours_in_second
        actual = ExecutionTime()._calculate(start=int(PyFunceble.time()), end=end)

        self.assertEqual(expected, actual)

    @mock.patch("PyFunceble.execution_time.ExecutionTime._calculate")
    def test_format_execution_time(self, calculate):
        """
        Test if the printed format is the one we want.
        """

        calculate.return_value = PyFunceble.OrderedDict(
            [("days", "01"), ("hours", "12"), ("minutes", "25"), ("seconds", "15")]
        )

        actual = ExecutionTime("start").format_execution_time()
        expected = "01:12:25:15"

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
