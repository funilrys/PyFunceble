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

This submodule will test PyFunceble.auto_continue.

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
# pylint: disable=import-error
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.config import Load
from PyFunceble.helpers import Dict, File


class TestsAutoContinue(TestCase):
    """
    Testing of PyFunceble.AutoSave().
    """

    def setUp(self):
        """
        Setup the needed variables.
        """

        Load(PyFunceble.CURRENT_DIRECTORY)

        self.file_to_work_with = (
            PyFunceble.OUTPUT_DIRECTORY
            + PyFunceble.OUTPUTS["parent_directory"]
            + PyFunceble.OUTPUTS["logs"]["filenames"]["auto_continue"]
        )

        PyFunceble.CONFIGURATION["file_to_test"] = "hello.world"
        self.types = ["up", "down", "invalid", "tested"]

    def set_counter(self, to_set=15):
        """
        Set the counter at a given number.

        Argument:
            - to_set: int
                The number to set to every counter.
        """

        for string in self.types:
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: to_set})

    def test_delete_file(self):
        """
        Delete and ensure that the file we are working with does not exist.
        """

        File(self.file_to_work_with).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file_to_work_with)

        self.assertEqual(expected, actual)

    def test_backup(self):
        """
        Test AutoContinue().backup().
        """

        self.test_delete_file()
        PyFunceble.CONFIGURATION["auto_continue"] = True
        self.set_counter(to_set=25)

        AutoContinue().backup()

        expected = True
        actual = PyFunceble.path.isfile(self.file_to_work_with)

        self.assertEqual(expected, actual)

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "up": 25,
                "down": 25,
                "invalid": 25,
                "tested": 25,
            }
        }
        actual = Dict().from_json(File(self.file_to_work_with).read())

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["auto_continue"]
        self.test_delete_file()

    def test_backup_not_activated(self):
        """
        Test AutoContinue().backup() for the case that we did not
        activated the backup system.
        """

        self.test_delete_file()
        PyFunceble.CONFIGURATION["auto_continue"] = False

        AutoContinue().backup()

        expected = False
        actual = PyFunceble.path.isfile(self.file_to_work_with)

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["auto_continue"]
        self.test_delete_file()

    def test_restore(self):
        """
        Test AutoContinue().restore().
        """

        self.test_delete_file()
        PyFunceble.CONFIGURATION["auto_continue"] = True
        self.set_counter(12)

        expected = {"up": 12, "down": 12, "invalid": 12, "tested": 12}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        saved = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "up": 17,
                "down": 12,
                "invalid": 8,
                "tested": 37,
            }
        }

        Dict(saved).to_json(self.file_to_work_with)
        AutoContinue().restore()

        expected = saved[PyFunceble.CONFIGURATION["file_to_test"]]
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        self.set_counter(0)

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["auto_continue"]
        self.test_delete_file()

    def test_restore_old_system(self):
        """
        Test AutoContinue().restore() for the case that we run the
        most recent version but with data from the old system.
        """

        self.test_delete_file()
        PyFunceble.CONFIGURATION["auto_continue"] = True

        old_system = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "number_of_up": 15,
                "number_of_down": 18,
                "number_of_invalid": 5,
                "number_of_tested": 38,
            }
        }

        Dict(old_system).to_json(self.file_to_work_with)
        AutoContinue().restore()

        expected = {"up": 15, "down": 18, "invalid": 5, "tested": 38}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        self.set_counter(0)

        expected = {"up": 0, "down": 0, "invalid": 0, "tested": 0}
        actual = PyFunceble.CONFIGURATION["counter"]["number"]

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["auto_continue"]
        self.test_delete_file()


if __name__ == "__main__":
    launch_tests()
