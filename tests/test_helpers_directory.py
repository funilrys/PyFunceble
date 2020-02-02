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

Tests of PyFunceble.helpers.directory

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

from os import path
from os import sep as directory_separator
from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.helpers import Directory


class TestDirectory(TestCase):
    """
    Tests of PyFunceble.helpers.directory.
    """

    def tests_create_and_delete(self):
        """
        Tests the methods which let us create and delete
        a directory.
        """

        directory_test = "this_directory_is_a_ghost"
        dir_instance = Directory(directory_test)

        dir_instance.delete()

        expected = False
        actual = path.isdir(directory_test)

        self.assertEqual(expected, actual)

        dir_instance.create()

        expected = True
        actual = path.isdir(directory_test)

        self.assertEqual(expected, actual)

        dir_instance.delete()

    def test_fix_path(self):
        """
        Tests the method which allows us to fix
        directory paths.
        """

        expected = "hello" + directory_separator + "world" + directory_separator
        actual = Directory("/hello/world").fix_path()

        self.assertEqual(expected, actual)

        actual = Directory("\\hello\\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory("hello\\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory(r"hello\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory(r"hello/world/").fix_path()
        self.assertEqual(expected, actual)

        to_test = ["", None, []]

        for element in to_test:
            actual = Directory(element).fix_path()
            self.assertEqual(element, actual)


if __name__ == "__main__":
    launch_tests()
