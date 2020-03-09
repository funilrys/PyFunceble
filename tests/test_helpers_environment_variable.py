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

Tests of PyFunceble.helpers.environement_variable

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

from os import environ
from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.helpers import EnvironmentVariable


class TestEnvironmentVariable(TestCase):
    """
    Tests of PyFunceble.helpers.environement_variable
    """

    def test_name_exists(self):
        """
        Tests the case that a name exist.
        """

        environ["TEST"] = "test"

        expected = True
        actual = EnvironmentVariable("TEST").exists()

        self.assertEqual(expected, actual)

    def test_name_does_not_exists(self):
        """
        Tests the case that a name does not exist.
        """

        expected = False
        actual = EnvironmentVariable("HELLO,WORLD").exists()

        self.assertEqual(expected, actual)

    def test_get_value(self):
        """
        Tests the case that the value is needed.
        """

        environ["TEST"] = "Hello, World!"
        expected = "Hello, World!"
        actual = EnvironmentVariable("TEST").get_value()

        self.assertEqual(expected, actual)

    def test_get_default_value(self):
        """
        Tests the case that the environment variable does not
        exists and the value is needed.
        """

        expected = None
        actual = EnvironmentVariable("Hello,World").get_value()

        self.assertEqual(expected, actual)

        expected = True
        actual = EnvironmentVariable("Hello,World").get_value(default=True)

        self.assertEqual(expected, actual)

    def test_set_value(self):
        """
        Tests the case the we want to set the value of an environment variable.
        """

        expected_value = "Hello!"

        expected_output = True
        actual = EnvironmentVariable("TEST").set_value("Hello!")

        self.assertEqual(expected_output, actual)
        self.assertEqual(expected_value, environ["TEST"])

    def test_set_value_wrong_type(self):
        """
        Tests the case that we want to set a non string value.
        """

        self.assertRaises(TypeError, lambda: EnvironmentVariable("TEST").set_value(1))


if __name__ == "__main__":
    launch_tests()
