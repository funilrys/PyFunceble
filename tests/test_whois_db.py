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

This submodule will test PyFunceble.whois_db.

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
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.helpers import Dict, File
from PyFunceble.whois_db import WhoisDB


class TestWhoisDB(TestCase):
    """
    Test PyFunceble.whois_db.WhoisDB
    """

    def setUp(self):
        """
        Setup everything needed for the test
        """

        PyFunceble.load_config(generate_directory_structure=False)

        self.file = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["whois_db"]
        )

        self.expected_content = {
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

        self.whois_db = WhoisDB()

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

        self.assertEqual(expected, self.whois_db.authorization())

        PyFunceble.CONFIGURATION["no_whois"] = False
        PyFunceble.CONFIGURATION["whois_database"] = False

        self.assertEqual(expected, self.whois_db.authorization())

        PyFunceble.CONFIGURATION["no_whois"] = True
        PyFunceble.CONFIGURATION["whois_database"] = True

        self.assertEqual(expected, self.whois_db.authorization())

        PyFunceble.CONFIGURATION["no_whois"] = False
        PyFunceble.CONFIGURATION["whois_database"] = True
        expected = True

        self.assertEqual(expected, self.whois_db.authorization())

    def test_load_file_not_exist(self):
        """
        Test the case that we want to load the database file that does not exist.
        """

        self.test_file_not_exist()

        self.whois_db.database = {}
        self.whois_db.load()

        expected = {}
        self.assertEqual(expected, self.whois_db.database)

        self.test_file_not_exist()

    def test_load_file_exist(self):
        """
        Test the case that we want to load the database file that exist.
        """

        self.test_file_not_exist()

        Dict(self.expected_content).to_json(self.file)
        self.whois_db.load()

        self.assertEqual(self.expected_content, self.whois_db.database)

        self.test_file_not_exist()

    def test_save(self):
        """
        Test the saving of the database.
        """

        self.test_file_not_exist()

        self.whois_db.database = self.expected_content
        self.whois_db.save()

        expected = True
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        self.whois_db.database = {}
        self.whois_db.load()

        self.assertEqual(self.expected_content, self.whois_db.database)

        self.test_file_not_exist()

    def test_is_in_database(self):
        """
        Test the check.
        """

        self.test_file_not_exist()

        self.whois_db.database = self.expected_content

        expected = True
        actual = "google.com" in self.whois_db

        self.assertEqual(expected, actual)

        expected = False
        actual = "hello.google.com" in self.whois_db

        self.assertEqual(expected, actual)

        self.test_file_not_exist()

    def test_is_time_older(self):
        """
        Test if a time is older or not than the current date.
        """

        self.test_file_not_exist()

        self.whois_db.database = self.expected_content

        self.whois_db.database["google.com"]["epoch"] = PyFunceble.time() - (
            15 * (60 * 60 * 24)
        )

        expected = True
        actual = self.whois_db.is_time_older("google.com")

        self.assertEqual(expected, actual)

        self.whois_db.database["google.com"]["epoch"] = PyFunceble.time() + (
            15 * (60 * 60 * 24)
        )

        expected = False
        actual = self.whois_db.is_time_older("google.com")

        self.assertEqual(expected, actual)

        self.test_file_not_exist()

    def test_get_expiration_date(self):
        """
        Test the way we get the expiration date from the database.
        """

        self.test_file_not_exist()

        self.whois_db.database = self.expected_content

        expected = "14-sep-2020"
        actual = self.whois_db.get_expiration_date("google.com")

        self.assertEqual(expected, actual)

        expected = None
        actual = self.whois_db.get_expiration_date("hello.google.com")

        self.assertEqual(expected, actual)

        self.test_file_not_exist()

    def test_add(self):
        """
        Test the addition for the case that the element is not into
        the database.
        """

        self.test_file_not_exist()

        self.whois_db.database = {}

        epoch = int(PyFunceble.mktime(PyFunceble.strptime("25-dec-2022", "%d-%b-%Y")))

        expected = {
            "microsoft.google.com": {
                "epoch": epoch,
                "expiration_date": "25-dec-2022",
                "state": "future",
            }
        }

        self.whois_db.add("microsoft.google.com", "25-dec-2022")
        self.assertEqual(expected, self.whois_db.database)

        self.whois_db.database["microsoft.google.com"]["state"] = "hello"

        self.whois_db.add("microsoft.google.com", "25-dec-2022")
        self.assertEqual(expected, self.whois_db.database)

        epoch = int(PyFunceble.mktime(PyFunceble.strptime("25-dec-2007", "%d-%b-%Y")))

        expected = {
            "microsoft.google.com": {
                "epoch": epoch,
                "expiration_date": "25-dec-2007",
                "state": "past",
            }
        }

        self.whois_db.add("microsoft.google.com", "25-dec-2007")
        self.assertEqual(expected, self.whois_db.database)

        self.test_file_not_exist()


if __name__ == "__main__":
    launch_tests()
