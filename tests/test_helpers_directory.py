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
