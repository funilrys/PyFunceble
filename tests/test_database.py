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
from PyFunceble.database import Inactive, Whois
from PyFunceble.helpers import Dict, File


class TestDatabaseInactive(TestCase):
    """
    Test PyFunceble.database.Inactive
    """

    def setUp(self):
        """
        Setup everything needed for the test
        """

        PyFunceble.load_config(True)

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

    def test_file_not_exist(self):
        """
        Test if everything is right with the generated
        file.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_retrieve_file_not_exist(self):
        """
        Test the case that we want to retrieve a file that does not exist.
        """

        self.test_file_not_exist()

        Inactive()._retrieve()

        expected = {}

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_retrieve_file_exist(self):
        """
        Test the case that we want to retrieve a file that exist.
        """

        self.test_file_not_exist()

        Dict(self.expected_content).to_json(self.file)
        Inactive()._retrieve()

        self.assertEqual(self.expected_content, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_backup(self):
        """
        Test the backup of the Inactive.
        """

        self.test_file_not_exist()
        PyFunceble.CONFIGURATION["inactive_db"] = self.expected_content

        Inactive()._backup()

        self.assertEqual(
            self.expected_content, Dict().from_json(File(self.file).read())
        )

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_add_to_test__path_not_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive._add_to_test() for the case that the currently tested
        path is not present into the Inactive.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        Inactive()._add_to_test("hello.world")

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"to_test": ["hello.world"]}
        }

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_add_to_test__path_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive._add_to_test() for the case that the path exist
        in the Inactive.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"to_test": ["hello.world"]}
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["hello.world", "world.hello"]
            }
        }

        Inactive()._add_to_test("world.hello")

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_add_to_test__path_exist_not_test(self):  # pylint: disable=invalid-name
        """
        Test Inactive._add_to_test() for the case that the path exist
        in the database but the not `to_test` index.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {}
        }

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {"to_test": ["hello.world"]}
        }

        Inactive()._add_to_test("hello.world")

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_to_test__path_not_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive.to_test() for the case that the path does not exist.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        expected = {PyFunceble.CONFIGURATION["file_to_test"]: {}}

        Inactive().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_to_test__path_exist_time_past(self):  # pylint: disable=invalid-name
        """
        Test Inactive.to_test() for the case that the path exist but
        the timestamp is in the past.
        """

        self.test_file_not_exist()

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
        Inactive().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_to_test__path_exist_time_future(self):  # pylint: disable=invalid-name
        """
        Test Inactive.to_test() for the case that the path exist but
        the timestamp is in the future.
        """

        self.test_file_not_exist()

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
        Inactive().to_test()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_timestamp_path_does_not_exit(self):  # pylint: disable=invalid-name
        """
        Test Inactive.timestamp() for the case that the path does
        not exist but the time is in the past.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {}

        expected = int(PyFunceble.time())
        actual = Inactive()._timestamp()

        self.assertGreaterEqual(expected, actual)

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_timestamp_path_exist_time_past(self):  # pylint: disable=invalid-name
        """
        Test Inactive.timestamp() for the case that the path exist but
        the time is in the past.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_past: ["hello.world", "world.hello"]
            }
        }

        expected = int(PyFunceble.time())
        actual = Inactive()._timestamp()

        self.assertGreaterEqual(expected, actual)

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_timestamp_path_exist_time_future(self):  # pylint: disable=invalid-name
        """
        Test Inactive.timestamp() for the case that the path exist but
        the time is in the future.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                self.time_future: ["hello.world", "world.hello"]
            }
        }

        expected = int(self.time_future)
        actual = Inactive()._timestamp()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_add_path_does_not_exist(self):  # pylint: disable=invalid-name
        """
        Test Inactive.add() for the case that the path does not exist.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(Inactive()._timestamp()): ["hello.world"]
            }
        }

        Inactive().add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        PyFunceble.CONFIGURATION["inactive_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = "http://hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                str(Inactive()._timestamp()): ["http://hello.world"]
            }
        }

        Inactive().add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        PyFunceble.CONFIGURATION["to_test"] = ""
        self.test_file_not_exist()

    def test_add_file_path_not_present(self):  # pylint: disable=invalid-name
        """
        Test Inactive.add() for the case that the path is not
        present into the Inactive.
        """

        self.test_file_not_exist()

        timestamp = str(Inactive()._timestamp())
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"
        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {timestamp: ["hello.world"]}
        }

        Inactive().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["inactive_db"]

        self.test_file_not_exist()

    def test_add_file_path_present(self):  # pylint: disable=invalid-name
        """
        Test Inactive.add() for the case that the path is present
        into the Inactive.
        """

        self.test_file_not_exist()

        timestamp = str(Inactive()._timestamp())
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

        expected = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: ["world.hello", "hello.world"]
            }
        }

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {timestamp: ["world.hello"]}
        }

        Inactive().add()
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

        Inactive().add()
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

        Inactive().add()
        actual = Dict().from_json(File(self.file).read())

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_remove(self):
        """
        Test Inactive.remove().
        """

        timestamp = str(Inactive()._timestamp())

        self.test_file_not_exist()

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

        Inactive().remove()

        self.assertEqual(expected, PyFunceble.CONFIGURATION["inactive_db"])

        del PyFunceble.CONFIGURATION["inactive_db"]
        self.test_file_not_exist()

    def test_content(self):
        """
        Test Inactive.content().
        """

        self.test_file_not_exist()

        # Test of the case that everything goes right !
        timestamp = str(Inactive()._timestamp())

        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                timestamp: ["hello.world", "world.hello", "hello-world.com"],
                "to_test": ["hello.world", "world.hello"],
            }
        }
        PyFunceble.CONFIGURATION["to_test"] = "hello.world"

        expected = ["hello.world", "world.hello", "hello-world.com"]

        actual = Inactive().content()

        self.assertEqual(expected, actual)

        # Test of the case that the database is not activated
        PyFunceble.CONFIGURATION["inactive_database"] = False

        expected = []
        actual = Inactive().content()

        self.assertEqual(expected, actual)

        # Test of the case that there is nothing in the Inactive.
        PyFunceble.CONFIGURATION["inactive_db"] = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "to_test": ["hello.world", "world.hello"]
            }
        }

        actual = Inactive().content()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["inactive_db"]
        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["inactive_database"]

        self.test_file_not_exist()


