# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.preset.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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
from PyFunceble.preset import Preset


class TestSwitch(TestCase):
    """
    Test the switching subsystem.
    """

    def setUp(self):
        """
        Setup everything that is needed.
        """

        PyFunceble.load_config(generate_directory_structure=False)

        self.exception_message = "Impossible to switch %s. Please post an issue to https://github.com/funilrys/PyFunceble/issues."  # pylint:disable=line-too-long

    def test_index_not_exist(self):
        """
        Test the case that the switched data does not exist into
        the configuration system.
        """

        to_switch = "helloworld"

        self.assertRaisesRegex(
            Exception,
            self.exception_message % repr(to_switch),
            lambda: Preset.switch(to_switch),
        )

    def test_switch_true(self):
        """
        Test the case that we want to switch a switch which is set
        to True.
        """

        PyFunceble.CONFIGURATION["helloworld"] = True

        expected = False
        actual = Preset.switch("helloworld")

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["helloworld"]

    def test_switch_false(self):
        """
        Test the case that we want to switch a switch which is set
        to False.
        """

        PyFunceble.CONFIGURATION["helloworld"] = False

        expected = True
        actual = Preset.switch("helloworld")

        self.assertEqual(expected, actual)

        del PyFunceble.CONFIGURATION["helloworld"]

    def test_switch_value_is_not_bool(self):
        """
        Test the case that we want to switch a switch which is not
        in bool format.
        """
        PyFunceble.CONFIGURATION["helloworld"] = "Hello, World!"

        to_switch = "helloworld"

        self.assertRaisesRegex(
            Exception,
            self.exception_message % repr(to_switch),
            lambda: Preset.switch(to_switch),
        )

        del PyFunceble.CONFIGURATION["helloworld"]


class TestsResetCounters(TestCase):
    """
    Test of PyFunceble.preset.Preset.reset_counters
    """

    def setUp(self):
        """
        Setup everything that is needed for the test.
        """

        PyFunceble.load_config(generate_directory_structure=False)

        self.types = ["up", "down", "invalid", "tested"]

    def set_counter(self):
        """
        Set every counter to 15.
        """

        for string in self.types:
            PyFunceble.INTERN["counter"]["number"].update({string: 15})

    def tests_counter_set(self):
        """
        Test if the counter is really set.
        """

        self.set_counter()

        for string in self.types:
            expected = 15
            actual = PyFunceble.INTERN["counter"]["number"][string]

            self.assertEqual(expected, actual)

    def tests_reset_counters(self):
        """
        Test if the counter is reseted.
        """

        Preset.reset_counters()

        for string in self.types:
            expected = 0
            actual = PyFunceble.INTERN["counter"]["number"][string]

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
