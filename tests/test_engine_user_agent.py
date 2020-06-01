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