class TestDatabaseWhois(TestCase):
    """
    Test PyFunceble.database.Whois
    """

    def setUp(self):
        """
        Setup everything needed for the test
        """

        PyFunceble.CONFIGURATION["file_to_test"] = "this_file_is_a_ghost"
        self.file = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["whois_db"]
        )

        self.expected_content = {
            PyFunceble.CONFIGURATION["file_to_test"]: {
                "google.com": {
                    "epoch": "1600034400",
                    "expiration_date": "14-sep-2020",
                    "state": "future",
                },
                "github.com": {
                    "epoch": "1602194400",
                    "expiration_date": "09-oct-2020",
                    "state": "future",
                },
            }
        }

    def test_file_not_exist(self):
        """
        Test if everything is right with the generated
        file.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_authorization(self):
        """
        Test the authorization method.
        """

        PyFunceble.CONFIGURATION["no_whois"] = True
        PyFunceble.CONFIGURATION["whois_database"] = False
        expected = False

        self.assertEqual(expected, Whois()._authorization())

        PyFunceble.CONFIGURATION["no_whois"] = False
        PyFunceble.CONFIGURATION["whois_database"] = False

        self.assertEqual(expected, Whois()._authorization())

        PyFunceble.CONFIGURATION["no_whois"] = True
        PyFunceble.CONFIGURATION["whois_database"] = True

        self.assertEqual(expected, Whois()._authorization())

        PyFunceble.CONFIGURATION["no_whois"] = False
        PyFunceble.CONFIGURATION["whois_database"] = True
        expected = True

        self.assertEqual(expected, Whois()._authorization())

    def test_retrieve_file_not_exist(self):
        """
        Test the case that we want to retrieve a file that does not exist.
        """

        self.test_file_not_exist()
        Whois()._retrieve()

        expected = {}
        self.assertEqual(expected, PyFunceble.CONFIGURATION["whois_db"])

        del PyFunceble.CONFIGURATION["whois_db"]

        self.test_file_not_exist()

    def test_retrieve_file_exist(self):
        """
        Test the case that we want to retrieve a file that exist.
        """

        self.test_file_not_exist()

        Dict(self.expected_content).to_json(self.file)
        Whois()._retrieve()

        self.assertEqual(self.expected_content, PyFunceble.CONFIGURATION["whois_db"])

        del PyFunceble.CONFIGURATION["whois_db"]

        self.test_file_not_exist()

    def test_backup(self):
        """
        Test the backup of the database.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["whois_db"] = self.expected_content
        Whois()._backup()

        expected = True
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["whois_db"]
        Whois()._retrieve()

        self.assertEqual(self.expected_content, PyFunceble.CONFIGURATION["whois_db"])

        del PyFunceble.CONFIGURATION["whois_db"]

        self.test_file_not_exist()

    def test_is_in_database(self):
        """
        Test the check.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["whois_db"] = self.expected_content
        PyFunceble.CONFIGURATION["to_test"] = "google.com"

        expected = True
        actual = Whois().is_in_database()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["to_test"] = "hello.google.com"

        expected = False
        actual = Whois().is_in_database()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["whois_db"]
        self.test_file_not_exist()

    def test_is_time_older(self):
        """
        Test if a time is older or not than the current date.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["whois_db"] = self.expected_content
        PyFunceble.CONFIGURATION["to_test"] = "google.com"

        PyFunceble.CONFIGURATION["whois_db"][PyFunceble.CONFIGURATION["file_to_test"]][
            "google.com"
        ]["epoch"] = PyFunceble.time() - (15 * (60 * 60 * 24))

        expected = True
        actual = Whois().is_time_older()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["whois_db"][PyFunceble.CONFIGURATION["file_to_test"]][
            "google.com"
        ]["epoch"] = PyFunceble.time() + (15 * (60 * 60 * 24))

        expected = False
        actual = Whois().is_time_older()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["whois_db"]
        self.test_file_not_exist()

    def test_get_expiration_date(self):
        """
        Test the way we get the expiration date from the database.
        """

        self.test_file_not_exist()

        PyFunceble.CONFIGURATION["whois_db"] = self.expected_content
        PyFunceble.CONFIGURATION["to_test"] = "google.com"

        expected = "14-sep-2020"
        actual = Whois().get_expiration_date()

        self.assertEqual(expected, actual)

        PyFunceble.CONFIGURATION["to_test"] = "hello.google.com"

        expected = None
        actual = Whois().get_expiration_date()

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["whois_db"]
        self.test_file_not_exist()

    def test_add(self):
        """
        Test the addition for the case that the element is not into
        the database.
        """

        self.test_file_not_exist()
        del PyFunceble.CONFIGURATION["file_to_test"]

        PyFunceble.CONFIGURATION["whois_db"] = {}
        PyFunceble.CONFIGURATION["to_test"] = "microsoft.google.com"

        epoch = str(
            int(PyFunceble.mktime(PyFunceble.strptime("25-dec-2022", "%d-%b-%Y")))
        )
        expected = {
            "single_testing": {
                "microsoft.google.com": {
                    "epoch": epoch,
                    "expiration_date": "25-dec-2022",
                    "state": "future",
                }
            }
        }

        Whois("25-dec-2022").add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["whois_db"])

        PyFunceble.CONFIGURATION["whois_db"]["single_testing"]["microsoft.google.com"][
            "state"
        ] = "hello"

        Whois("25-dec-2022").add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["whois_db"])

        epoch = str(
            int(PyFunceble.mktime(PyFunceble.strptime("25-dec-2007", "%d-%b-%Y")))
        )
        expected = {
            "single_testing": {
                "microsoft.google.com": {
                    "epoch": epoch,
                    "expiration_date": "25-dec-2007",
                    "state": "past",
                }
            }
        }

        Whois("25-dec-2007").add()
        self.assertEqual(expected, PyFunceble.CONFIGURATION["whois_db"])

        del PyFunceble.CONFIGURATION["to_test"]
        del PyFunceble.CONFIGURATION["whois_db"]
        self.test_file_not_exist()


if __name__ == "__main__":
    launch_tests()
