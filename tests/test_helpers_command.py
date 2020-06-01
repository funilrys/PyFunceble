# pylint:disable=line-too-long,invalid-name,import-error
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.helpers.command

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

import sys
from unittest import main as launch_tests

from PyFunceble.abstracts import Platform
from PyFunceble.helpers import Command
from stdout_base import StdoutBase


class TestCommand(StdoutBase):
    """
    Tests of PyFunceble.helpers.command.
    """

    def test_execute(self):
        """
        Tests the execution of command.
        """

        if Platform.is_unix():
            expected = "Hello, World!\n"
            actual = Command("echo 'Hello, World!'").execute()

            self.assertEqual(expected, actual)

            expected = ""
            actual = Command("printf ''").execute()

            self.assertEqual(expected, actual)

    def test_run_to_stdout(self):
        """
        Tests the run of command.
        """

        if Platform.is_unix():
            expected = "Hello, World!\n"

            Command("echo 'Hello, World!'").run_to_stdout()

            actual = sys.stdout.getvalue()

            self.assertEqual(expected, actual)

    def test_run(self):
        """
        Tests the run of a command.
        """

        if Platform.is_unix():
            expected = ["Hello, World!"]
            actual = list(Command("echo 'Hello, World!'").run())

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
