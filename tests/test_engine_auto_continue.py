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

Tests of PyFunceble.engine.auto_continue

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
from PyFunceble.engine import AutoContinue


class TestAutoContinue(TestCase):
    """
    Tests of PyFunceble.engine.auto_continue
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        PyFunceble.load_config(
            generate_directory_structure=False, custom={"db_type": "json"}
        )

        self.storage_file = (
            PyFunceble.OUTPUT_DIRECTORY
            + PyFunceble.OUTPUTS.parent_directory
            + PyFunceble.OUTPUTS.logs.filenames.auto_continue
        )

        self.file_to_test = "this_file_is_a_ghost"
        self.our_dataset = {self.file_to_test: {"INVALID": ["hello", "world"]}}

        self.auto_continue = AutoContinue(self.file_to_test, parent_process=True)

        PyFunceble.helpers.File(self.storage_file).delete()

    def tearDown(self):
        """
        Setups everything needed after a test.
        """

        PyFunceble.helpers.File(self.storage_file).delete()

    def test_authorization(self):
        """
        Tests of the authorization method.
        """

        expected = False

        PyFunceble.CONFIGURATION.auto_continue = False
        PyFunceble.CONFIGURATION.no_files = True
        actual = self.auto_continue.authorization()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION.auto_continue = True
        PyFunceble.CONFIGURATION.no_files = True
        actual = self.auto_continue.authorization()

        self.assertEqual(expected, actual)

        expected = True

        PyFunceble.CONFIGURATION.auto_continue = True
        PyFunceble.CONFIGURATION.no_files = False
        actual = self.auto_continue.authorization()

        self.assertEqual(expected, actual)

    def test_save(self):
        """
        Tests of the saving method.
        """

        self.auto_continue.database = self.our_dataset.copy()
        self.auto_continue.save()

        expected = True
        actual = PyFunceble.helpers.File(self.storage_file).exists()

        self.assertEqual(expected, actual)

        expected = self.our_dataset.copy()
        actual = PyFunceble.helpers.Dict().from_json_file(self.storage_file)

        self.assertEqual(expected, actual)

    def test_load(self):
        """
        Tests of the loading method.
        """

        PyFunceble.helpers.Dict(self.our_dataset.copy()).to_json_file(self.storage_file)

        expected = self.our_dataset.copy()
        self.auto_continue.load()

        self.assertEqual(expected, self.auto_continue.database)

    def test_is_present(self):
        """
        Tests of the way we check if a method is present.
        """

        self.auto_continue.database = self.our_dataset.copy()

        expected = True
        actual = "hello" in self.auto_continue

        self.assertEqual(expected, actual)

        expected = False
        actual = "hello.world" in self.auto_continue

        self.assertEqual(expected, actual)

    def test_is_empty(self):
        """
        Tests of the method which checks if the database
        of the current file is empty.
        """

        self.auto_continue.database = {}

        expected = True
        actual = self.auto_continue.is_empty()

        self.assertEqual(expected, actual)

        self.auto_continue.database = {self.file_to_test: {}}

        actual = self.auto_continue.is_empty()

        self.assertEqual(expected, actual)

        self.auto_continue.database = self.our_dataset.copy()

        expected = False
        actual = self.auto_continue.is_empty()

        self.assertEqual(expected, actual)

    def test_add(self):
        """
        Tests of the addition method.
        """

        self.auto_continue.database = {}

        self.auto_continue.add("hello.world", "ACTIVE")
        self.auto_continue.add("world.hello", "ACTIVE")
        self.auto_continue.add("hello.world", "ACTIVE")

        expected = {
            self.file_to_test: {"ACTIVE": ["hello.world", "world.hello", "hello.world"]}
        }

        self.assertEqual(expected, self.auto_continue.database)

        self.auto_continue.add("hello.world.hello", "INACTIVE")

        expected[self.file_to_test]["INACTIVE"] = ["hello.world.hello"]

        self.assertEqual(expected, self.auto_continue.database)

    def test_clean(self):
        """
        Tests of the cleaning method.
        """

        self.auto_continue.database = self.our_dataset.copy()

        expected = {self.file_to_test: {}}

        self.auto_continue.clean()

        self.assertEqual(expected, self.auto_continue.database)

    def test_get_already_tested(self):
        """
        Tests of the method which provides the list of already tested subject.
        """

        self.auto_continue.database = {}

        self.auto_continue.add("hello.world", "ACTIVE")
        self.auto_continue.add("world.hello", "ACTIVE")

        expected = {"hello.world", "world.hello"}
        actual = self.auto_continue.get_already_tested()

        self.assertEqual(expected, actual)

        self.auto_continue.add("hello.world.hello", "INACTIVE")

        expected = {"hello.world", "world.hello", "hello.world.hello"}
        actual = self.auto_continue.get_already_tested()

        self.assertEqual(expected, actual)

        self.auto_continue.clean()

        expected = set()
        actual = self.auto_continue.get_already_tested()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
