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

This submodule will test PyFunceble.database.

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
# pylint: disable=protected-access, import-error
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.helpers import Dict, File
from PyFunceble.inactive_db import InactiveDB


class TestInactiveDB(TestCase):
    """
    Test PyFunceble.database.Inactive
    """

    def setUp(self):
        """
        Setup everything needed for the test
        """

        PyFunceble.load_config(True)

        self.file_to_test = "this_file_is_a_ghost"

        self.file = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["inactive_db"]
        )

        self.expected_content = {
            self.file_to_test: {
                "0": ["mÿethèrwallét.com", "||google.com^"],
                "to_test": ["myètherwället.com"],
            }
        }

        self.time_past = str(int(PyFunceble.time()) - (365 * 24 * 3600))
        self.time_future = str(int(PyFunceble.time()) + (365 * 24 * 3600))

        self.inactive_db = InactiveDB(self.file_to_test)

    def test_file_not_exist(self):
        """
        Test if everything is right with the generated
        file.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_load_file_not_exist(self):
        """
        Test the case that we want to load the database file that does not exist.
        """

        self.test_file_not_exist()

        self.inactive_db.load()

        expected = {self.file_to_test: {"to_test": []}}

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_load_file_exist(self):
        """
        Test the case that we want to load a file that exist.
        """

        self.test_file_not_exist()

        Dict(self.expected_content).to_json(self.file)
        self.inactive_db.database = {}
        self.inactive_db.load()

        self.assertEqual(self.expected_content, self.inactive_db.database)

        self.test_file_not_exist()

    def test_save(self):
        """
        Test the saving of the inactive database.
        """

        self.test_file_not_exist()
        self.inactive_db.database = self.expected_content

        self.inactive_db.save()

        self.assertEqual(
            self.expected_content, Dict().from_json(File(self.file).read())
        )

        self.test_file_not_exist()

    def test_add_to_test__path_not_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive._add_to_test() for the case that the currently tested
        path is not present into the Inactive.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {}
        self.inactive_db._add_to_test("hello.world")

        expected = {self.file_to_test: {"to_test": ["hello.world"]}}

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_add_to_test__path_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive._add_to_test() for the case that the path exist
        in the Inactive.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {self.file_to_test: {"to_test": ["hello.world"]}}

        expected = {self.file_to_test: {"to_test": ["hello.world", "world.hello"]}}

        self.inactive_db._add_to_test("world.hello")

        self.assertEqual(expected, self.inactive_db.database)
        self.test_file_not_exist()

    def test_add_to_test__path_exist_not_test(self):  # pylint: disable=invalid-name
        """
        Test Inactive._add_to_test() for the case that the path exist
        in the database but the not `to_test` index.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {self.file_to_test: {}}

        expected = {self.file_to_test: {"to_test": ["hello.world"]}}

        self.inactive_db._add_to_test("hello.world")

        self.assertEqual(expected, self.inactive_db.database)
        self.test_file_not_exist()

    def test_initiate__path_not_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive.initiate() for the case that the path does not exist.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {}

        expected = {self.file_to_test: {"to_test": []}}

        self.inactive_db.initiate()

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_initiate__path_exist_time_past(self):  # pylint: disable=invalid-name
        """
        Test Inactive.initiate() for the case that the path exist but
        the timestamp is in the past.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {
            self.file_to_test: {
                self.time_past: ["hello.world", "world.hello"],
                "to_test": ["github.com"],
            }
        }

        expected = {
            self.file_to_test: {"to_test": ["github.com", "hello.world", "world.hello"]}
        }

        self.inactive_db.save()
        self.inactive_db.initiate()

        self.assertEqual(expected, self.inactive_db.database)
        self.test_file_not_exist()

    def test_initiate__path_exist_time_future(self):  # pylint: disable=invalid-name
        """
        Test Inactive.initiate() for the case that the path exist but
        the timestamp is in the future.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {
            self.file_to_test: {self.time_future: ["hello.world", "world.hello"]}
        }

        expected = {
            self.file_to_test: {
                self.time_future: ["hello.world", "world.hello"],
                "to_test": [],
            }
        }

        self.inactive_db.save()
        self.inactive_db.initiate()

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_timestamp_path_does_not_exit(self):  # pylint: disable=invalid-name
        """
        Test Inactive._timestamp() for the case that the path does
        not exist but the time is in the past.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {}

        expected = int(PyFunceble.time())
        actual = self.inactive_db._timestamp()

        self.assertGreaterEqual(expected, actual)

        self.test_file_not_exist()

    def test_timestamp_path_exist_time_past(self):  # pylint: disable=invalid-name
        """
        Test Inactive._timestamp() for the case that the path exist but
        the time is in the past.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {
            self.file_to_test: {self.time_past: ["hello.world", "world.hello"]}
        }

        expected = int(PyFunceble.time())
        actual = self.inactive_db._timestamp()

        self.assertGreaterEqual(expected, actual)

        self.test_file_not_exist()

    def test_timestamp_path_exist_time_future(self):  # pylint: disable=invalid-name
        """
        Test Inactive._timestamp() for the case that the path exist but
        the time is in the future.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {
            self.file_to_test: {self.time_future: ["hello.world", "world.hello"]}
        }

        expected = int(self.time_future)
        actual = self.inactive_db._timestamp()

        self.assertEqual(expected, actual)

        self.test_file_not_exist()

    def test_add_path_does_not_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive.add() for the case that the path does not exist.
        """

        self.test_file_not_exist()

        self.inactive_db.database = {}
        subject = "hello.world"

        expected = {
            self.file_to_test: {str(self.inactive_db._timestamp()): ["hello.world"]}
        }

        self.inactive_db.add(subject)
        self.assertEqual(expected, self.inactive_db.database)

        self.inactive_db.database = {}
        subject = "http://hello.world"

        expected = {
            self.file_to_test: {
                str(self.inactive_db._timestamp()): ["http://hello.world"]
            }
        }

        self.inactive_db.add(subject)
        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_add_file_path_not_present(self):  # pylint: disable=invalid-name
        """
        Test Inactive.add() for the case that the path is not
        present into the Inactive.
        """

        self.test_file_not_exist()

        timestamp = str(self.inactive_db._timestamp())
        subject = "hello.world"
        expected = {self.file_to_test: {timestamp: ["hello.world"], "to_test": []}}

        self.inactive_db.add(subject)

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_add_file_path_present(self):  # pylint: disable=invalid-name
        """
        Test Inactive.add() for the case that the path is present
        into the Inactive.
        """

        self.test_file_not_exist()

        timestamp = str(self.inactive_db._timestamp())
        subject = "hello.world"

        expected = {
            self.file_to_test: {
                timestamp: ["hello.world", "world.hello"],
                "to_test": [],
            }
        }

        self.inactive_db.database = {
            self.file_to_test: {timestamp: ["world.hello"], "to_test": ["hello.world"]}
        }

        self.inactive_db.add(subject)

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_remove(self):
        """
        Test Inactive.remove().
        """

        timestamp = str(self.inactive_db._timestamp())

        self.test_file_not_exist()

        self.inactive_db.database = {
            self.file_to_test: {
                timestamp: ["hello.world"],
                "to_test": ["hello.world", "world.hello"],
            }
        }
        subject = "hello.world"

        expected = {self.file_to_test: {timestamp: [], "to_test": ["world.hello"]}}

        self.inactive_db.remove(subject)

        self.assertEqual(expected, self.inactive_db.database)

        self.test_file_not_exist()

    def test_is_present(self):
        """
        Test the presence of element in the databse.
        """

        self.test_file_not_exist()

        # Test of the case that everything goes right !
        timestamp = str(self.inactive_db._timestamp())

        self.inactive_db.database = {
            self.file_to_test: {
                timestamp: ["hello.world", "world.hello", "hello-world.com"],
                "to_test": ["hello.world", "world.hello"],
            }
        }
        subject = "hello.world"

        expected = True
        actual = subject in self.inactive_db

        self.assertEqual(expected, actual)

        del self.inactive_db.database[self.file_to_test][timestamp]
        subject = "world.hello.world"
        expected = False
        actual = subject in self.inactive_db

        self.assertEqual(expected, actual)

        self.assertEqual(expected, actual)

        self.test_file_not_exist()


if __name__ == "__main__":
    launch_tests()
