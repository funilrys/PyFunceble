"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the download helper.

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


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

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

import tempfile
import unittest
import unittest.mock

import requests

import PyFunceble.helpers.exceptions
from PyFunceble.helpers.download import DownloadHelper


class TestDownloadHelper(unittest.TestCase):
    """
    Tests of the download helper.
    """

    def test_set_url_return(self) -> None:
        """
        Tests the response of the method which let us set the url to work with.
        """

        given = "https://example.org"
        download_helper = DownloadHelper()

        actual = download_helper.set_url(given)

        self.assertIsInstance(actual, DownloadHelper)

    def test_set_url(self) -> None:
        """
        Tests the method which let us set the url to work with.
        """

        given = "https://example.org"

        expected = "https://example.org"
        download_helper = DownloadHelper()

        download_helper.set_url(given)

        actual = download_helper.url

        self.assertEqual(expected, actual)

        download_helper = DownloadHelper(given)

        actual = download_helper.url

        self.assertEqual(expected, actual)

    def test_set_url_not_str(self) -> None:
        """
        Tests the method which let us set the url to work with for the case that
        the given url is not a string.
        """

        given = ["Hello", "World"]

        download_helper = DownloadHelper()

        self.assertRaises(TypeError, lambda: download_helper.set_url(given))

    def test_set_certificate_validation_return(self) -> None:
        """
        Tests the response of the method which let us authorize the certificate
        validation.
        """

        given = True
        download_helper = DownloadHelper()

        actual = download_helper.set_certificate_validation(given)

        self.assertIsInstance(actual, DownloadHelper)

    def test_set_certificate_validation(self) -> None:
        """
        Tests the method which let us authorize the certificate validation.
        """

        given = True

        expected = True
        download_helper = DownloadHelper()

        download_helper.set_certificate_validation(given)

        actual = download_helper.certificate_validation

        self.assertEqual(expected, actual)

        download_helper = DownloadHelper(certificate_validation=given)

        actual = download_helper.certificate_validation

        self.assertEqual(expected, actual)

    def test_set_certificate_validation_not_bool(self) -> None:
        """
        Tests the method which let us authorize the certificate validation for
        the case that the given value is not a boolean.
        """

        given = ["Hello", "World"]

        download_helper = DownloadHelper()

        self.assertRaises(
            TypeError, lambda: download_helper.set_certificate_validation(given)
        )

    def test_set_retries_return(self) -> None:
        """
        Tests the response of the method which let us set the number of retry
        to perform.
        """

        given = 3
        download_helper = DownloadHelper()

        actual = download_helper.set_retries(given)

        self.assertIsInstance(actual, DownloadHelper)

    def test_set_retries(self) -> None:
        """
        Tests the method which let us set the number of retry to perform.
        """

        given = 3

        expected = 3
        download_helper = DownloadHelper()

        download_helper.set_retries(given)

        actual = download_helper.retries

        self.assertEqual(expected, actual)

        download_helper = DownloadHelper(retries=given)

        actual = download_helper.retries

        self.assertEqual(expected, actual)

    def test_set_retries_not_int(self) -> None:
        """
        Tests the method which let us set the number of retry to perform for the
        case that the given value is not a string.
        """

        given = ["Hello", "World"]

        download_helper = DownloadHelper()

        self.assertRaises(TypeError, lambda: download_helper.set_retries(given))

    def test_set_retries_less_than_zero(self) -> None:
        """
        Tests the method which let us set the number of retry to perform for the
        case that the given value is less than zero
        """

        given = -1
        download_helper = DownloadHelper()

        self.assertRaises(ValueError, lambda: download_helper.set_retries(given))

    @unittest.mock.patch.object(requests.Session, "get")
    def test_download_text(self, session_patch: unittest.mock.MagicMock) -> None:
        """
        Tests the method which let us set download the text of a given
        url.
        """

        given = "https://exmaple.org"

        download_helper = DownloadHelper(given)

        session_patch.return_value.text = "Hello, World!"
        session_patch.return_value.status_code = 200

        expected = "Hello, World!"
        actual = download_helper.download_text()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "get")
    def test_download_text_to_file(
        self, session_patch: unittest.mock.MagicMock
    ) -> None:
        """
        Tests the method which let us set download the text of a given
        url for the case that we want the response into a file.
        """

        destination = tempfile.NamedTemporaryFile()

        given = "https://exmaple.org"

        download_helper = DownloadHelper(given)

        session_patch.return_value.text = "Hello, World!"
        session_patch.return_value.status_code = 200

        download_helper.download_text(destination=destination.name)

        destination.seek(0)

        expected = b"Hello, World!"
        actual = destination.read()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "get")
    def test_download_text_response_not_ok(
        self, session_patch: unittest.mock.MagicMock
    ) -> None:
        """
        Tests the method which let us set download the text of a given
        url for the case that the response is not ok.
        """

        destination = tempfile.NamedTemporaryFile()

        given = "https://exmaple.org"

        download_helper = DownloadHelper(given)

        session_patch.return_value.status_code = 500

        self.assertRaises(
            PyFunceble.helpers.exceptions.UnableToDownload,
            lambda: download_helper.download_text(destination=destination.name),
        )


if __name__ == "__main__":
    unittest.main()
