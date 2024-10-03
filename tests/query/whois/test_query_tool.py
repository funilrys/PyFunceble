"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests our WHOIS query tool.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# pylint: disable=protected-access

import unittest
import unittest.mock

from PyFunceble.query.record.whois import WhoisQueryToolRecord
from PyFunceble.query.whois.query_tool import WhoisQueryTool


class TestWhoisQueryTool(unittest.TestCase):
    """
    Tests of our WHOIS record query tool.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.query_tool = WhoisQueryTool()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.query_tool

    def test_set_subject_return(self) -> None:
        """
        Tests the response from the method which let us set the subject to work
        with.
        """

        given = "example.org"

        actual = self.query_tool.set_subject(given)

        self.assertIsInstance(actual, WhoisQueryTool)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "example.org"
        expected = "example.org"

        self.query_tool.set_subject(given)

        actual = self.query_tool.subject

        self.assertEqual(expected, actual)

    def test_set_subject_not_str(self) -> None:
        """
        Tests the method which let us set the subject to work with; For the
        case that the given subject is not a :py:class:`str`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_subject(given))

    def test_set_subject_empty_str(self) -> None:
        """
        Tests the method which let us set the subject to work with; For the
        case that the given subject is an empty :py:class:`str`.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.query_tool.set_subject(given))

    def test_set_subject_attribute(self) -> None:
        """
        Tests overwritting of the :code:`subject` attribute.
        """

        given = "example.org"
        expected = "example.org"

        self.query_tool.subject = given
        actual = self.query_tool.subject

        self.assertEqual(expected, actual)

    def test_set_subject_through_init(self) -> None:
        """
        Tests the overwritting of the subject to work through the class constructor.
        """

        given = "example.org"
        expected = "example.org"

        query_tool = WhoisQueryTool(subject=given)
        actual = query_tool.subject

        self.assertEqual(expected, actual)

    def test_set_server_return(self) -> None:
        """
        Tests the response from the method which let us set the server to work
        with.
        """

        given = "whois.example.org"

        actual = self.query_tool.set_server(given)

        self.assertIsInstance(actual, WhoisQueryTool)

    def test_set_server_method(self) -> None:
        """
        Tests the method which let us set the server to work with.
        """

        given = "whois.example.org"
        expected = "whois.example.org"

        self.query_tool.set_server(given)

        actual = self.query_tool.server

        self.assertEqual(expected, actual)

    def test_set_server_not_str(self) -> None:
        """
        Tests the method which let us set the server to work with; For the
        case that the given server is not a :py:class:`str`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_server(given))

    def test_set_server_empty_str(self) -> None:
        """
        Tests the method which let us set the server to work with; For the
        case that the given server is an empty :py:class:`str`.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.query_tool.set_server(given))

    def test_set_server_attribute(self) -> None:
        """
        Tests overwritting of the :code:`server` attribute.
        """

        given = "whois.example.org"
        expected = "whois.example.org"

        self.query_tool.server = given
        actual = self.query_tool.server

        self.assertEqual(expected, actual)

    def test_set_server_through_init(self) -> None:
        """
        Tests the overwritting of the server to work through the class constructor.
        """

        given = "whois.example.org"
        expected = "whois.example.org"

        query_tool = WhoisQueryTool(server=given)
        actual = query_tool.server

        self.assertEqual(expected, actual)

    def test_set_query_timeout_return(self) -> None:
        """
        Tests the response from the method which let us set the timeout to apply.
        """

        given = 100

        actual = self.query_tool.set_query_timeout(given)

        self.assertIsInstance(actual, WhoisQueryTool)

    def test_set_query_timeout_method(self) -> None:
        """
        Tests the method which let us set the query timeout to apply.
        """

        given = 1000
        expected = 1000.0

        self.query_tool.set_query_timeout(given)

        actual = self.query_tool.query_timeout

        self.assertEqual(expected, actual)

    def test_set_query_timeout_not_int_nor_float(self) -> None:
        """
        Tests the method which let us set the query timeout to apply; For
        the case that the given timeout is not a :py:class:`int` nor
        :py:class:`float`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_query_timeout(given))

    def test_set_query_timeout_empty_str(self) -> None:
        """
        Tests the method which let us set the query timeout to apply; For the
        case that the given timeout is less than 1.
        """

        given = -4

        self.assertRaises(ValueError, lambda: self.query_tool.set_query_timeout(given))

    def test_set_query_timeout_attribute(self) -> None:
        """
        Tests overwritting of the :code:`query_timeout` attribute.
        """

        given = 10000
        expected = 10000.0

        self.query_tool.query_timeout = given
        actual = self.query_tool.query_timeout

        self.assertEqual(expected, actual)

    def test_set_query_timeout_through_init(self) -> None:
        """
        Tests the overwritting of the query timeout to use through the class
        constructor.
        """

        given = 1000
        expected = 1000.0

        query_tool = WhoisQueryTool(query_timeout=given)
        actual = query_tool.query_timeout

        self.assertEqual(expected, actual)

    def test_read_expiration_date(self) -> None:
        """
        Tests the method which let us get the expiration date.
        """

        self.query_tool.query_timeout = 10000.0
        self.query_tool.server = "whois.example.org"
        self.query_tool.subject = "example.org"
        self.query_tool._expiration_date = ""

        expected = ""
        self.assertEqual(expected, self.query_tool.expiration_date)

        self.query_tool._expiration_date = "2021-01-01 00:00:00"

        expected = "2021-01-01 00:00:00"
        self.assertEqual(expected, self.query_tool.expiration_date)

        self.query_tool._expiration_date = None
        self.query_tool.lookup_record.record = "expires: 2021-01-01 00:00:00"

        expected = "01-jan-2021"
        self.assertEqual(expected, self.query_tool.expiration_date)

    def test_read_registrar(self) -> None:
        """
        Tests the method which let us get the registrar.
        """

        self.query_tool.query_timeout = 10000.0
        self.query_tool.server = "whois.example.org"
        self.query_tool.subject = "example.org"
        self.query_tool._registrar = ""

        expected = ""
        self.assertEqual(expected, self.query_tool.registrar)

        self.query_tool._registrar = "Example Registrar"

        expected = "Example Registrar"
        self.assertEqual(expected, self.query_tool.registrar)

        self.query_tool._registrar = None
        self.query_tool.lookup_record.record = "registrar: Example Registrar"

        expected = "Example Registrar"
        self.assertEqual(expected, self.query_tool.registrar)

    def test_read_record(self) -> None:
        """
        Tests the method which let us get the record.
        """

        self.query_tool.query_timeout = 10000.0
        self.query_tool.server = "whois.example.org"
        self.query_tool.subject = "example.org"
        self.query_tool.lookup_record.record = "Hello, World!"

        expected = "Hello, World!"
        self.assertEqual(expected, self.query_tool.record)

    def test_get_lookup_record(self) -> None:
        """
        Tests the method which let us get the lookup record.
        """

        self.query_tool.query_timeout = 10000.0
        self.query_tool.server = "whois.example.org"
        self.query_tool.subject = "example.org"

        self.query_tool._expiration_date = "2021-01-01 00:00:00"
        self.query_tool._registrar = "Example Registrar"

        actual = self.query_tool.get_lookup_record()

        self.assertIsInstance(actual, WhoisQueryToolRecord)

        expected = "example.org"
        self.assertEqual(expected, actual.subject)

        expected = "whois.example.org"
        self.assertEqual(expected, actual.server)

        expected = "2021-01-01 00:00:00"
        self.assertEqual(expected, actual.expiration_date)

        expected = "Example Registrar"
        self.assertEqual(expected, actual.registrar)

        expected = 10000.0
        self.assertEqual(expected, actual.query_timeout)


if __name__ == "__main__":
    unittest.main()
