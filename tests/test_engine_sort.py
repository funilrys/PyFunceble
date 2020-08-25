# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.engine.sort

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

from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.engine import Sort
from PyFunceble.helpers import List


class TestSort(TestCase):
    """
    Tests of PyFunceble.engine.sort
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.data_list = [
            "adservice.google.com",
            "pagead2.googleadservices.com",
            "ade.googlesyndication.com",
            "1.gravatar.com",
            "chart.googleapis.com",
            "imasdk.googleapis.com",
            "google.com",
            "ad-creatives-public.commondatastorage.googleapis.com",
            "googleadservices.com",
            "www-google-analytics.l.google.com",
            "0.gravatar.com",
            "hello_world.google.com",
            "partner.googleadservices.com",
            "www.googleadservices.com",
            "s0-2mdn-net.l.google.com",
            "ssl-google-analytics.l.google.com",
            "google-analytics.com",
            "redirector.googlevideo.com",
            "www.google-analytics.com",
            "ssl.google-analytics.com",
            "pagead2.googlesyndication.com",
            "www.googletagmanager.com",
            "tpc.googlesyndication.com",
            "www.googletagservices.com",
            "hello",
        ]

        self.data_url_list = [
            "https://0.gravatar.com",
            "https://1.gravatar.com",
            "https://ad-creatives-public.commondatastorage.googleapis.com",
            "https://ade.googlesyndication.com",
            "https://adservice.google.com",
            "https://chart.googleapis.com",
            "https://google.com",
            "https://google-analytics.com",
            "https://googleadservices.com",
            "https://hello_world.google.com",
            "https://imasdk.googleapis.com",
            "https://pagead2.googleadservices.com",
            "https://pagead2.googlesyndication.com",
            "https://partner.googleadservices.com",
            "https://redirector.googlevideo.com",
            "https://s0-2mdn-net.l.google.com",
            "https://ssl-google-analytics.l.google.com",
            "https://ssl.google-analytics.com",
            "https://tpc.googlesyndication.com",
            "https://www-google-analytics.l.google.com",
            "https://www.google-analytics.com",
            "https://www.googleadservices.com",
            "https://www.googletagmanager.com",
            "https://www.googletagservices.com",
            "https://hello",
        ]

    def test_standard_numeric_sorting(self):
        """
        Tests the standard numeric sorting.
        """

        given = [
            "1.example.com",
            "2.example.com",
            "3.example.com",
            "11.example.com",
            "12.example.com",
            "10.example.com",
        ]

        given_url = [f"http://{x}" for x in given]

        expected = [
            "1.example.com",
            "2.example.com",
            "3.example.com",
            "10.example.com",
            "11.example.com",
            "12.example.com",
        ]

        expected_url = [f"http://{x}" for x in expected]

        actual = List(given).custom_format(Sort.standard)

        self.assertEqual(expected, actual)

        actual_url = List(given_url).custom_format(Sort.standard)

        self.assertEqual(expected_url, actual_url)

    def test_hierarchical_numeric_sorting(self):
        """
        Tests the hierarchical numeric sorting.
        """

        given = [
            "1.example.com",
            "2.example.com",
            "3.example.com",
            "11.example.com",
            "12.example.com",
            "10.example.com",
            "hello.1.example.com",
            "hello.2.example.com",
            "hello.3.example.com",
            "hello.11.example.com",
            "hello.12.example.com",
            "hello.10.example.com",
        ]

        expected = [
            "1.example.com",
            "hello.1.example.com",
            "2.example.com",
            "hello.2.example.com",
            "3.example.com",
            "hello.3.example.com",
            "10.example.com",
            "hello.10.example.com",
            "11.example.com",
            "hello.11.example.com",
            "12.example.com",
            "hello.12.example.com",
        ]

        actual = List(given).custom_format(Sort.hierarchical)

        self.assertEqual(expected, actual)

    def test_standard_sorting(self):
        """
        Tests standard sorting.
        """

        expected = [
            "0.gravatar.com",
            "1.gravatar.com",
            "ad-creatives-public.commondatastorage.googleapis.com",
            "ade.googlesyndication.com",
            "adservice.google.com",
            "chart.googleapis.com",
            "google.com",
            "googleadservices.com",
            "google-analytics.com",
            "hello",
            "hello_world.google.com",
            "imasdk.googleapis.com",
            "pagead2.googleadservices.com",
            "pagead2.googlesyndication.com",
            "partner.googleadservices.com",
            "redirector.googlevideo.com",
            "s0-2mdn-net.l.google.com",
            "ssl.google-analytics.com",
            "ssl-google-analytics.l.google.com",
            "tpc.googlesyndication.com",
            "www.googleadservices.com",
            "www.google-analytics.com",
            "www.googletagmanager.com",
            "www.googletagservices.com",
            "www-google-analytics.l.google.com",
        ]
        actual = List(self.data_list).custom_format(Sort.standard)

        self.assertEqual(expected, actual)

        expected_url = [f"https://{x}" for x in expected]
        actual_url = List(self.data_url_list).custom_format(Sort.standard)

        self.assertEqual(expected_url, actual_url)

    def test_hierarchical_sorting(self):
        """
        Tests hierarchical sorting.
        """

        expected = [
            "google.com",
            "adservice.google.com",
            "hello_world.google.com",
            "s0-2mdn-net.l.google.com",
            "ssl-google-analytics.l.google.com",
            "www-google-analytics.l.google.com",
            "googleadservices.com",
            "pagead2.googleadservices.com",
            "partner.googleadservices.com",
            "www.googleadservices.com",
            "google-analytics.com",
            "ssl.google-analytics.com",
            "www.google-analytics.com",
            "chart.googleapis.com",
            "ad-creatives-public.commondatastorage.googleapis.com",
            "imasdk.googleapis.com",
            "ade.googlesyndication.com",
            "pagead2.googlesyndication.com",
            "tpc.googlesyndication.com",
            "www.googletagmanager.com",
            "www.googletagservices.com",
            "redirector.googlevideo.com",
            "0.gravatar.com",
            "1.gravatar.com",
            "hello",
        ]

        actual = List(self.data_list).custom_format(Sort.hierarchical)

        self.assertEqual(expected, actual)

        expected_url = [f"https://{x}" for x in expected]

        actual_url = List(self.data_url_list).custom_format(Sort.hierarchical)

        self.assertEqual(expected_url, actual_url)


if __name__ == "__main__":
    launch_tests()
