# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.engine.mining

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

from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.engine import Mining


class TestMining(TestCase):
    """
    Tests of PyFunceble.engine.mining.
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        PyFunceble.load_config(custom={"db_type": "json"})
        PyFunceble.CONFIGURATION.mining = True

        self.file_to_test = "this_file_is_a_ghost"

        self.storage_file = (
            PyFunceble.CONFIG_DIRECTORY + PyFunceble.OUTPUTS.default_files.mining
        )

        self.mining = Mining(self.file_to_test, parent_process=True)

        self.file_to_test_instance = PyFunceble.helpers.File(self.file_to_test)
        self.storage_file_instance = PyFunceble.helpers.File(self.storage_file)

        self.file_to_test_instance.delete()
        self.storage_file_instance.delete()

        self.excepted_content = {
            self.file_to_test: {
                "myètherwället.com": ["www.google.com", "www.facebook.com"]
            }
        }

    def tearDown(self):
        """
        Setups everything needed after the tests.
        """

        self.file_to_test_instance.delete()
        self.storage_file_instance.delete()

    def test_load_file_not_exist(self):
        """
        Tests the method which let us load the storage file
        for the case that the storage file does not exists.
        """

        expected = False
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        self.mining.load()

        expected = {self.file_to_test_instance.path: {}}

        self.assertEqual(expected, self.mining.database)

    def test_load_file_exist(self):
        """
        Tests the method which let us load the storage file
        for the case that the storage file exists.
        """

        expected = False
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        PyFunceble.helpers.Dict(self.excepted_content.copy()).to_json_file(
            self.storage_file_instance.path
        )

        expected = self.excepted_content.copy()

        self.mining.load()

        self.assertEqual(expected, self.mining.database)

    def test_add(self):
        """
        Tests the method which let us add a new entry.
        """

        expected = False
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        expected = {
            self.file_to_test_instance.path: {
                "www.google.com": ["facebook.com", "www.facebook.com"]
            }
        }

        self.mining["www.google.com"] = ["facebook.com", "www.facebook.com"]

        self.assertEqual(expected, self.mining.database)

        self.mining["www.google.com"] = ["github.com"]

        expected[self.file_to_test_instance.path]["www.google.com"].append("github.com")

        self.assertEqual(expected, self.mining.database)

    def test_remove(self):
        """
        Tests the method which let us remove a new entry.
        """

        expected = False
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        expected = {
            self.file_to_test_instance.path: {
                "myètherwället.com": ["www.facebook.com", "facebook.com"],
                "example.org": ["facebook.com"],
            }
        }
        self.mining.database = {self.file_to_test_instance.path: {}}

        self.mining["myètherwället.com"] = ["www.facebook.com", "facebook.com"]
        self.mining["example.org"] = ["www.facebook.com", "facebook.com"]

        self.mining.remove("example.org", "www.facebook.com")
        self.assertEqual(expected, self.mining.database)

    def test_list_of_mined(self):
        """
        Tests the method which let us get the list of previously mined
        data.
        """

        expected = False
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        self.mining.database = self.excepted_content.copy()

        expected = [
            ("myètherwället.com", "www.google.com"),
            ("myètherwället.com", "www.facebook.com"),
        ]

        self.assertEqual(expected, self.mining.list_of_mined())

    def test_save(self):
        """
        Tests the method which let us save the mined database.
        """

        expected = False
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        self.mining.database = self.excepted_content.copy()
        self.mining.save()

        expected = True
        actual = self.storage_file_instance.exists()

        self.assertEqual(expected, actual)

        expected = self.excepted_content.copy()
        actual = PyFunceble.helpers.Dict().from_json_file(
            self.storage_file_instance.path
        )

        self.assertEqual(
            expected, actual,
        )


if __name__ == "__main__":
    launch_tests()
