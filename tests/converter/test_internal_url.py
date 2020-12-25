"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our internal URL converter.

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

import unittest
import unittest.mock

import PyFunceble.storage
from PyFunceble.converter.internal_url import InternalUrlConverter


class TestInternalUrlConverter(unittest.TestCase):
    """
    Tests our internal URL converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = InternalUrlConverter()

    def tearDown(self) -> None:
        """
        Destroys everything previously created for the tests.
        """

        del self.converter

    def test_set_data_to_convert_no_string(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that a non-string value is given.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_data_to_convert(given))

    def test_get_converted_nothing_to_decode(self) -> None:
        """
        Tests the method which let us convert our internal url for the case that
        no conversion is needed..
        """

        original_version = PyFunceble.storage.PROJECT_VERSION
        PyFunceble.storage.PROJECT_VERSION = "1.0.0.dev (Hello, World)"

        given = "https://raw.githubusercontent.com/funilrys/hello_world/dev/test.json"
        expected = (
            "https://raw.githubusercontent.com/funilrys/hello_world/dev/test.json"
        )

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

        PyFunceble.storage.PROJECT_VERSION = original_version

    def test_get_converted_dev_to_master(self) -> None:
        """
        Tests the method which let us convert our internal url for the case that
        we want to get the master version of the url.
        """

        original_version = PyFunceble.storage.PROJECT_VERSION
        PyFunceble.storage.PROJECT_VERSION = "1.0.0. (Hello, World)"

        given = "https://raw.githubusercontent.com/funilrys/hello_world/dev/test.json"
        expected = (
            "https://raw.githubusercontent.com/funilrys/hello_world/master/test.json"
        )

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

        PyFunceble.storage.PROJECT_VERSION = original_version

    def test_get_converted_master_to_dev(self) -> None:
        """
        Tests the method which let us convert our internal url for the case that
        we want to get the dev version of the url.
        """

        original_version = PyFunceble.storage.PROJECT_VERSION
        PyFunceble.storage.PROJECT_VERSION = "1.0.0.dev (Hello, World)"

        given = (
            "https://raw.githubusercontent.com/funilrys/hello_world/master/test.json"
        )
        expected = (
            "https://raw.githubusercontent.com/funilrys/hello_world/dev/test.json"
        )

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

        PyFunceble.storage.PROJECT_VERSION = original_version


if __name__ == "__main__":
    unittest.main()
