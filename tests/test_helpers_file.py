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

Tests of the PyFunceble.helpers.file

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

from PyFunceble.helpers import File


class TestFile(TestCase):
    """
    Tests of the PyFunceble.helpers.file.
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.file = "this_file_is_a_ghost"

    def test_exists(self):
        """
        Tests of the method which let us check the existance
        of a file.
        """

        file_instance = File(self.file)
        file_instance.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        with open(self.file, "w") as file_stream:
            file_stream.write(file_instance.path)

        expected = True
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        file_instance.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

    def test_delete_read_and_write(self):
        """
        Tests the method which let us delete and write into a file.
        """

        file_instance = File(self.file)
        file_instance.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        file_instance.write("Hello, World!")

        expected = "Hello, World!"
        actual = file_instance.read()

        self.assertEqual(expected, actual)

        file_instance.write("Hello, World!")

        expected += "Hello, World!"
        actual = file_instance.read()

        self.assertEqual(expected, actual)

        file_instance.write("Crap!", overwrite=True)

        expected = "Crap!"
        actual = file_instance.read()

        self.assertEqual(expected, actual)

        file_instance.delete()

        expected = False
        actual = file_instance.exists()

    def test_copy(self):
        """
        Tests the method which let us copy a file to another location.
        """

        file_instance = File(self.file)
        file_instance.delete()

        file_instance_2 = File(self.file + "_2")
        file_instance_2.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        actual = file_instance_2.exists()

        self.assertEqual(expected, actual)

        file_instance.write("Hello, World!")

        expected = "Hello, World!"
        actual = file_instance.read()

        self.assertEqual(expected, actual)

        file_instance.copy(file_instance_2.path)

        expected = True
        actual = file_instance_2.exists()

        self.assertEqual(expected, actual)
        self.assertEqual(expected, file_instance.exists())

        expected = "Hello, World!"
        actual = file_instance_2.read()

        self.assertEqual(expected, actual)

        file_instance = File(self.file)
        file_instance.delete()

        file_instance_2 = File(self.file + "_2")
        file_instance_2.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        actual = file_instance_2.exists()

        self.assertEqual(expected, actual)

    def test_move(self):
        """
        Tests the method which let us move a file to another location.
        """

        file_instance = File(self.file)
        file_instance.delete()

        file_instance_2 = File(self.file + "_2")
        file_instance_2.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        actual = file_instance_2.exists()

        self.assertEqual(expected, actual)

        file_instance.write("Hello, World!")

        expected = "Hello, World!"
        actual = file_instance.read()

        self.assertEqual(expected, actual)

        file_instance.move(file_instance_2.path)

        expected = True
        actual = file_instance_2.exists()

        self.assertEqual(expected, actual)

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        expected = "Hello, World!"
        actual = file_instance_2.read()

        self.assertEqual(expected, actual)

        file_instance = File(self.file)
        file_instance.delete()

        file_instance_2 = File(self.file + "_2")
        file_instance_2.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        actual = file_instance_2.exists()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
