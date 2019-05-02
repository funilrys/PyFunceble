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
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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
from PyFunceble.helpers import Dict, File


class TestsAutoContinue(TestCase):
    """
    Testing of PyFunceble.AutoSave().
    """

    def setUp(self):
        """
        Setup the needed variables.
        """

        PyFunceble.load_config(generate_directory_structure=False)

        self.file_to_work_with = (
            PyFunceble.OUTPUT_DIRECTORY
            + PyFunceble.OUTPUTS["parent_directory"]
            + PyFunceble.OUTPUTS["logs"]["filenames"]["auto_continue"]
        )

        self.file_to_test = "hello.world"
        self.auto_continue = AutoContinue(self.file_to_test)

    def test_delete_file(self):
        """
        Delete and ensure that the file we are working with does not exist.
        """

        File(self.file_to_work_with).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file_to_work_with)

        self.assertEqual(expected, actual)

    def test_save(self):
        """
        Test AutoContinue().backup().
        """

        self.test_delete_file()
        self.auto_continue.authorized = True

        self.auto_continue.database = {
            self.file_to_test: {"Hello": "INVALID", "world": "INVALID"}
        }
        self.auto_continue.save()

        expected = True
        actual = PyFunceble.path.isfile(self.file_to_work_with)
        self.assertEqual(expected, actual)

        expected = {self.file_to_test: {"Hello": "INVALID", "world": "INVALID"}}

        actual = Dict().from_json(File(self.file_to_work_with).read())

        self.assertEqual(expected, actual)
        self.test_delete_file()

    def test_save_not_activated(self):
        """
        Test AutoContinue().save() for the case that we did not
        activated the backup system.
        """

        self.test_delete_file()

        self.auto_continue.authorized = False
        self.auto_continue.database = {"hello": "world"}

        self.auto_continue.save()

        expected = False
        actual = PyFunceble.path.isfile(self.file_to_work_with)

        self.assertEqual(expected, actual)

        self.test_delete_file()

    def test_load(self):
        """
        Test AutoContinue().restore().
        """

        self.test_delete_file()
        self.auto_continue.authorized = True

        Dict({"hello": "world"}).to_json(self.file_to_work_with)

        expected = {"hello": "world"}
        self.auto_continue.load()

        self.assertEqual(expected, self.auto_continue.database)

        self.test_delete_file()

    def test_is_present(self):
        """
        Test the presence of elements.
        """

        self.test_delete_file()
        self.auto_continue.authorized = True

        for status in ["ACTIVE", "INACTIVE", "INVALID"]:
            self.auto_continue.database = {
                self.file_to_test: {
                    "hello": status,
                    "world": "INACTIVE",
                    "hehe": "INVALID",
                }
            }

            expected = True
            actual = "hello" in self.auto_continue

            self.assertEqual(expected, actual)

        expected = False
        actual = "hello.world" in self.auto_continue

        self.assertEqual(expected, actual)

        self.test_delete_file()

    def test_is_empty(self):
        """
        Test if the databse if empty.
        """

        self.test_delete_file()
        self.auto_continue.authorized = True

        self.auto_continue.database = {}

        expected = True
        actual = self.auto_continue.is_empty()

        self.assertEqual(expected, actual)

        self.auto_continue.database = {self.file_to_test: {"hello": "world"}}

        expected = False
        actual = self.auto_continue.is_empty()

        self.assertEqual(expected, actual)

        self.test_delete_file()

    def test_add(self):
        """
        Test the addition of an element.
        """

        self.test_delete_file()
        self.auto_continue.authorized = True

        self.auto_continue.database = {}

        self.auto_continue.add("hello.world", "ACTIVE")
        self.auto_continue.add("world.hello", "ACTIVE")

        expected = {self.file_to_test: {"ACTIVE": ["hello.world", "world.hello"]}}

        self.assertEqual(expected, self.auto_continue.database)

        self.auto_continue.add("hello.world.hello", "INACTIVE")

        expected = {
            self.file_to_test: {
                "ACTIVE": ["hello.world", "world.hello"],
                "INACTIVE": ["hello.world.hello"],
            }
        }

        self.assertEqual(expected, self.auto_continue.database)

        expected = {self.file_to_test: {}}

        self.auto_continue.clean()
        self.assertEqual(expected, self.auto_continue.database)

        self.test_delete_file()


if __name__ == "__main__":
    launch_tests()
