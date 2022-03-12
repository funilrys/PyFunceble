"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our checker WHOIS utilities.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/latest/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

import unittest

from PyFunceble.checker.utils import whois
from PyFunceble.config.loader import ConfigLoader
from PyFunceble.dataset.whois.csv import CSVWhoisDataset
from PyFunceble.dataset.whois.mariadb import MariaDBWhoisDataset
from PyFunceble.dataset.whois.mysql import MySQLWhoisDataset

# pylint: disable=unnecessary-lambda


class TestCheckerWhoisUtils(unittest.TestCase):
    """
    Tests of the WHOIS utilities.
    """

    def setUp(self) -> None:
        """
        Setup everything needed for the tests.
        """

        self.config_loader = ConfigLoader()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.config_loader

    def test_get_whois_dataset_obj_no_config(self) -> None:
        """
        Tests of the function which let us get a new WHOIS dataset object.
        """

        self.assertRaises(RuntimeError, lambda: whois.get_whois_dataset_object())

    def test_get_whois_dataset_obj_csv(self) -> None:
        """
        Tests of the function which let us get a new WHOIS dataset object.

        In this case, we check the case that the CSV was declared.
        """

        self.config_loader.set_custom_config(
            {"cli_testing": {"db_type": "csv"}}
        ).start()

        expected = CSVWhoisDataset
        actual = whois.get_whois_dataset_object()

        self.assertIsInstance(actual, expected)

    def test_get_whois_dataset_obj_mariadb(self) -> None:
        """
        Tests of the function which let us get a new WHOIS dataset object.

        In this case, we check the case that the MariaDb was declared.
        """

        self.config_loader.set_custom_config(
            {"cli_testing": {"db_type": "mariadb"}}
        ).start()

        expected = MariaDBWhoisDataset
        actual = whois.get_whois_dataset_object()

        self.assertIsInstance(actual, expected)

    def test_get_whois_dataset_obj_mysql(self) -> None:
        """
        Tests of the function which let us get a new WHOIS dataset object.

        In this case, we check the case that the MySQL was declared.
        """

        self.config_loader.set_custom_config(
            {"cli_testing": {"db_type": "mysql"}}
        ).start()

        expected = MySQLWhoisDataset
        actual = whois.get_whois_dataset_object()

        self.assertIsInstance(actual, expected)

    def test_get_whois_dataset_obj_unknown(self) -> None:
        """
        Tests of the function which let us get a new WHOIS dataset object.

        In this case, we check the case that an unknown db type was declared.
        """

        self.config_loader.set_custom_config(
            {"cli_testing": {"db_type": "hello"}}
        ).start()

        self.assertRaises(ValueError, lambda: whois.get_whois_dataset_object())


if __name__ == "__main__":
    unittest.main()
