"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.prints


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
# pylint: disable=bad-continuation,protected-access,ungrouped-imports

from unittest import main as launch_tests

import PyFunceble
from helpers import BaseStdout
from PyFunceble.helpers import File
from PyFunceble.prints import Prints


class TestPrints(BaseStdout):
    """
    This class will partially test PyFunceble.prints.
    Indeed, we use the word partially as the whole printing method depends on `print`
    which is a well know keyworkd but also PyFunceble.helpers.File().

    So we do prefer to test all helpers and make sure they are working proprely instead
    if test all the logic.

    We assume the lack of tests here but this class will be completed over time.
    """

    def setUp(self):
        """
        This method setup everything needed for the tests.
        """

        self.file = "this_file_is_a_ghost"
        self.to_print = {
            "basic": {"hello": 5, "world": 6, "here": 7, "is": 8, "PyFunceble": 10},
            "size_constructor": [5, 6, 7, 8, 9, 10],
            "basic_string": "Hello, World!",
        }

    def test_before_header(self):
        """
        This method test the functionability of Prints().before_header()
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        expected = """# File generated with %s
# Date of generation: %s

""" % (
            PyFunceble.LINKS["repo"], PyFunceble.CURRENT_TIME + " "
        )

        Prints(None, None, output_file=self.file, only_on_file=False).before_header()

        self.assertEqual(expected, File(self.file).read())

    def test_header_constructor_with_separator(self):  # pylint: disable=invalid-name
        """
        This method test Prints()._header_constructor() for the case that we
        want to print the header.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        expected = [
            "hello world  here    is       PyFunceble ",
            "----- ------ ------- -------- ---------- ",
        ]
        actual = Prints(
            None, None, output_file=None, only_on_file=False
        )._header_constructor(
            self.to_print["basic"]
        )

        self.assertEqual(expected, actual)

    def test_header_constructor_without_separator(self):  # pylint: disable=invalid-name
        """
        This method test Prints()._header_constructor() for the case that we
        want to print the result of the test.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        expected = ["hello world  here    is       PyFunceble "]
        actual = Prints(
            None, None, output_file=None, only_on_file=False
        )._header_constructor(
            self.to_print["basic"], None
        )

        self.assertEqual(expected, actual)

    def test_data_constructor(self):
        """
        This method test Prints()._data_constructor().
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        expected = PyFunceble.OrderedDict()
        to_print = []

        chars = ["H", "E", "L", "L", "O", "!"]

        for i, size in enumerate(self.to_print["size_constructor"]):
            index = chars[i] * size
            expected[index] = size
            to_print.append(index)

        actual = Prints(
            to_print, None, output_file=None, only_on_file=False
        )._data_constructor(
            self.to_print["size_constructor"]
        )

        self.assertEqual(expected, actual)

        # Test the case that there is an issue.
        expected = PyFunceble.OrderedDict()
        to_print = []

        chars = ["H", "E", "L", "L", "O", "!"]

        for i, size in enumerate(self.to_print["size_constructor"]):
            index = chars[i] * size
            expected[index] = size
            to_print.append(index)

        del to_print[-1]

        self.assertRaisesRegex(
            Exception,
            "Inputed: %d; Size: %d"
            % (
                len(self.to_print["size_constructor"]) - 1,
                len(self.to_print["size_constructor"]),
            ),
            lambda: Prints(
                to_print, None, output_file=None, only_on_file=False
            )._data_constructor(
                self.to_print["size_constructor"]
            ),
        )

    def test_size_from_header(self):
        """
        This method test Prints()._size_from_header() which is used to extract
        the static sizes.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        expected = [element for _, element in self.to_print["basic"].items()]

        actual = Prints(
            None, None, output_file=None, only_on_file=False
        )._size_from_header(
            self.to_print["basic"]
        )

        self.assertEqual(expected, actual)

    def test_colorify(self):
        """
        This method test Prints().colorify(). In other word, it test the coloration
        of the line we have to print depending of the status.
        """

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        # Test with a template that is not designed for colorify
        expected = self.to_print["basic_string"]
        actual = Prints(None, "Hehehe", output_file=None, only_on_file=False)._colorify(
            self.to_print["basic_string"]
        )

        self.assertEqual(expected, actual)

        # Test with a template that is designed for colorify + Status is UP
        expected = PyFunceble.Fore.BLACK + PyFunceble.Back.GREEN + self.to_print[
            "basic_string"
        ]
        actual = Prints(
            ["This is a test", PyFunceble.STATUS["official"]["up"]],
            "Generic",
            output_file=None,
            only_on_file=False,
        )._colorify(
            self.to_print["basic_string"]
        )

        self.assertEqual(expected, actual)

        # Test with a template that is designed for colorify + Status is DOWN
        expected = PyFunceble.Fore.BLACK + PyFunceble.Back.RED + self.to_print[
            "basic_string"
        ]
        actual = Prints(
            ["This is a test", PyFunceble.STATUS["official"]["down"]],
            "Generic",
            output_file=None,
            only_on_file=False,
        )._colorify(
            self.to_print["basic_string"]
        )

        self.assertEqual(expected, actual)

        # Test with a template that is designed for colorify + Status is
        # UNKNOWN or INVALID
        expected = PyFunceble.Fore.BLACK + PyFunceble.Back.CYAN + self.to_print[
            "basic_string"
        ]
        actual = Prints(
            ["This is a test", PyFunceble.STATUS["official"]["invalid"]],
            "Generic",
            output_file=None,
            only_on_file=False,
        )._colorify(
            self.to_print["basic_string"]
        )

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
