# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will test PyFunceble.database.

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
        This method setup everything needed for the test
        """

        PyFunceble.CONFIGURATION["file_to_test"] = "this_file_is_a_ghost"
        self.file = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["inactive_db"]
        )

        self.expected_content = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "1523447416": ["mÿethèrwallét.com", "||google.com^"],
                "to_test": ["myètherwället.com"],
            }
        }

        self.time_past = str(int(PyFunceble.time()) - (365 * 24 * 3600))
        self.time_future = str(int(PyFunceble.time()) + (365 * 24 * 3600))

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

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

    def test_retrieve_file_exist(self):
        """
        This method test the case that we want to retrieve a file that exist.
        """

        expected = False
        File(self.file).delete()

        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        Dict(self.expected_content).to_json(self.file)
        Database()._retrieve()

        self.assertEqual(self.expected_content, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_backup(self):
        """
        This method test the backup of the database.
        """

        PyFunceble.CONFIGURATION["inactive_db"] = self.expected_content

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        Database()._backup()

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(
            self.expected_content, Dict().from_json(File(self.file).read())
        )

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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
                self.time_future: ["hello.world", "world.hello"],
                "to_test": [],
            }
        }

        Dict(PyFunceble.CONFIGURATION["inactive_db"]).to_json(self.file)
        Database().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        expected = int(PyFunceble.time())
        actual = Database()._timestamp()

        self.assertGreaterEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        expected = int(PyFunceble.time())
        actual = Database()._timestamp()
        self.assertGreaterEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

    def test_add_path_does_not_exist(self):  # pylint: disable=invalid-name
        """
        This method test Database.add() for the case that the path does not exist.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(Database()._timestamp()): ["hello.world"]
            }
        }

        Database().add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = "http://hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(Database()._timestamp()): ["http://hello.world"]
            }
        }

        Database().add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = ""

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"
        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {timestamp: ["hello.world"]}
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["to_test"]
        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

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
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

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
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(int(timestamp) - (5 * 24 * 3600)): ["world.hello"]
            }
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(int(timestamp) - (5 * 24 * 3600)): ["world.hello"],
                timestamp: ["hello.world"],
            }
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(int(timestamp) - (5 * 24 * 3600)): ["world.hello"],
                "to_test": [PyFunceble.CONFIGURATION["to_test"]],
            }
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(int(timestamp) - (5 * 24 * 3600)): ["world.hello"],
                timestamp: ["hello.world"],
                "to_test": [],
            }
        }

        Database().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

    def test_remove(self):
        """
        This method test Database.remove().
        """

        timestamp = str(Database()._timestamp())

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: ["hello.world"],
                "to_test": ["hello.world", "world.hello"],
            }
        }
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: [],
                "to_test": ["world.hello"],
            }
        }

        Database().remove()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

    def test_content(self):
        """
        This method will test Database().content().
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        # Test of the case that everything goes right !
        timestamp = str(Database()._timestamp())

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: ["hello.world", "world.hello", "hello-world.com"],
                "to_test": ["hello.world", "world.hello"],
            }
        }
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

        expected = ["hello.world", "world.hello", "hello-world.com"]

        actual = Database().content()

        self.assertEqual(expected, actual)

        # Test of the case that the database is not activated
        PyFunceble.CONFIGURATION["inactive_database"] = False

        expected = []
        actual = Database().content()

        self.assertEqual(expected, actual)

        # Test of the case that there is nothing in the database.
        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["hello.world", "world.hello"]
            }
        }

        actual = Database().content()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = ""
        PyFunceble.CONFIGURATION["inactive_database"] = True

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)


if __name__ == "__main__":
    launch_tests()
