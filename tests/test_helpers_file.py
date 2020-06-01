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

Tests of PyFunceble.helpers.file

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

from PyFunceble.helpers import File


class TestFile(TestCase):
    """
    Tests of PyFunceble.helpers.file.
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.file = "this_file_is_a_ghost"

        self.file_instance = File(self.file)
        self.file_instance_2 = File(self.file + "_2")

        self.file_instance.delete()
        self.file_instance_2.delete()

    def tearDown(self):
        """
        Setups everything needed after the tests.
        """

        self.file_instance.delete()
        self.file_instance_2.delete()

    def test_exists(self):
        """
        Tests method which let us check the existance
        of a file.
        """

        expected = False
        actual = self.file_instance.exists()

        self.assertEqual(expected, actual)

        self.file_instance.write(self.file_instance.path)

        expected = True
        actual = self.file_instance.exists()

        self.assertEqual(expected, actual)

    def test_get_size(self):
        """
        Tests the method which let us get the size of a file.
        """

        self.file_instance.write("Hello, World!", overwrite=True)

        expected = 13
        actual = self.file_instance.get_size()

        self.assertEqual(expected, actual)

        self.file_instance.write(" ", overwrite=True)

        expected = 1
        actual = self.file_instance.get_size()

        self.assertEqual(expected, actual)

    def test_is_emtpy(self):
        """
        Tests the method which let us know if a file is empty.
        """

        self.file_instance.write("Hello!!", overwrite=True)

        expected = False
        actual = self.file_instance.is_empty()

        self.assertEqual(expected, actual)

        self.file_instance.write("", overwrite=True)

        expected = True
        actual = self.file_instance.is_empty()

        self.assertEqual(expected, actual)

    def test_delete_read_and_write(self):
        """
        Tests the method which let us delete and write into a file.
        """

        self.file_instance.write("Hello, World!")

        expected = "Hello, World!"
        actual = self.file_instance.read()

        self.assertEqual(expected, actual)

        self.file_instance.write("Hello, World!")

        expected += "Hello, World!"
        actual = self.file_instance.read()

        self.assertEqual(expected, actual)

        self.file_instance.write("Crap!", overwrite=True)

        expected = "Crap!"
        actual = self.file_instance.read()

        self.assertEqual(expected, actual)

    def test_copy(self):
        """
        Tests the method which let us copy a file to another location.
        """

        self.file_instance.write("Hello, World!")

        expected = "Hello, World!"
        actual = self.file_instance.read()

        self.assertEqual(expected, actual)

        self.file_instance.copy(self.file_instance_2.path)

        expected = True

        self.assertEqual(expected, self.file_instance_2.exists())
        self.assertEqual(expected, self.file_instance.exists())

        expected = "Hello, World!"
        actual = self.file_instance_2.read()

        self.assertEqual(expected, actual)

    def test_move(self):
        """
        Tests the method which let us move a file to another location.
        """

        self.file_instance.write("Hello, World!")

        expected = "Hello, World!"
        actual = self.file_instance.read()

        self.assertEqual(expected, actual)

        self.file_instance.move(self.file_instance_2.path)

        expected = True
        actual = self.file_instance_2.exists()

        self.assertEqual(expected, actual)

        expected = False
        actual = self.file_instance.exists()

        self.assertEqual(expected, actual)

        expected = "Hello, World!"
        actual = self.file_instance_2.read()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
