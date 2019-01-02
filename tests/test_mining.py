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

This submodule will test PyFunceble.mining.

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
# pylint: disable=protected-access

from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.helpers import Dict, File
from PyFunceble.mining import Mining


class TestMining(TestCase):
    """
    Test PyFunceble.mining
    """

    def setUp(self):
        """
        Setup everything needeed for the test.
        """

        PyFunceble.load_config(True)

        PyFunceble.CONFIGURATION["mining"] = True

        PyFunceble.CONFIGURATION["file_to_test"] = "this_file_is_a_ghost"

        self.file = (
            PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS["default_files"]["mining"]
        )

        self.excepted_content = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "myètherwället.com": ["www.google.com", "www.facebook.com"]
            }
        }

    def tearDown(self):
        """
        Setup every we do not need after the test.
        """

        PyFunceble.CONFIGURATION["mining"] = False

    def test_retrieve_file_not_exist(self):
        """
        Test the case that we want to retrieve a file that does not exist.
        """

        File(self.file).delete()

        actual = PyFunceble.path.isfile(self.file)
        expected = False

        self.assertEqual(expected, actual)

        Mining()._retrieve()

        excepted = {}
        self.assertEqual(excepted, PyFunceble.CONFIGURATION["mined"])

        PyFunceble.CONFIGURATION["mined"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_retrieve_file_exist(self):
        """
        Test the case that we want to retrieve a file that exist.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["to_test_type"] = "domain"

        Dict(self.excepted_content).to_json(self.file)
        Mining()._retrieve()

        self.assertEqual(self.excepted_content, PyFunceble.CONFIGURATION["mined"])

        del PyFunceble.CONFIGURATION["mined"]
        del PyFunceble.CONFIGURATION["to_test_type"]

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_add(self):
        """
        Test the addition subsystem.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        to_add = {"www.google.com": ["facebook.com", "www.facebook.com"]}

        expected = {PyFunceble.CONFIGURATION["file_to_test"]: to_add}

        Mining()._add(to_add)

        self.assertEqual(expected, PyFunceble.CONFIGURATION["mined"])

        to_add["www.google.com"].append("github.com")

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "www.google.com": ["facebook.com", "github.com", "www.facebook.com"]
            }
        }

        Mining()._add(to_add)

        self.assertEqual(expected, PyFunceble.CONFIGURATION["mined"])

        del PyFunceble.CONFIGURATION["mined"]

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_remove(self):
        """
        Test the deletion subsystem.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["mined"] = self.excepted_content
        PyFunceble.CONFIGURATION["to_test_type"] = "domain"
        PyFunceble.CONFIGURATION["to_test"] = "www.google.com"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "myètherwället.com": ["www.facebook.com"]
            }
        }

        Mining().remove()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["mined"])

        del PyFunceble.CONFIGURATION["mined"]
        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["to_test_type"]

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

    def test_list_of_mined(self):
        """
        Test Mining.list_of_mined
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["mined"] = self.excepted_content

        expected = ["www.facebook.com", "www.google.com"]

        self.assertEqual(expected, Mining().list_of_mined())

        del PyFunceble.CONFIGURATION["mined"]

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

    def test_backup(self):
        """
        Test the backup system.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["mined"] = self.excepted_content
        Mining()._backup()

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(
            self.excepted_content, Dict().from_json(File(self.file).read())
        )

        del PyFunceble.CONFIGURATION["mined"]

        File(self.file).delete()

        actual = PyFunceble.path.isfile(self.file)
        expected = False

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
