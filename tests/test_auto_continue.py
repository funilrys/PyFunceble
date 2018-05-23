"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.auto_continue


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

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
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.config import Load
from PyFunceble.helpers import Dict, File


class TestsAutoContinue(TestCase):
    """
    This class is in char of testing PyFunceble.AutoSave().
    """

    def setUp(self):
        """
        This method setup the needed variables.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)
        self.file = PyFunceble.OUTPUTS["parent_directory"] + PyFunceble.OUTPUTS["logs"][
            "filenames"
        ][
            "auto_continue"
        ]
        PyFunceble.CONFIGURATION["file_to_test"] = "hello.world"
        self.types = ["up", "down", "invalid", "tested"]

    def set_counter(self, to_set=15):
        """
        This method will set the counter at a given number.

        Argument:
            - to_set: int
                The number to set to every counter.
        """

        for string in self.types:
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: to_set})

    def test_backup(self):
        """
        This function test AutoContinue().backup().
        """

        PyFunceble.CONFIGURATION["auto_continue"] = True

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)
        self.set_counter(to_set=25)

        AutoContinue().backup()

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "up": 25, "down": 25, "invalid": 25, "tested": 25
            }
        }
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)
        PyFunceble.CONFIGURATION["auto_continue"] = False
        File(self.file).delete()

    def test_backup_not_activated(self):
        """
        This function test AutoContinue().backup() for the case that we did not
        activated the backup system.
        """

        PyFunceble.CONFIGURATION["auto_continue"] = False

        AutoContinue().backup()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_restore(self):
        """
        This method test AutoContinue().restore().
        """

        PyFunceble.CONFIGURATION["auto_continue"] = True
        File(self.file).delete()

        self.set_counter(12)

        expected = {"up": 12, "down": 12, "invalid": 12, "tested": 12}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        saved = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "up": 17, "down": 12, "invalid": 8, "tested": 37
            }
        }

        Dict(saved).to_json(self.file)
        AutoContinue().restore()

        expected = saved[PyFunceble.CONFIGURATION["file_to_test"]]
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        self.set_counter(0)

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)
        PyFunceble.CONFIGURATION["auto_continue"] = False
        File(self.file).delete()

    def test_restore_old_system(self):
        """
        This method test AutoContinue().restore() for the case that we run the
        most recent version but with data from the old system.
        """

        PyFunceble.CONFIGURATION["auto_continue"] = True
        File(self.file).delete()

        old_system = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "number_of_up": 15,
                "number_of_down": 18,
                "number_of_invalid": 5,
                "number_of_tested": 38,
            }
        }

        Dict(old_system).to_json(self.file)
        AutoContinue().restore()

        expected = {"up": 15, "down": 18, "invalid": 5, "tested": 38}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        self.set_counter(0)

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)
        PyFunceble.CONFIGURATION["auto_continue"] = False
        File(self.file).delete()


if __name__ == "__main__":
    launch_tests()
