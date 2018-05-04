"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.percentage


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
# pylint: disable=bad-continuation,protected-access,ungrouped-imports

from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout, sys
from PyFunceble.percentage import Percentage


class TestPercentage(BaseStdout):
    """
    This class will test PyFunceble.percentage.
    """

    def test_count(self):
        """
        This method test if the counter can be set proprely.
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

        PyFunceble.CONFIGURATION["counter"]["number"] = {}

    def test_init(self):
        """
        This method test the `init` argument of Percentage()
        """

        expected = {"up": 15, "down": 2, "invalid": 0, "tested": 75}

        Percentage(domain_status=None, init=expected)

        self.assertEqual(expected, PyFunceble.CONFIGURATION["counter"]["percentage"])

        PyFunceble.CONFIGURATION["counter"]["percentage"] = {}

    def test_calculate(self):
        """
        This method test the calculation system.
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
        This method test the log system.
        """

        BaseStdout.setUp(self)

        expected = """

Status      Percentage   Numbers%s
----------- ------------ ------------%s
ACTIVE      36%%          45%s
INACTIVE    62%%          78%s
INVALID     1%%           2%s
""" % (
            " " * 6, " " * 1, " " * 11, " " * 11, " " * 12
        )
        PyFunceble.CONFIGURATION["counter"]["number"].update(
            {"up": 45, "down": 78, "invalid": 2, "tested": 125}
        )

        Percentage(domain_status=None, init=None).log()
        actual = sys.stdout.getvalue()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
