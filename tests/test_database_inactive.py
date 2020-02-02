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

Tests of PyFunceble.database.inactive

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
from time import sleep
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.database.inactive import InactiveDB


class TestInactiveDB(TestCase):
    """
    Tests of PyFunceble.database.inactive
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        PyFunceble.load_config(
            generate_directory_structure=False, custom={"db_type": "json"}
        )

        self.file_to_test = "this_is_a_ghost"
        self.storage_file = (
            PyFunceble.CONFIG_DIRECTORY + PyFunceble.OUTPUTS.default_files.inactive_db
        )

        self.time_past = str(int((datetime.now() - timedelta(days=365)).timestamp()))
        self.time_future = str(int((datetime.now() + timedelta(days=365)).timestamp()))

        self.inactive_db = InactiveDB(self.file_to_test, parent_process=True)

        PyFunceble.helpers.File(self.storage_file).delete()

    def tearDown(self):
        """
        Setups everything needed after a test.
        """

        PyFunceble.helpers.File(self.storage_file).delete()

    def test_load_file_does_not_exists(self):
        """
        Tests the case that we load the file but it does not exists.
        """

        self.inactive_db.load()
        expected = {self.file_to_test: {}}

        self.assertEqual(expected, self.inactive_db.database)

    def test_load_file_exists(self):
        """
        Tests the case that we load the file.
        """

        # We also test the merging.
        self.inactive_db.database = {
            self.file_to_test: {
                "to_test": {"google.com": PyFunceble.STATUS.official.invalid}
            },
            "this_is_another_ghost": {
                "190": {"||google.com^": PyFunceble.STATUS.official.invalid}
            },
        }

        expected = {
            self.file_to_test: {
                "0": {
                    "mÿethèrwallét.com": PyFunceble.STATUS.official.invalid,
                    "||google.com^": PyFunceble.STATUS.official.invalid,
                }
            },
            "this_is_another_ghost": {
                "0": {"||google.com^": PyFunceble.STATUS.official.invalid},
                "190": {"||google.com^": PyFunceble.STATUS.official.invalid},
            },
            "this_is_a_hidden_ghost": {
                "200": {"200.com": PyFunceble.STATUS.official.invalid}
            },
        }

        PyFunceble.helpers.Dict(expected.copy()).to_json_file(self.storage_file)
        expected[self.file_to_test][
            str(
                int(
                    (
                        datetime.now() - timedelta(days=1) - timedelta(seconds=100)
                    ).timestamp()
                )
            )
        ] = {"google.com": PyFunceble.STATUS.official.invalid}

        self.inactive_db.load()

        self.assertEqual(expected, self.inactive_db.database)

    def test_save(self):
        """
        Tests teh case that we save the database.
        """

        expected = {
            self.file_to_test: {
                "0": {
                    "mÿethèrwallét.com": PyFunceble.STATUS.official.invalid,
                    "||google.com^": PyFunceble.STATUS.official.invalid,
                }
            }
        }

        self.inactive_db.database = expected.copy()
        self.inactive_db.save()

        self.assertEqual(
            expected, PyFunceble.helpers.Dict().from_json_file(self.storage_file)
        )

    def test_initiate_tested_path_does_not_exists(self):
        """
        Tests the initiate method for the case that the file
        we are testing is not indexed.
        """

        expected = {self.file_to_test: {}}

        self.inactive_db.database = {}
        self.inactive_db.initiate()

        self.assertEqual(expected, self.inactive_db.database)

    def test_add_tested_path_does_not_exists(self):
        """
        Tests the addition method for the case that teh flle
        we are testing is not indexed.
        """

        self.inactive_db.database = {}

        subject = "hello.world"

        expected = {
            self.file_to_test: {
                str(int(datetime.now().timestamp())): {
                    subject: PyFunceble.STATUS.official.down
                }
            }
        }

        self.inactive_db.add(subject, PyFunceble.STATUS.official.down)
        self.assertEqual(expected, self.inactive_db.database)

        subject = "world.hello"

        sleep(2)

        expected[self.file_to_test][str(int(datetime.now().timestamp()))] = {
            subject: PyFunceble.STATUS.official.down
        }

        self.inactive_db.add(subject, PyFunceble.STATUS.official.down)
        self.assertEqual(expected, self.inactive_db.database)

    def test_remove(self):
        """
        Tests of the deletion method.
        """

        subject = "hello.world"

        self.inactive_db.database = {
            self.file_to_test: {
                str(int(datetime.now().timestamp())): {
                    subject: PyFunceble.STATUS.official.down
                }
            }
        }

        expected = {self.file_to_test: {}}

        self.inactive_db.remove(subject)
        self.assertEqual(expected, self.inactive_db.database)

    def test_is_present(self):
        """
        Tests the presence checker method.
        """

        subject = "hello.world"

        self.inactive_db.database = {
            self.file_to_test: {
                str(int(datetime.now().timestamp())): {
                    subject: PyFunceble.STATUS.official.down
                }
            }
        }

        expected = True
        actual = subject in self.inactive_db

        self.assertEqual(expected, actual)

        expected = False
        actual = "world.hello" in self.inactive_db

        self.assertEqual(expected, actual)

    def test_set_item_from_outside(self):
        """
        Tests the case that we adds items from outside the class.
        """

        expected = {
            self.file_to_test: {
                str(int(datetime.now().timestamp())): {
                    "hello.world": PyFunceble.STATUS.official.down,
                    "world.hello": PyFunceble.STATUS.official.down,
                }
            }
        }

        self.inactive_db.database = {
            self.file_to_test: {
                str(int(datetime.now().timestamp())): {
                    "world.hello": PyFunceble.STATUS.official.down
                }
            }
        }

        self.inactive_db[str(int(datetime.now().timestamp()))] = {
            "hello.world": PyFunceble.STATUS.official.down
        }

        self.assertEqual(expected, self.inactive_db.database)


if __name__ == "__main__":
    launch_tests()
