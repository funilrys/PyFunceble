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
            "googleadservices.com",
            "google-analytics.com",
            "google.com",
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
            "www-google-analytics.l.google.com",
            "www.googletagmanager.com",
            "www.googletagservices.com",
        ]
        actual = List(self.data_list).custom_format(Sort.standard)

        self.assertEqual(expected, actual)

        expected = [
            "https://0.gravatar.com",
            "https://1.gravatar.com",
            "https://ad-creatives-public.commondatastorage.googleapis.com",
            "https://ade.googlesyndication.com",
            "https://adservice.google.com",
            "https://chart.googleapis.com",
            "https://googleadservices.com",
            "https://google-analytics.com",
            "https://google.com",
            "https://hello",
            "https://hello_world.google.com",
            "https://imasdk.googleapis.com",
            "https://pagead2.googleadservices.com",
            "https://pagead2.googlesyndication.com",
            "https://partner.googleadservices.com",
            "https://redirector.googlevideo.com",
            "https://s0-2mdn-net.l.google.com",
            "https://ssl.google-analytics.com",
            "https://ssl-google-analytics.l.google.com",
            "https://tpc.googlesyndication.com",
            "https://www.googleadservices.com",
            "https://www.google-analytics.com",
            "https://www-google-analytics.l.google.com",
            "https://www.googletagmanager.com",
            "https://www.googletagservices.com",
        ]
        actual = List(self.data_url_list).custom_format(Sort.standard)

        self.assertEqual(expected, actual)

    def test_hierarchical_sorting(self):
        """
        Tests hierarchical sorting.
        """

        expected = [
            "chart.googleapis.com",
            "ad-creatives-public.commondatastorage.googleapis.com",
            "googleadservices.com",
            "pagead2.googleadservices.com",
            "partner.googleadservices.com",
            "www.googleadservices.com",
            "google-analytics.com",
            "ssl.google-analytics.com",
            "www.google-analytics.com",
            "google.com",
            "adservice.google.com",
            "hello_world.google.com",
            "s0-2mdn-net.l.google.com",
            "ssl-google-analytics.l.google.com",
            "www-google-analytics.l.google.com",
            "ade.googlesyndication.com",
            "pagead2.googlesyndication.com",
            "tpc.googlesyndication.com",
            "www.googletagmanager.com",
            "www.googletagservices.com",
            "redirector.googlevideo.com",
            "0.gravatar.com",
            "1.gravatar.com",
            "hello",
            "imasdk.googleapis.com",
        ]
        actual = List(self.data_list).custom_format(Sort.hierarchical)

        self.assertEqual(expected, actual)

        expected = [
            "https://chart.googleapis.com",
            "https://ad-creatives-public.commondatastorage.googleapis.com",
            "https://googleadservices.com",
            "https://pagead2.googleadservices.com",
            "https://partner.googleadservices.com",
            "https://www.googleadservices.com",
            "https://google-analytics.com",
            "https://ssl.google-analytics.com",
            "https://www.google-analytics.com",
            "https://google.com",
            "https://adservice.google.com",
            "https://hello_world.google.com",
            "https://s0-2mdn-net.l.google.com",
            "https://ssl-google-analytics.l.google.com",
            "https://www-google-analytics.l.google.com",
            "https://ade.googlesyndication.com",
            "https://pagead2.googlesyndication.com",
            "https://tpc.googlesyndication.com",
            "https://www.googletagmanager.com",
            "https://www.googletagservices.com",
            "https://redirector.googlevideo.com",
            "https://0.gravatar.com",
            "https://1.gravatar.com",
            "https://hello",
            "https://imasdk.googleapis.com",
        ]
        actual = List(self.data_url_list).custom_format(Sort.hierarchical)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
