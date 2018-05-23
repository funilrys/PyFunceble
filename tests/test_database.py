"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.database


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
# pylint: disable=protected-access, import-error
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.database import Database
from PyFunceble.helpers import Dict, File


class TestDatabase(TestCase):
    """
    This class will test PyFunceble.database
    """

    def setUp(self):
        """
        This variable setup everything needed for the test
        """

        PyFunceble.CONFIGURATION["file_to_test"] = "this_file_is_a_ghost"
        self.file = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS["default_files"][
            "inactive_db"
        ]

        self.expected_content = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "1523447416": ["mÿethèrwallét.com", "||google.com^"],
                "to_test": ["myètherwället.com"],
            }
        }

        self.time_past = str(int(PyFunceble.strftime("%s")) - (365 * 24 * 3600))
        self.time_future = str(int(PyFunceble.strftime("%s")) + (365 * 24 * 3600))

    def test_retrieve_file_not_exist(self):
        """
        This method test the case that we want to retrieve a file that does not exist.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        Database()._retrieve()

        expected = {}
        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

    def test_retrieve_file_exist(self):
        """
        This method test the case that we want to retrieve a file that exist.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        Dict(self.expected_content).to_json(self.file)
        Database()._retrieve()

        self.assertEqual(self.expected_content, PyFunceble.CONFIGURATION["inactive_db"])

    def test_backup(self):
        """
        This method test the backup system.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = self.expected_content
        Database()._backup()

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(
            self.expected_content, Dict().from_json(File(self.file).read())
        )

    def test_add_to_test__path_not_exist(self):  # pylint: disable=invalid-name
        """
        This method test Database._add_to_test() for the case that the currently tested
        path is not present into the database.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        Database()._add_to_test("hello.world")

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"to_test": ["hello.world"]}
        }

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])
        self.assertEqual(expected, Dict().from_json(File(self.file).read()))

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_add_to_test__path_exist(self):  # pylint: disable=invalid-name
        """
        This method test Database._add_to_test() for the case that the path exist
        in the database.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"to_test": ["hello.world"]}
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["hello.world", "world.hello"]
            }
        }

        Database()._add_to_test("world.hello")

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])
        self.assertEqual(expected, Dict().from_json(File(self.file).read()))

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_add_to_test__path_exist_not_test(self):  # pylint: disable=invalid-name
        """
        This method test Database._add_to_test() for the case that the path exist
        in the database but the not `to_test` index.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {}
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"to_test": ["hello.world"]}
        }

        Database()._add_to_test("hello.world")

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])
        self.assertEqual(expected, Dict().from_json(File(self.file).read()))

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_to_test__path_not_exist(self):  # pylint: disable=invalid-name
        """
        This method test Database.to_test() for the case that the path does not exist.
        """
        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        expected = {PyFunceble.CONFIGURATION["file_to_test"]: {}}

        Database().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])
        self.assertEqual(expected, Dict().from_json(File(self.file).read()))

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_to_test__path_exist_time_past(self):  # pylint: disable=invalid-name
        """
        This method test Database.to_test() for the case that the path exist but
        the timestamp is in the past.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_past: ["hello.world", "world.hello"],
                "to_test": ["github.com"],
            }
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["github.com", "hello.world", "world.hello"]
            }
        }

        Dict(PyFunceble.CONFIGURATION["inactive_db"]).to_json(self.file)
        Database().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])
        self.assertEqual(expected, Dict().from_json(File(self.file).read()))

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_to_test__path_exist_time_future(self):  # pylint: disable=invalid-name
        """
        This method test Database.to_test() for the case that the path exist but
        the timestamp is in the future.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_future: ["hello.world", "world.hello"]
            }
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_future: ["hello.world", "world.hello"], "to_test": []
            }
        }

        Dict(PyFunceble.CONFIGURATION["inactive_db"]).to_json(self.file)
        Database().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])
        self.assertEqual(expected, Dict().from_json(File(self.file).read()))

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_timestamp_path_does_not_exit(self):  # pylint: disable=invalid-name
        """
        This method test Database.timestamp() for the case that the path does
        not exist but the time is in the past.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        expected = int(PyFunceble.strftime("%s"))
        actual = Database()._timestamp()

        self.assertEqual(expected, actual)

    def test_timestamp_path_exist_time_past(self):  # pylint: disable=invalid-name
        """
        This method test Database.timestamp() for the case that the path exist but
        the time is in the past.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_past: ["hello.world", "world.hello"]
            }
        }

        expected = int(PyFunceble.strftime("%s"))
        actual = Database()._timestamp()
        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_timestamp_path_exist_time_future(self):  # pylint: disable=invalid-name
        """
        This method test Database.timestamp() for the case that the path exist but
        the time is in the future.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_future: ["hello.world", "world.hello"]
            }
        }

        expected = int(self.time_future)
        actual = Database()._timestamp()
        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_add_path_does_not_exist(self):  # pylint: disable=invalid-name
        """
        This method test Database.add() for the case that the path does not exist.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["domain"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(Database()._timestamp()): ["hello.world"]
            }
        }

        Database().add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}

    def test_add_file_path_not_present(self):  # pylint: disable=invalid-name
        """
        This method test Database.add() for the case that the path is not
        present into the database.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        timestamp = str(Database()._timestamp())
        PyFunceble.CONFIGURATION["domain"] = "hello.world"
        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {timestamp: ["hello.world"]}
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["domain"]

    def test_add_file_path_present(self):  # pylint: disable=invalid-name
        """
        This method test Database.add() for the case that the path is present
        into the database.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        timestamp = str(Database()._timestamp())
        PyFunceble.CONFIGURATION["domain"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: ["world.hello", "hello.world"]
            }
        }

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {timestamp: ["world.hello"]}
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"0": ["world.hello"]}
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["world.hello"], timestamp: ["hello.world"]
            }
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "0": ["world.hello"], "to_test": ["hello.world"]
            }
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["world.hello"], timestamp: ["hello.world"]
            }
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

    def test_remove(self):
        """
        This method test Database.remove().
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        timestamp = str(Database()._timestamp())

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: ["hello.world"], "to_test": ["hello.world", "world.hello"]
            }
        }
        PyFunceble.CONFIGURATION["domain"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: [], "to_test": ["world.hello"]
            }
        }

        Database().remove()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        self.assertEqual(expected, Dict().from_json(File(self.file).read()))
        PyFunceble.CONFIGURATION["inactive_db"] = {}


if __name__ == "__main__":
    launch_tests()
