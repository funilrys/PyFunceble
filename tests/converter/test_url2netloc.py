"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of URL 2 Network Location converter.

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

from PyFunceble.converter.url2netloc import Url2Netloc


class TestUrl2Netloc(unittest.TestCase):
    """
    Tests our internal URL converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = Url2Netloc()

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

    def test_set_data_to_convert_empty_string(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that an empty-string value is given.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.converter.set_data_to_convert(given))

    def test_get_converted_nothing_to_decode(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that no conversion is needed.
        """

        given = "example.org"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_full_url(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that a full URL is given.
        """

        given = "https://example.org/hello/world/this/is/a/test"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_full_url_with_port(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that a full URL (with explicit port) is given.
        """

        given = "https://example.org:8080/hello/world/this/is/a/test"
        expected = "example.org:8080"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_full_url_with_params(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that a full URL (with params) is given.
        """

        given = "https://example.org/?is_admin=true"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_without_scheme(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that no scheme is given.
        """

        given = "example.org/hello/world/this/is/a/test"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_without_scheme_and_with_params(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that no scheme (but with params) is given.
        """

        given = "example.org/?is_admin=true"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_without_protocol(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that no protocol is given.
        """

        given = "://example.org/hello/world/this/is/a/test"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_without_protocol_and_with_params(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that no protocol (but params) is given.
        """

        given = "://example.org/?is_admin=true"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_without_protocol_and_path(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that no protocol and path is given.
        """

        given = "://example.org/"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_startswith_2_slashes(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that the given url starts with 2 slashes.
        """

        given = "//example.org/hello/world/this/is/a/test"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_url_startswith_1_slash(self) -> None:
        """
        Tests the method which let us extracts the netloc from a given URL for
        the case that the given url starts with 1 slash.
        """

        given = "/example.org/hello/world/this/is/a/test"
        expected = ""

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
