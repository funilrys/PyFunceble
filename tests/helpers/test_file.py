"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the file helper.

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


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

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

import os
import secrets
import tempfile
import unittest

from PyFunceble.helpers.file import FileHelper


class TestFileHelper(unittest.TestCase):
    """
    Tests of the file helpers.
    """

    def test_set_path_return(self) -> None:
        """
        Tests the response from the method which let us set the path to work with.
        """

        given = tempfile.NamedTemporaryFile()

        file_helper = FileHelper()
        actual = file_helper.set_path(given.name)

        self.assertIsInstance(actual, FileHelper)

    def test_set_path(self) -> None:
        """
        Tests the method which let us set the path to work with.
        """

        given = tempfile.NamedTemporaryFile()
        expected = given.name

        file_helper = FileHelper()
        file_helper.set_path(given.name)

        actual = file_helper.path

        self.assertEqual(expected, actual)

        file_helper = FileHelper(given.name)

        actual = file_helper.path

        self.assertEqual(expected, actual)

    def test_set_path_not_str(self) -> None:
        """
        Tests the method which let us set the path to work with for the case
        that it's not a string.
        """

        given = ["Hello", "World"]

        file_helper = FileHelper()

        self.assertRaises(TypeError, lambda: file_helper.set_path(given))

    def test_join_path(self) -> None:
        """
        Tests the method which let us join paths.
        """

        given = "/hello/world"
        expected = "/hello/world/hello/world"

        actual = FileHelper(given).join_path("hello", "world")

        self.assertEqual(expected, actual)

    def test_exists(self) -> None:
        """
        Tests the method which let us check if the given file exists.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        with open(file_helper.path, "w") as file_stream:
            file_stream.write("Hello, World!")

        expected = True
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        os.remove(file_helper.path)

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

    def test_get_size(self) -> None:
        """
        Tests the method which let us get the size of a file.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        with open(file_helper.path, "w") as file_stream:
            file_stream.write("Hello, World!")

        expected = True
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = 13
        actual = file_helper.get_size()

        self.assertEqual(expected, actual)

        os.remove(file_helper.path)

    def test_is_empty(self) -> None:
        """
        Tests the method which let us check if a file is empty.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        with open(file_helper.path, "w") as file_stream:
            file_stream.write("")

        expected = True
        actual = file_helper.is_empty()

        self.assertEqual(expected, actual)

        with open(file_helper.path, "w") as file_stream:
            file_stream.write("Hello, World!")

        expected = False
        actual = file_helper.is_empty()

        self.assertEqual(expected, actual)

        os.remove(file_helper.path)

    def test_delete(self) -> None:
        """
        Tests the method which let us delete a file.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        with open(file_helper.path, "w") as file_stream:
            file_stream.write("")

        expected = True
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        file_helper.delete()

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

    def test_write(self) -> None:
        """
        Tests the method which let us write a file.
        """

        given = tempfile.NamedTemporaryFile()

        file_helper = FileHelper(given.name)

        file_helper.write("Hello, World!")
        given.seek(0)

        expected = b"Hello, World!"
        actual = given.read()

        self.assertEqual(expected, actual)

        file_helper.write("Hello, this is Funilrys!")
        given.seek(0)

        expected = b"Hello, World!Hello, this is Funilrys!"
        actual = given.read()

        self.assertEqual(expected, actual)

        file_helper.write("Hello, World!", overwrite=True)
        given.seek(0)

        expected = b"Hello, World!"
        actual = given.read()

        self.assertEqual(expected, actual)

    def test_read(self) -> None:
        """
        Tests the method which let us read a file.
        """

        given = tempfile.NamedTemporaryFile()

        file_helper = FileHelper(given.name)

        file_helper.write("Hello, World!")
        given.seek(0)

        expected = "Hello, World!"
        actual = file_helper.read()

        self.assertEqual(expected, actual)

    def test_read_file_does_not_exists(self) -> None:
        """
        Tests the method which let us read a file for the case that the given
        file does not exists.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = None
        actual = file_helper.read()

        self.assertEqual(expected, actual)

    def test_read_bytes(self) -> None:
        """
        Tests the method which let us read (bytes) a file.
        """

        given = tempfile.NamedTemporaryFile()

        file_helper = FileHelper(given.name)

        file_helper.write("Hello, World!")
        given.seek(0)

        expected = b"Hello, World!"
        actual = file_helper.read_bytes()

        self.assertEqual(expected, actual)

    def test_read_bytes_file_does_not_exists(self) -> None:
        """
        Tests the method which let us read (bytes) a file for the case that
        the given file does not exists.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = None
        actual = file_helper.read_bytes()

        self.assertEqual(expected, actual)

    def test_open(self) -> None:
        """
        Tests the method which let us open the given file as we want.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        with file_helper.open("w") as file_stream:
            file_stream.write("Hello, World!")

        expected = True
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = "Hello, World!"
        actual = file_helper.read()

        self.assertEqual(expected, actual)

    def test_copy(self) -> None:
        """
        Tests the method which let us copy a file to another place.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        copy_file_helper = FileHelper(tempfile.gettempdir())
        copy_file_helper.set_path(copy_file_helper.join_path(secrets.token_hex(8)))

        expected = False
        actual = file_helper.exists()
        actual_copy = copy_file_helper.exists()

        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_copy)

        file_helper.write("Hello, World!")

        expected = True
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = False
        actual_copy = copy_file_helper.exists()

        self.assertEqual(expected, actual_copy)

        file_helper.copy(copy_file_helper.path)

        expected = True
        actual_copy = copy_file_helper.exists()

        self.assertEqual(expected, actual_copy)

        expected = "Hello, World!"
        actual = copy_file_helper.read()

        self.assertEqual(expected, actual)

        expected = True
        actual = file_helper.exists()
        actual_copy = copy_file_helper.exists()

        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_copy)

    def test_move(self) -> None:
        """
        Tests of the method which let us move a file to another location.
        """

        file_helper = FileHelper(tempfile.gettempdir())
        file_helper.set_path(file_helper.join_path(secrets.token_hex(8)))

        destination_file_helper = FileHelper(tempfile.gettempdir())
        destination_file_helper.set_path(
            destination_file_helper.join_path(secrets.token_hex(8))
        )

        expected = False
        actual = file_helper.exists()
        actual_destination = destination_file_helper.exists()

        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual_destination)

        file_helper.write("Hello, World!")

        expected = True
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = False
        actual_destination = destination_file_helper.exists()

        self.assertEqual(expected, actual_destination)

        file_helper.move(destination_file_helper.path)

        expected = True
        actual_destination = destination_file_helper.exists()

        self.assertEqual(expected, actual_destination)

        expected = "Hello, World!"
        actual = destination_file_helper.read()

        self.assertEqual(expected, actual)

        expected = False
        actual = file_helper.exists()

        self.assertEqual(expected, actual)

        expected = True
        actual_destination = destination_file_helper.exists()

        self.assertEqual(expected, actual_destination)


if __name__ == "__main__":
    unittest.main()
