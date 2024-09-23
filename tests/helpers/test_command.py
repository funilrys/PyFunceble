"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the tests of our command helpers.

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

import sys
import unittest
import unittest.mock
from subprocess import Popen

from PyFunceble.helpers.command import CommandHelper
from PyFunceble.utils.platform import PlatformUtility

try:
    from stdout_base import StdoutBase
except ModuleNotFoundError:  # pragma: no cover
    from ..stdout_base import StdoutBase


class TestCommandHelper(StdoutBase):
    """
    Tests of the command helper.
    """

    def setUp(self):
        """
        Setups everything needed for the test.
        """

        self.helper = CommandHelper()

        return super().setUp()

    def tearDown(self):
        """
        Destroys everything needed for the test.
        """

        del self.helper

        return super().tearDown()

    def test_set_command_return(self) -> None:
        """
        Tests the response from the method which let us set the command to work
        with.
        """

        given = "echo 'Hello, World'"

        actual = self.helper.set_command(given)

        self.assertIsInstance(actual, CommandHelper)

    def test_set_command_method(self) -> None:
        """
        Tests the method which let us set the command to work with.
        """

        given = "echo 'Hello, World'"
        expected = "echo 'Hello, World'"

        self.helper.set_command(given)

        actual = self.helper.command

        self.assertEqual(expected, actual)

    def test_set_command_attribute(self) -> None:
        """
        Tests overwritting of the :code:`command` attribute.
        """

        given = "echo 'Hello, World'"
        expected = "echo 'Hello, World'"

        self.helper.command = given
        actual = self.helper.command

        self.assertEqual(expected, actual)

    def test_set_command_through_init(self) -> None:
        """
        Tests the overwritting of the command to work through the class
        constructor.
        """

        given = "echo 'Hello, World'"
        expected = "echo 'Hello, World'"

        helper = CommandHelper(given)
        actual = helper.command

        self.assertEqual(expected, actual)

    def test_set_command_list_given(self) -> None:
        """
        Tests the method which let us set the command to execute for
        the case that a list is given.
        """

        given = ["echo", "'Hello, World'"]
        expected = "echo 'Hello, World'"

        self.helper.set_command(given)
        actual = self.helper.command

        self.assertEqual(expected, actual)

    def test_set_command_not_list_or_str(self) -> None:
        """
        Tests the method which let us set the command to execute for the case
        that a list nor a str is given.
        """

        given = True

        self.assertRaises(TypeError, lambda: self.helper.set_command(given))

    def test_set_encoding_return(self) -> None:
        """
        Tests the response from the method which let us set the encoding to use.
        """

        given = "latin-1"

        actual = self.helper.set_encoding(given)

        self.assertIsInstance(actual, CommandHelper)

    def test_set_encoding_method(self) -> None:
        """
        Tests the method which let us set the encoding to use.
        """

        given = "latin-1"
        expected = "latin-1"

        self.helper.set_encoding(given)

        actual = self.helper.encoding

        self.assertEqual(expected, actual)

    def test_set_encoding_attribute(self) -> None:
        """
        Tests overwritting of the :code:`encoding` attribute.
        """

        given = "latin-1"
        expected = "latin-1"

        self.helper.encoding = given
        actual = self.helper.encoding

        self.assertEqual(expected, actual)

    def test_set_encoding_through_init(self) -> None:
        """
        Tests the overwritting of the encoding to use through the class
        constructor.
        """

        given = "latin-1"
        expected = "latin-1"

        helper = CommandHelper(encoding=given)
        actual = helper.encoding

        self.assertEqual(expected, actual)

    def test_set_encoding_not_str(self) -> None:
        """
        Tests the method which let us set  the encoding to use for the case
        that the given encoding is a string.
        """

        given = ["hello", "world"]

        self.assertRaises(TypeError, lambda: self.helper.set_encoding(given))

    def test_execute(self) -> None:
        """
        Tests the method which executes a command.
        """

        if PlatformUtility.is_unix():
            given = "echo 'Hello, World!'"
            expected = "Hello, World!\n"
            actual = self.helper.set_command(given).execute()

            self.assertEqual(expected, actual)

    def test_execute_empty_output(self) -> None:
        """
        Tests the method which executes a command for the case that the given
        command is empty.
        """

        if PlatformUtility.is_unix():
            expected = ""
            actual = self.helper.set_command("printf ''").execute()

            self.assertEqual(expected, actual)

    @unittest.mock.patch.object(Popen, "communicate")
    def test_execute_error(self, communicate_patch) -> None:
        """
        Tests the method which executes a command for the case that an
        error is produced by the command.
        """

        if PlatformUtility.is_unix():
            expected = "This is an error."

            communicate_patch.return_value = (b"", b"This is an error.")

            given = "echo 'This is an error.' 1>&2"
            actual = CommandHelper(given).execute()

            self.assertEqual(expected, actual)

    @unittest.mock.patch.object(Popen, "communicate")
    def test_execute_error_exception(self, communicate_patch) -> None:
        """
        Tests the method which executes a command for the case that an
        error is produced by the command and the end-user want an exception when
        such cases happen.
        """

        if PlatformUtility.is_unix():
            communicate_patch.return_value = (b"", b"This is an error.")

            given = "echo 'This is an error.' 1>&2"
            self.helper.set_command(given)

            self.assertRaises(
                RuntimeError, lambda: self.helper.execute(raise_on_error=True)
            )

    def test_run(self) -> None:
        """
        Tests the method which let us run a command.
        """

        if PlatformUtility.is_unix():
            expected = ["Hello, World!"]
            actual = list(CommandHelper("echo 'Hello, World!'").run())

            self.assertEqual(expected, actual[:1])

    def test_run_to_stdout(self) -> None:
        """
        Tests the method which let us run a command an output to stdout.
        """

        if PlatformUtility.is_unix():
            expected = "Hello, World!\n"

            CommandHelper("echo 'Hello, World!'").run_to_stdout()

            actual = sys.stdout.getvalue()

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
