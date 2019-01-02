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

This submodule will test PyFunceble.percentage.

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
# pylint: disable=bad-continuation,protected-access,ungrouped-imports

from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout, sys
from PyFunceble.percentage import Percentage


class TestPercentage(BaseStdout):
    """
    Test PyFunceble.percentage.
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        PyFunceble.load_config()

    def test_count(self):
        """
        Test if the counter can be set proprely.
        """

        expected = {}

        for i, element in enumerate(["tested", "up", "down", "invalid"]):
            PyFunceble.CONFIGURATION["counter"]["number"][element] = 12 + i
            expected.update({element: 12 + i})

        for element in ["tested", "up", "down", "invalid"]:
            try:
                Percentage(
                    domain_status=PyFunceble.STATUS["official"][element], init=None
                ).count()

                expected[element] += 1
                expected["tested"] += 1
                actual = PyFunceble.CONFIGURATION["counter"]["number"]

                self.assertEqual(expected, actual)
            except KeyError:
                pass

        PyFunceble.CONFIGURATION["syntax"] = True

        for i, element in enumerate(["tested", "up", "down", "invalid"]):
            PyFunceble.CONFIGURATION["counter"]["number"][element] = 12 + i
            expected.update({element: 12 + i})

        for element in ["tested", "up", "down", "invalid"]:
            try:
                Percentage(
                    domain_status=PyFunceble.STATUS["official"][element], init=None
                ).count()

                expected[element] += 1
                expected["tested"] += 1
                actual = PyFunceble.CONFIGURATION["counter"]["number"]

                self.assertEqual(expected, actual)
            except KeyError:
                pass

        PyFunceble.CONFIGURATION["counter"]["number"] = {}
        PyFunceble.CONFIGURATION["syntax"] = False

    def test_init(self):
        """
        Test the :code:`init` argument of Percentage()
        """

        expected = {"up": 15, "down": 2, "invalid": 0, "tested": 75}

        Percentage(domain_status=None, init=expected)

        self.assertEqual(expected, PyFunceble.CONFIGURATION["counter"]["percentage"])

        PyFunceble.CONFIGURATION["counter"]["percentage"] = {}

    def test_calculate(self):
        """
        Test the calculation system.
        """

        PyFunceble.CONFIGURATION["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        expected = {"up": 36, "down": 62, "invalid": 1}

        Percentage(domain_status=None, init=None)._calculate()
        actual = PyFunceble.CONFIGURATION["counter"]["percentage"]

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["counter"]["number"] = {}

    def test_log(self):
        """
        Test the log system.
        """

        BaseStdout.setUp(self)

        expected = """

Status      Percentage   Numbers%s
----------- ------------ ------------
ACTIVE      36%%          45%s
INACTIVE    62%%          78%s
INVALID     1%%           2%s
""" % (
            " " * 5,
            " " * 10,
            " " * 10,
            " " * 11,
        )
        PyFunceble.CONFIGURATION["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        # Test for the case that we do not show_percentage
        PyFunceble.CONFIGURATION["show_percentage"] = False
        PyFunceble.CONFIGURATION["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()

        actual = PyFunceble.CONFIGURATION["counter"]["percentage"]
        expected = {"up": 36, "down": 62, "invalid": 1}
        self.assertEqual(expected, actual)

    def test_log_syntax(self):
        """
        Test the log system for the case that we are checking for syntax.
        """

        PyFunceble.CONFIGURATION["syntax"] = True

        BaseStdout.setUp(self)

        expected = """

Status      Percentage   Numbers%s
----------- ------------ ------------
VALID       36%%          45%s
INVALID     1%%           2%s
""" % (
            " " * 5,
            " " * 10,
            " " * 11,
        )
        PyFunceble.CONFIGURATION["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        # Test for the case that we do not show_percentage
        PyFunceble.CONFIGURATION["show_percentage"] = False
        PyFunceble.CONFIGURATION["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()

        actual = PyFunceble.CONFIGURATION["counter"]["percentage"]
        expected = {"up": 36, "down": 62, "invalid": 1}
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
