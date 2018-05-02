"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.clean


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
# pylint: disable=import-error
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.clean import Clean
from PyFunceble.config import load_configuration
from PyFunceble.helpers import File


class TestClean(TestCase):
    """
    This test is in charge of testing PyFunceble.clean.
    """

    def setUp(self):
        """
        This method setup everything that is needed.
        """

        load_configuration(PyFunceble.CURRENT_DIRECTORY)
        self.file = PyFunceble.OUTPUTS["parent_directory"] + "hello_world"
        self.types = ["up", "down", "invalid", "tested"]

    def set_counter(self, to_set=15):
        """
        This method set the counters to the desired number.

        Argument:
            - to_set: int
                The number to set to each counter
        """

        for string in self.types:
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: to_set})

    def test_with_empty_list(self):
        """
        This method test the cleaning in the case that we have to test an empty
        list.
        """

        File(self.file).write("Hello, World!")

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)
        Clean(None)

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_number_of_tested_null(self):
        """
        This method test the cleaning process in the case that the number of tested
        is null.
        """

        File(self.file).write("Hello, World!")

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)
        self.set_counter()

        expected = {"up": 15, "down": 15, "invalid": 15, "tested": 15}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)
        PyFunceble.CONFIGURATION["counter"]["number"]["tested"] = 0

        expected = {"up": 15, "down": 15, "invalid": 15, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)
        Clean(["hello.world"])

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_tested_out_of_index(self):
        """
        This method test the cleaning process in the case that the number of tested
        is > len(list_to_test).
        """

        File(self.file).write("Hello, World!")

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)
        self.set_counter()

        expected = {"up": 15, "down": 15, "invalid": 15, "tested": 15}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)
        Clean(["hello.world"])

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_tested_same_last(self):
        """
        This method test the cleaning process in the case that the number of tested
        is = len(list_to_test).
        """

        File(self.file).write("Hello, World!")

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)
        self.set_counter(3)

        expected = {"up": 3, "down": 3, "invalid": 3, "tested": 3}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)
        Clean(["hello.world", "world.hello", "hello-world.com"])

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
