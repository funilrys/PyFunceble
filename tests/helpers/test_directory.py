"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the directory helper.

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
import unittest.mock

from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.list import ListHelper
from PyFunceble.utils.platform import PlatformUtility


class TestDirectoryHelper(unittest.TestCase):
    """
    Tests of the directory helper.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.temp_path = tempfile.TemporaryDirectory()

        self.helper = DirectoryHelper(path=self.temp_path.name)

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.helper

        self.temp_path.cleanup()
        del self.temp_path

    def test_set_path_return(self) -> None:
        """
        Tests the response from the method which let us set the path to work
        with.
        """

        actual = self.helper.set_path(self.temp_path.name)

        self.assertIsInstance(actual, DirectoryHelper)

    def test_set_path_method(self) -> None:
        """
        Tests the method which let us set the path to work with.
        """

        given = self.temp_path.name
        expected = self.temp_path.name

        self.helper.set_path(given)

        actual = self.helper.path

        self.assertEqual(expected, actual)

    def test_set_path_attribute(self) -> None:
        """
        Tests overwritting of the :code:`path` attribute.
        """

        given = self.temp_path.name
        expected = self.temp_path.name

        self.helper.path = given
        actual = self.helper.path

        self.assertEqual(expected, actual)

    def test_set_path_through_init(self) -> None:
        """
        Tests the overwritting of the path to work through the class
        constructor.
        """

        given = self.temp_path.name
        expected = self.temp_path.name

        helper = DirectoryHelper(given)
        actual = helper.path

        self.assertEqual(expected, actual)

    def test_set_path_not_str(self) -> None:
        """
        Tests the method which let us set the path to work with for the case
        that it's not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.helper.set_path(given))

    def test_realpath(self) -> None:
        """
        Tests the method which let us get the real path to the currently set
        path.
        """

        expected = os.path.realpath(self.temp_path.name)

        actual = self.helper.realpath

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(os, "getcwd")
    def test_get_current(self, getcwd_path: unittest.mock.MagicMock) -> None:
        """
        Tests the method which let us get the current directory.
        """

        getcwd_path.return_value = "/hello/world"

        expected = "/hello/world"
        actual = self.helper.get_current()

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(os, "getcwd")
    def test_get_current_with_sep(self, getcwd_path: unittest.mock.MagicMock) -> None:
        """
        Tests the method which let us get the current directory for the case
        that we want to have the directory separator at  the end.
        """

        getcwd_path.return_value = "/hello/world"

        if PlatformUtility.is_windows():
            expected = "/hello/world\\"
        else:
            expected = "/hello/world/"

        actual = self.helper.get_current(with_end_sep=True)

        self.assertEqual(expected, actual)

    def test_join_path(self) -> None:
        """
        Tests the method which let us join paths.
        """

        if PlatformUtility.is_windows():
            given = "\\hello\\world"
            expected = "\\hello\\world\\hello\\world"
        else:
            given = "/hello/world"
            expected = "/hello/world/hello/world"

        actual = DirectoryHelper(given).join_path("hello", "world")

        self.assertEqual(expected, actual)

    def test_exists(self) -> None:
        """
        Tests the method which let check if a directory exists.
        """

        self.helper.set_path(self.helper.join_path(secrets.token_urlsafe(8)))

        expected = False
        actual = self.helper.exists()

        self.assertEqual(expected, actual)

        expected = True
        os.makedirs(self.helper.path)

        actual = self.helper.exists()

        self.assertEqual(expected, actual)

    def test_create_and_delete(self) -> None:
        """
        Tests the methods which let us create and delete a directory.
        """

        self.helper.set_path(self.helper.join_path(secrets.token_urlsafe(8)))

        expected = False
        actual = self.helper.exists()

        self.assertEqual(expected, actual)

        expected = True
        actual = self.helper.create().exists()

        self.assertEqual(expected, actual)

        expected = False
        actual = self.helper.delete().exists()

        self.assertEqual(expected, actual)

    def test_list_all_subdirectories(self) -> None:
        """
        Tests the method which let us list all subdirectories.
        """

        dirname = [secrets.token_hex(6) for _ in range(10)]

        for directory in dirname:
            self.helper.set_path(os.path.join(self.temp_path.name, directory)).create()

            self.helper.set_path(
                os.path.join(self.temp_path.name, directory, directory)
            ).create()

            self.helper.set_path(
                os.path.join(self.temp_path.name, directory, directory, directory)
            ).create()

        self.helper.set_path(self.temp_path.name)

        expected = (
            ListHelper(
                [os.path.join(self.temp_path.name, x) for x in dirname]
                + [os.path.join(self.temp_path.name, x, x) for x in dirname]
                + [os.path.join(self.temp_path.name, x, x, x) for x in dirname]
            )
            .remove_duplicates()
            .sort()
            .subject
        )

        actual = self.helper.list_all_subdirectories()

        self.assertEqual(expected, actual)

    def test_list_all_files(self) -> None:
        """
        Tests the method which let us list all subdirectories.
        """

        dirname = [secrets.token_hex(6) for _ in range(10)]
        filename = secrets.token_hex(6)

        for directory in dirname:
            self.helper.set_path(os.path.join(self.temp_path.name, directory)).create()

            with open(os.path.join(self.helper.path, filename), "w") as file_stream:
                file_stream.write("Hello")

            self.helper.set_path(
                os.path.join(self.temp_path.name, directory, directory)
            ).create()

            with open(os.path.join(self.helper.path, filename), "w") as file_stream:
                file_stream.write("Hello")

            self.helper.set_path(
                os.path.join(self.temp_path.name, directory, directory, directory)
            ).create()

            with open(os.path.join(self.helper.path, filename), "w") as file_stream:
                file_stream.write("Hello")

        self.helper.set_path(self.temp_path.name)

        expected = (
            ListHelper(
                [os.path.join(self.temp_path.name, x, filename) for x in dirname]
                + [os.path.join(self.temp_path.name, x, x, filename) for x in dirname]
                + [
                    os.path.join(self.temp_path.name, x, x, x, filename)
                    for x in dirname
                ]
            )
            .sort()
            .subject
        )

        actual = self.helper.list_all_files()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
