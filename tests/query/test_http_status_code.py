"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the HTTP status code query tool.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023 Nissar Chababy

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

import requests
import requests.models

import PyFunceble.factory
from PyFunceble.config.loader import ConfigLoader
from PyFunceble.query.http_status_code import HTTPStatusCode


class TestHTTPStatusCode(unittest.TestCase):
    """
    Tests the HTTP status code query tool.
    """

    def setUp(self) -> None:
        """
        Sets everything needed by the tests.
        """

        self.query_tool = HTTPStatusCode()

        return super().setUp()

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.query_tool

    def test_set_subject_return(self) -> None:
        """
        Tests the response from the method which let us set the subject
        to work with.
        """

        given = "example.org"

        actual = self.query_tool.set_subject(given)

        self.assertIsInstance(actual, HTTPStatusCode)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "example.org"
        expected = "example.org"

        self.query_tool.set_subject(given)

        actual = self.query_tool.subject

        self.assertEqual(expected, actual)

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
        Tests the overwritting of the subject to work through the class
        constructor.
        """

        given = "example.org"
        expected = "example.org"

        query_tool = HTTPStatusCode(subject=given)
        actual = query_tool.subject

        self.assertEqual(expected, actual)

    def test_set_subject_not_str(self) -> None:
        """
        Tests the method which let us set the subject to work with for the case
        that the given subject is not a :py:class:`str`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_subject(given))

    def test_set_subject_empty_str(self) -> None:
        """
        Tests the method which let us set the subject to work with for the case
        that the given subject is an empty :py:class:`str`.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.query_tool.set_subject(given))

    def test_set_timeout_return(self) -> None:
        """
        Tests the response from the method which let us set the timeout
        to work with.
        """

        given = 15.0

        actual = self.query_tool.set_timeout(given)

        self.assertIsInstance(actual, HTTPStatusCode)

    def test_set_timeout_method(self) -> None:
        """
        Tests the method which let us set the timeout to work with.
        """

        given = 15.0
        expected = 15.0

        self.query_tool.set_timeout(given)

        actual = self.query_tool.timeout

        self.assertEqual(expected, actual)

    def test_set_timeout_attribute(self) -> None:
        """
        Tests overwritting of the :code:`timeout` attribute.
        """

        given = 15.0
        expected = 15.0

        self.query_tool.timeout = given
        actual = self.query_tool.timeout

        self.assertEqual(expected, actual)

    def test_set_timeout_through_init(self) -> None:
        """
        Tests the overwritting of the timeout to work through the class
        constructor.
        """

        given = 15.0
        expected = 15.0

        query_tool = HTTPStatusCode(timeout=given)
        actual = query_tool.timeout

        self.assertEqual(expected, actual)

    def test_set_timeout_not_int_nor_float(self) -> None:
        """
        Tests the method which let us set the timeout to work with for the case
        that the given timeout is not a :py:class:`int`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_timeout(given))

    def test_set_timeout_lower_than_1(self) -> None:
        """
        Tests the method which let us set the timeout to work with for the case
        that the given timeout is less than 1.
        """

        given = 0.5
        expected = 0.5

        query_tool = HTTPStatusCode(timeout=given)
        actual = query_tool.timeout

        self.assertEqual(expected, actual)

    def test_set_timeout_equal_0(self) -> None:
        """
        Tests the method which let us set the timeout to work with for the case
        that the given timeout is equal to 0.
        """

        given = 0
        expected = 0.0

        query_tool = HTTPStatusCode(timeout=given)
        actual = query_tool.timeout

        self.assertEqual(expected, actual)

    def test_set_timeout_lower_0(self) -> None:
        """
        Tests the method which let us set the timeout to work with for the case
        that the given timeout is lower then 0.
        """

        given = -3

        self.assertRaises(ValueError, lambda: self.query_tool.set_timeout(given))

    def test_guess_and_set_timeout(self) -> None:
        """
        Tests the method which let us guess and set the timeout from the
        configuration file.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"lookup": {"timeout": 15.0}}).start()

        self.query_tool.guess_and_set_timeout()

        expected = 15.0
        actual = self.query_tool.timeout

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_timeout_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the timeout from the
        configuration file.
        """

        self.query_tool.guess_and_set_timeout()

        expected = self.query_tool.STD_TIMEOUT
        actual = self.query_tool.timeout

        self.assertEqual(expected, actual)

    def test_set_verify_certificate_return(self) -> None:
        """
        Tests the response from the method which let us activate or disable
        the certificate verification.
        """

        given = True

        actual = self.query_tool.set_verify_certificate(given)

        self.assertIsInstance(actual, HTTPStatusCode)

    def test_set_verify_certificate_method(self) -> None:
        """
        Tests the method which let us activate or disable the certificate
        verification.
        """

        given = True
        expected = True

        self.query_tool.set_verify_certificate(given)

        actual = self.query_tool.verify_certificate

        self.assertEqual(expected, actual)

    def test_set_verify_certificate_attribute(self) -> None:
        """
        Tests overwritting of the :code:`verify_certificate` attribute.
        """

        given = True
        expected = True

        self.query_tool.verify_certificate = given
        actual = self.query_tool.verify_certificate

        self.assertEqual(expected, actual)

    def test_set_verify_certificate_through_init(self) -> None:
        """
        Tests the overwritting of the value of the certificate validation
        through the class constructor.
        """

        given = True
        expected = True

        query_tool = HTTPStatusCode(verify_certificate=given)
        actual = query_tool.verify_certificate

        self.assertEqual(expected, actual)

    def test_set_verify_certificate_not_bool(self) -> None:
        """
        Tests the method which let us activate or disable the certificate
        validation for the case that the given value is not a :py:class`bool`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: self.query_tool.set_verify_certificate(given)
        )

    def test_guess_and_set_verify_certificate(self) -> None:
        """
        Tests the method which let us guess and set the certificate verification
        attribute from the configuration file.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"verify_ssl_certificate": True}).start()

        self.query_tool.guess_and_set_verify_certificate()

        expected = True
        actual = self.query_tool.verify_certificate

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_certificate_verification_config_not_loaded(self) -> None:
        """
        Tests the method which let us guess and set the certificate
        verification from the configuration file.
        """

        self.query_tool.guess_and_set_verify_certificate()

        expected = self.query_tool.STD_VERIFY_CERTIFICATE
        actual = self.query_tool.verify_certificate

        self.assertEqual(expected, actual)

    def test_set_allow_redirects_return(self) -> None:
        """
        Tests the response from the method which let us allow the redirection.
        """

        given = True

        actual = self.query_tool.set_allow_redirects(given)

        self.assertIsInstance(actual, HTTPStatusCode)

    def test_set_allow_redirects_method(self) -> None:
        """
        Tests the method which let us allow the redirection.
        """

        given = True
        expected = True

        self.query_tool.set_allow_redirects(given)

        actual = self.query_tool.allow_redirects

        self.assertEqual(expected, actual)

    def test_set_allow_redirects_not_bool(self) -> None:
        """
        Tests the method which let us allow the redirection for the case that
        the given value is not a boolean.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_allow_redirects(given))

    def test_set_allow_redirects_attribute(self) -> None:
        """
        Tests overwritting of the :code:`allow_redirects` attribute.
        """

        given = True
        expected = True

        self.query_tool.allow_redirects = given
        actual = self.query_tool.allow_redirects

        self.assertEqual(expected, actual)

    def test_set_allow_redirects_through_init(self) -> None:
        """
        Tests the overwritting of the attribute which let us allow the
        redirection.
        """

        given = True
        expected = True

        query_tool = HTTPStatusCode(allow_redirects=given)
        actual = query_tool.allow_redirects

        self.assertEqual(expected, actual)

    def test_get_status_code_no_subject(self) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that no subject is actually given.
        """

        # pylint: disable=unnecessary-lambda
        self.assertRaises(TypeError, lambda: self.query_tool.get_status_code())

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code(self, request_mock) -> None:
        """
        Tests the method which let us get the status code of the given subject.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = "I'm a teapot."

            response = requests.models.Response()
            response.url = "https://example.org"
            response.status_code = 418

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.subject = "https://example.org"

        request_mock.side_effect = mocking

        expected = 418
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_error(self, request_mock) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that an error happened during the request.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            raise PyFunceble.factory.Requester.exceptions.ConnectionError(
                "I'm a teapot."
            )

        self.query_tool.subject = "https://example.org"

        request_mock.side_effect = mocking

        expected = self.query_tool.STD_UNKNOWN_STATUS_CODE
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_too_many_redirects(self, request_mock) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that too many redirects happened during the request.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            raise PyFunceble.factory.Requester.exceptions.TooManyRedirects(
                "Exceeded 30 redirects."
            )

        self.query_tool.subject = "https://example.org"

        request_mock.side_effect = mocking

        expected = self.query_tool.STD_UNKNOWN_STATUS_CODE
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_http_to_https(self, request_mock) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that a redirection from HTTP to HTTPS is done.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            first_response = requests.models.Response()
            first_response.headers = {"Location": "https://example.org"}
            first_response.url = "http://example.org"
            first_response.status_code = 302

            final_response = requests.models.Response()
            final_response.url = "https://example.org"
            final_response.status_code = 200

            # pylint: disable=protected-access
            final_response._content = "Hello, World!".encode("utf-8")

            final_response.history = [first_response]

            return final_response

        self.query_tool.subject = "http://example.org"

        request_mock.side_effect = mocking

        expected = 200
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_http_to_https_different_subject(
        self, request_mock
    ) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that a redirection from HTTP to HTTPS is done but the
        subject of the HTTPS query is different from the original one.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            first_response = requests.models.Response()
            first_response.headers = {"Location": "https://test.example.org"}
            first_response.url = "http://example.org"
            first_response.status_code = 302

            final_response = requests.models.Response()
            final_response.url = "https://test.example.org"
            final_response.status_code = 200

            # pylint: disable=protected-access
            final_response._content = "Hello, World!".encode("utf-8")

            final_response.history = [first_response]

            return final_response

        self.query_tool.subject = "http://example.org"

        request_mock.side_effect = mocking

        expected = 302
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_http_to_https_different_subject_allow_redirects(
        self, request_mock
    ) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that a redirection from HTTP to HTTPS is done but the
        subject of the HTTPS query is different from the original one.

        In this case, we forces the interface to follow the redirect. Meaning
        that the status code of the final one should be always returned.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            first_response = requests.models.Response()
            first_response.headers = {"Location": "https://test.example.org"}
            first_response.url = "http://example.org"
            first_response.status_code = 302

            final_response = requests.models.Response()
            final_response.url = "https://test.example.org"
            final_response.status_code = 200

            # pylint: disable=protected-access
            final_response._content = "Hello, World!".encode("utf-8")

            final_response.history = [first_response]

            return final_response

        self.query_tool.allow_redirects = True
        self.query_tool.subject = "http://example.org"

        request_mock.side_effect = mocking

        expected = 200
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_http_to_https_multiple_jump(self, request_mock) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that a redirection from HTTP to HTTPS is done but other
        redirect came along the route.

        In this case, only the first one (in the row) should be provided.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            first_response = requests.models.Response()
            first_response.headers = {"Location": "https://test.example.org"}
            first_response.url = "http://example.org"
            first_response.status_code = 301

            second_response = requests.models.Response()
            second_response.headers = {"Location": "https://test2.example.org"}
            second_response.url = "https://test.example.org"
            second_response.status_code = 302

            third_response = requests.models.Response()
            third_response.headers = {"Location": "https://example.org"}
            third_response.url = "https://test2.example.org"
            third_response.status_code = 302

            final_response = requests.models.Response()
            final_response.url = "https://test.example.org"
            final_response.status_code = 200

            # pylint: disable=protected-access
            final_response._content = "Hello, World!".encode("utf-8")

            final_response.history = [first_response, second_response, third_response]

            return final_response

        self.query_tool.subject = "http://example.org"

        request_mock.side_effect = mocking

        expected = 301
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(PyFunceble.factory.Requester, "get")
    def test_get_status_code_http_to_https_multiple_jump_allow_redirects(
        self, request_mock
    ) -> None:
        """
        Tests the method which let us get the status code of the given subject
        for the case that a redirection from HTTP to HTTPS is done but other
        redirect came along the route.

        In this case we force the interface to follow the redirect. Meaning that
        the final status code should be provided.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            first_response = requests.models.Response()
            first_response.headers = {"Location": "https://test.example.org"}
            first_response.url = "http://example.org"
            first_response.status_code = 301

            second_response = requests.models.Response()
            second_response.headers = {"Location": "https://test2.example.org"}
            second_response.url = "https://test.example.org"
            second_response.status_code = 302

            third_response = requests.models.Response()
            third_response.headers = {"Location": "https://example.org"}
            third_response.url = "https://test2.example.org"
            third_response.status_code = 302

            final_response = requests.models.Response()
            final_response.url = "https://test.example.org"
            final_response.status_code = 200

            # pylint: disable=protected-access
            final_response._content = "Hello, World!".encode("utf-8")

            final_response.history = [first_response, second_response, third_response]

            return final_response

        self.query_tool.allow_redirects = True
        self.query_tool.subject = "http://example.org"

        request_mock.side_effect = mocking

        expected = 200
        actual = self.query_tool.get_status_code()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
