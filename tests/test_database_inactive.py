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
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
# pylint: enable=line-too-long

from datetime import datetime, timedelta
from unittest import TestCase
from unittest import main as launch_tests
from unittest.mock import Mock, patch

import PyFunceble
from PyFunceble.database.inactive import InactiveDB
from time_zone import TZ


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

    @patch("datetime.datetime")
    def test_load_file_exists(self, datetime_patch):
        """
        Tests the case that we load the file.
        """

        our_value = datetime(1970, 1, 1, 1, 3, 10, 0, tzinfo=TZ("+", hours=1).get())
        datetime_patch = Mock(wraps=datetime)
        datetime_patch.now = Mock(return_value=our_value)
        datetime_patch.fromtimestamp = Mock(return_value=our_value)
        patcher = patch("PyFunceble.database.inactive.datetime", new=datetime_patch)
        patcher.start()

        # We also test the merging.
        to_write = {
            self.file_to_test: {
                "190": {"example.com": PyFunceble.STATUS.official.invalid}
            },
            "this_is_a_well_informed_ghost": {
                "example.com": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
        }

        expected = {
            self.file_to_test: {
                "example.com": {
                    "included_at_epoch": our_value.timestamp(),
                    "included_at_iso": our_value.isoformat(),
                    "last_retested_at_epoch": our_value.timestamp(),
                    "last_retested_at_iso": our_value.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
            "this_is_a_well_informed_ghost": {
                "example.com": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
        }

        PyFunceble.helpers.Dict(to_write).to_json_file(self.storage_file)

        self.inactive_db.load()

        self.assertEqual(expected, self.inactive_db.database)

        patcher.stop()

    def test_clean(self):
        """
        Tests the cleaning process
        """

        to_write = {
            self.file_to_test: {
                "example.com": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
        }

        PyFunceble.helpers.Dict(to_write).to_json_file(self.storage_file)

        self.inactive_db.load()
        self.inactive_db.parent = True
        self.inactive_db.clean()
        self.inactive_db.parent = False

        expected = {self.file_to_test: {}}

        self.assertEqual(expected, self.inactive_db.database)

    def test_get_to_retest(self):
        """
        Tests the method which is supposed to provides the list
        of subject to restest.
        """

        today = datetime.now()
        past = today - timedelta(days=100)
        to_write = {
            self.file_to_test: {
                "example.com": {
                    "included_at_epoch": today.timestamp(),
                    "included_at_iso": today.isoformat(),
                    "last_retested_at_epoch": today.timestamp(),
                    "last_retested_at_iso": today.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "example.org": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "example.net": {
                    "included_at_epoch": past.timestamp(),
                    "included_at_iso": past.isoformat(),
                    "last_retested_at_epoch": past.timestamp(),
                    "last_retested_at_iso": past.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
        }

        PyFunceble.helpers.Dict(to_write).to_json_file(self.storage_file)

        self.inactive_db.load()

        expected = {"example.org", "example.net"}

        self.assertEqual(expected, self.inactive_db.get_to_retest())

        self.inactive_db.remove("example.org")
        self.inactive_db.remove("example.net")

        expected = set()

        self.assertEqual(expected, self.inactive_db.get_to_retest())

    def test_get_already_tested(self):
        """
        Tests of the method which gives us the list of already
        tested subject.
        """

        today = datetime.now()
        past = today - timedelta(days=300)
        to_write = {
            self.file_to_test: {
                "example.com": {
                    "included_at_epoch": today.timestamp(),
                    "included_at_iso": today.isoformat(),
                    "last_retested_at_epoch": today.timestamp(),
                    "last_retested_at_iso": today.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "example.org": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "example.net": {
                    "included_at_epoch": past.timestamp(),
                    "included_at_iso": past.isoformat(),
                    "last_retested_at_epoch": past.timestamp(),
                    "last_retested_at_iso": past.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
        }

        PyFunceble.helpers.Dict(to_write).to_json_file(self.storage_file)

        self.inactive_db.load()

        expected = {"example.com", "example.org"}

        self.assertEqual(expected, self.inactive_db.get_already_tested())

        self.inactive_db.remove("example.com")
        self.inactive_db.remove("example.org")

        expected = set()

        self.assertEqual(expected, self.inactive_db.get_already_tested())

        self.inactive_db.authorized = False

        self.assertEqual(expected, self.inactive_db.get_already_tested())

    def test_get_to_clean(self):
        """
        Tests of the method which gives us the list of subject to clean.
        """

        today = datetime.now()
        past = today - timedelta(days=300)
        to_write = {
            self.file_to_test: {
                "example.com": {
                    "included_at_epoch": today.timestamp(),
                    "included_at_iso": today.isoformat(),
                    "last_retested_at_epoch": today.timestamp(),
                    "last_retested_at_iso": today.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "example.org": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "example.net": {
                    "included_at_epoch": past.timestamp(),
                    "included_at_iso": past.isoformat(),
                    "last_retested_at_epoch": past.timestamp(),
                    "last_retested_at_iso": past.isoformat(),
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
        }

        PyFunceble.helpers.Dict(to_write).to_json_file(self.storage_file)

        self.inactive_db.load()

        excepted = {"example.net", "example.org"}

        self.assertEqual(excepted, self.inactive_db.get_to_clean())

        excepted = set()
        self.inactive_db.authorized = False

        self.assertEqual(excepted, self.inactive_db.get_to_clean())

    def test_save(self):
        """
        Tests the case that we save the database.
        """

        expected = {
            self.file_to_test: {
                "example.com": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
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

    @patch("datetime.datetime")
    def test_add_tested_path_does_not_exists(self, datetime_patch):
        """
        Tests the addition method for the case that the flle
        we are testing is not indexed.
        """

        self.inactive_db.database = {}

        our_value = datetime(1970, 1, 1, 1, 0, 2, 0, tzinfo=TZ("+", hours=1).get())
        datetime_patch = Mock(wraps=datetime)
        datetime_patch.now = Mock(return_value=our_value)
        patcher = patch("PyFunceble.database.inactive.datetime", new=datetime_patch)
        patcher.start()

        subject = "hello.world"

        expected = {
            self.file_to_test: {
                subject: {
                    "included_at_epoch": our_value.timestamp(),
                    "included_at_iso": our_value.isoformat(),
                    "last_retested_at_epoch": our_value.timestamp(),
                    "last_retested_at_iso": our_value.isoformat(),
                    "status": PyFunceble.STATUS.official.down,
                }
            }
        }

        self.inactive_db.add(subject, PyFunceble.STATUS.official.down)
        self.assertEqual(expected, self.inactive_db.database)

        subject = "world.hello"

        expected[self.file_to_test][subject] = expected[self.file_to_test][
            "hello.world"
        ].copy()

        self.inactive_db.add(subject, PyFunceble.STATUS.official.down)
        self.assertEqual(expected, self.inactive_db.database)

        self.inactive_db.add(subject, PyFunceble.STATUS.official.down)
        self.assertEqual(expected, self.inactive_db.database)

        patcher.stop()

    def test_remove(self):
        """
        Tests of the deletion method.
        """

        subject = "hello.world"

        self.inactive_db.database = {
            self.file_to_test: {
                subject: {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
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
                subject: {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.invalid,
                },
            },
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
                "hello.world": {
                    "included_at_epoch": 190.0,
                    "included_at_iso": "1970-01-01T01:03:10",
                    "last_retested_at_epoch": 190.0,
                    "last_retested_at_iso": "1970-01-01T01:03:10",
                    "status": PyFunceble.STATUS.official.invalid,
                },
                "world.hello": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.down,
                },
            },
        }

        self.inactive_db.database = {
            self.file_to_test: {
                "world.hello": {
                    "included_at_epoch": 0.0,
                    "included_at_iso": "1970-01-01T01:00:00",
                    "last_retested_at_epoch": 0.0,
                    "last_retested_at_iso": "1970-01-01T01:00:00",
                    "status": PyFunceble.STATUS.official.down,
                },
            },
        }

        self.inactive_db["hello.world"] = {
            "included_at_epoch": 190.0,
            "included_at_iso": "1970-01-01T01:03:10",
            "last_retested_at_epoch": 190.0,
            "last_retested_at_iso": "1970-01-01T01:03:10",
            "status": PyFunceble.STATUS.official.invalid,
        }

        self.assertEqual(expected, self.inactive_db.database)


if __name__ == "__main__":
    launch_tests()
