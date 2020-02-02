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

Tests of PyFunceble.engine.user_agent.

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

import PyFunceble


class TestUserAgent(TestCase):
    """
    Tests of PyFunceble.engine.user_agent
    """

    # pylint: disable=unnecessary-lambda

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        PyFunceble.load_config()

        self.user_agent = PyFunceble.engine.UserAgent()
        self.file_instance = PyFunceble.helpers.File(
            PyFunceble.abstracts.Infrastructure.USER_AGENT_FILENAME
        )
        self.file_instance.delete()

    def tearDown(self):
        """
        Setups everything needed after the tests.
        """

        self.file_instance.delete()

    def test_dumped_empty(self):
        """
        Tests of the case that the dump is
        empty.
        """

        self.user_agent.dumped = {}

        self.assertRaises(
            PyFunceble.exceptions.UserAgentBrowserNotFound,
            lambda: self.user_agent.get(),
        )

    def test_dumped_without_chosen_browser(self):
        """
        Tests of the case that the chosen browser
        does not exists.
        """

        del self.user_agent.dumped[PyFunceble.CONFIGURATION.user_agent.browser]

        self.assertRaises(
            PyFunceble.exceptions.UserAgentBrowserNotFound,
            lambda: self.user_agent.get(),
        )

    def test_dumped_without_chosen_platform(self):
        """
        Tests of the case that the chosen platform
        does not exists.
        """

        del self.user_agent.dumped[PyFunceble.CONFIGURATION.user_agent.browser][
            PyFunceble.CONFIGURATION.user_agent.platform
        ]

        self.assertRaises(
            PyFunceble.exceptions.UserAgentPlatformNotFound,
            lambda: self.user_agent.get(),
        )

    def test_dumped_does_not_exists(self):
        """
        Tests of the case that the chosen user agent
        does not exists.
        """

        self.user_agent.dumped[PyFunceble.CONFIGURATION.user_agent.browser][
            PyFunceble.CONFIGURATION.user_agent.platform
        ] = None

        self.assertRaises(
            PyFunceble.exceptions.UserAgentNotFound, lambda: self.user_agent.get(),
        )

    def test_dumped_output(self):
        """
        Tests of the normal case.
        """

        expected = "Hello, World!"

        self.user_agent.dumped[PyFunceble.CONFIGURATION.user_agent.browser][
            PyFunceble.CONFIGURATION.user_agent.platform
        ] = "Hello, World!"

        self.assertEqual(expected, self.user_agent.get())

    def test_custom_output(self):
        """
        Tests of the case that the end-user give us a custom user agent.
        """

        expected = self.user_agent.dumped[PyFunceble.CONFIGURATION.user_agent.browser][
            PyFunceble.CONFIGURATION.user_agent.platform
        ]
        actual = self.user_agent.get()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
