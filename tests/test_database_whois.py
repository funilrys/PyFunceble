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

Tests of PyFunceble.database.inactive.

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

from datetime import datetime, timedelta
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.database.whois import WhoisDB


class TestWhoisDB(TestCase):
    """
    Tests of PyFunceble.database.inactive.
    """

    def setUp(self):
        """
        Setups everything needed for the test.
        """

        PyFunceble.load_config(
            generate_directory_structure=False, custom={"db_type": "json"}
        )

        self.storage_file = (
            PyFunceble.CONFIG_DIRECTORY + PyFunceble.OUTPUTS.default_files.whois_db
        )

        self.whois_db = WhoisDB(parent_process=True)

        self.our_dataset = {
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

        PyFunceble.helpers.File(self.storage_file).delete()

    def tearDown(self):
        """
        Setups everything needed after a test.
        """

        PyFunceble.helpers.File(self.storage_file).delete()
        del self.whois_db

    def test_load_file_does_not_exists(self):
        """
        Tests the case that we load the file but it does not exists.
        """

        self.whois_db.load()
        expected = {}

        self.assertEqual(expected, self.whois_db.database)

    def test_load_file_exists(self):
        """
        Tests the case that we load the file.
        """

        expected = self.our_dataset.copy()

        PyFunceble.helpers.Dict(self.our_dataset.copy()).to_json_file(self.storage_file)

        self.whois_db.load()

        self.assertEqual(expected, self.whois_db.database)

    def test_authorization(self):
        """
        Tests of the authorization method.
        """

        PyFunceble.CONFIGURATION.no_whois = True
        PyFunceble.CONFIGURATION.whois_database = False
        expected = False

        self.assertEqual(expected, self.whois_db.authorization())

        PyFunceble.CONFIGURATION.no_whois = False
        PyFunceble.CONFIGURATION.whois_database = False

        self.assertEqual(expected, self.whois_db.authorization())

        PyFunceble.CONFIGURATION.no_whois = True
        PyFunceble.CONFIGURATION.whois_database = True

        self.assertEqual(expected, self.whois_db.authorization())

        PyFunceble.CONFIGURATION.no_whois = False
        PyFunceble.CONFIGURATION.whois_database = True
        expected = True

        self.assertEqual(expected, self.whois_db.authorization())

    def test_save(self):
        """
        Tests the saving saving method.
        """

        self.whois_db.database = self.our_dataset.copy()
        self.whois_db.save()

        expected = True
        actual = PyFunceble.helpers.File(self.storage_file).exists()

        self.assertEqual(expected, actual)

        expected = self.our_dataset.copy()
        actual = PyFunceble.helpers.Dict().from_json_file(self.storage_file)

        self.assertEqual(expected, actual)

    def test_is_present(self):
        """
        Tests the presence of a subject into the database.
        """

        self.whois_db.database = self.our_dataset.copy()

        expected = True
        actual = "google.com" in self.whois_db

        self.assertEqual(expected, actual)

        expected = False
        actual = "hello.google.com" in self.whois_db

        self.assertEqual(expected, actual)

    def test_is_time_older(self):
        """
        Tests of the method which checks if a given epoch/time
        is older.
        """

        self.whois_db.database = self.our_dataset.copy()

        self.whois_db.database["google.com"]["epoch"] = (
            datetime.now() - timedelta(days=15)
        ).timestamp()

        expected = True
        actual = self.whois_db.is_time_older("google.com")

        self.assertEqual(expected, actual)

        self.whois_db.database["google.com"]["epoch"] = (
            datetime.now() + timedelta(days=15)
        ).timestamp()

        expected = False
        actual = self.whois_db.is_time_older("google.com")

        self.assertEqual(expected, actual)

    def test_get_expiration_date(self):
        """
        Tests the method which is used to get the expiration date
        of a subject in the database.
        """

        self.whois_db.database = self.our_dataset.copy()

        expected = "14-sep-2020"
        actual = self.whois_db.get_expiration_date("google.com")

        self.assertEqual(expected, actual)

        expected = None
        actual = self.whois_db.get_expiration_date("hello.google.com")

        self.assertEqual(expected, actual)

    def test_add(self):
        """
        Tests of the addition method.
        """

        self.whois_db.database = {}

        epoch = datetime.strptime("25-dec-2022", "%d-%b-%Y").timestamp()

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

        epoch = datetime.strptime("25-dec-2007", "%d-%b-%Y").timestamp()

        expected = {
            "microsoft.google.com": {
                "epoch": epoch,
                "expiration_date": "25-dec-2007",
                "state": "past",
            }
        }

        self.whois_db.add("microsoft.google.com", "25-dec-2007")

        self.assertEqual(expected, self.whois_db.database)


if __name__ == "__main__":
    launch_tests()
