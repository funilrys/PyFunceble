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

Tests of the PyFunceble.output.percentage

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
# pylint: enable=line-too-long

import sys
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.output import Percentage
from stdout_base import StdoutBase


class TestPercentage(StdoutBase):
    """
    Tests of the PyFunceble.output.percentage.
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        PyFunceble.INTERN = {
            "counter": {
                "number": {"down": 0, "invalid": 0, "tested": 0, "up": 0},
                "percentage": {"down": 0, "invalid": 0, "up": 0},
            }
        }
        PyFunceble.load_config()
        StdoutBase.setUp(self)

        PyFunceble.cconfig.Preset().init_all()

        PyFunceble.CONFIGURATION.show_percentage = True
        PyFunceble.CONFIGURATION.syntax = False
        PyFunceble.CONFIGURATION.reputation = False

    @classmethod
    def __preset_counters_and_get_expected(cls):
        """
        Preset the counters.
        """

        expected = {}

        for i, element in enumerate(["tested", "up", "down", "invalid"]):
            PyFunceble.INTERN["counter"]["number"][element] = 12 + i
            expected.update({element: 12 + i})

        return expected

    def test_count(self):
        """
        Tests if the counter can be set proprely.
        """

        expected = self.__preset_counters_and_get_expected()

        for element in ["up", "down", "invalid"]:
            Percentage(
                domain_status=PyFunceble.STATUS.official[element], init=None
            ).count()

            expected[element] += 1
            expected["tested"] += 1
            actual = PyFunceble.INTERN["counter"]["number"]

            self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.syntax = True

        expected = self.__preset_counters_and_get_expected()

        for element in ["up", "down", "invalid"]:
            Percentage(
                domain_status=PyFunceble.STATUS.official[element], init=None
            ).count()

            expected[element] += 1
            expected["tested"] += 1
            actual = PyFunceble.INTERN["counter"]["number"]

            self.assertEqual(expected, actual)

    def test_init(self):
        """
        Tests if we are able to initiate the percentage
        system from outside.
        """

        expected = {"up": 15, "down": 2, "invalid": 0, "tested": 75}

        Percentage(domain_status=None, init=expected)

        self.assertEqual(expected, PyFunceble.INTERN["counter"]["number"])

    def test_calculate(self):
        """
        Tests the calculation method.
        """

        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        expected = {"up": 36, "down": 62, "invalid": 1}

        Percentage(domain_status=None, init=None).calculate()
        actual = PyFunceble.INTERN["counter"]["percentage"]

        self.assertEqual(expected, actual)

    def test_log(self):
        """
        Tests the log system.
        """

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
        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        # Test for the case that we do not show_percentage
        PyFunceble.CONFIGURATION.show_percentage = False
        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()

        actual = PyFunceble.INTERN["counter"]["percentage"]
        expected = {"up": 36, "down": 62, "invalid": 1}

        self.assertEqual(expected, actual)

    def test_log_syntax_test(self):
        """
        Tests the logging of the percentage for a syntax check.
        """

        PyFunceble.CONFIGURATION.syntax = True
        PyFunceble.CONFIGURATION.reputation = False

        expected = """

Status      Percentage   Numbers%s
----------- ------------ ------------
VALID       95%%          45%s
INVALID     4%%           2%s
""" % (
            " " * 5,
            " " * 10,
            " " * 11,
        )
        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 0, "down": 0, "valid": 45, "invalid": 2, "tested": 47}
        )

        Percentage(domain_status=None, init=None).log()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        # Test for the case that we do not show_percentage
        PyFunceble.CONFIGURATION.show_percentage = False
        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 0, "down": 0, "valid": 45, "invalid": 2, "tested": 47}
        )

        Percentage(domain_status=None, init=None).log()

        actual = PyFunceble.INTERN["counter"]["percentage"]
        expected = {"up": 0, "down": 0, "valid": 95, "invalid": 4}

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.syntax = False
        PyFunceble.CONFIGURATION.reputation = False

    def test_log_reputation_test(self):
        """
        Tests the logging of the percentage for a reputation check.
        """

        PyFunceble.CONFIGURATION.reputation = True
        PyFunceble.CONFIGURATION.syntax = False

        expected = """

Status      Percentage   Numbers%s
----------- ------------ ------------
SANE        95%%          45%s
MALICIOUS   4%%           2%s
""" % (
            " " * 5,
            " " * 10,
            " " * 11,
        )
        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 0, "down": 0, "invalid": 0, "sane": 45, "malicious": 2, "tested": 47}
        )

        Percentage(domain_status=None, init=None).log()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)

        # Test for the case that we do not show_percentage
        PyFunceble.CONFIGURATION.show_percentage = False
        PyFunceble.INTERN["counter"]["number"].update(
            {"up": 0, "down": 0, "invalid": 0, "sane": 45, "malicious": 2, "tested": 47}
        )

        Percentage(domain_status=None, init=None).log()

        actual = PyFunceble.INTERN["counter"]["percentage"]
        expected = {"up": 0, "down": 0, "invalid": 0, "sane": 95, "malicious": 4}

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.reputation = False
        PyFunceble.CONFIGURATION.syntax = False


if __name__ == "__main__":
    launch_tests()
