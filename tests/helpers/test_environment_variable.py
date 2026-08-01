"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the tests of our environment variable helpers.

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

import os
import tempfile
import unittest
import uuid
from pathlib import Path

from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper


class TestEnvironmentVariableHelper(unittest.TestCase):
    """
    Tests of our environment variable helper.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.helper = EnvironmentVariableHelper()

        self.test_name = "PYFUNCEBLE_TESTING"

        temp_dir = tempfile.gettempdir()
        uniq_env_file_name = f"test_envsys_{uuid.uuid4()}.env"
        self.temp_env_file = Path(os.path.join(temp_dir, uniq_env_file_name))
        self.temp_env_file.touch(exist_ok=True)

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        self.temp_env_file.unlink(missing_ok=True)

        del self.temp_env_file
        del self.test_name
        del self.helper

    def test_set_name_return(self) -> None:
        """
        Tests the response from the method which let us set the name to work
        with.
        """

        actual = self.helper.set_name(self.test_name)

        self.assertIsInstance(actual, EnvironmentVariableHelper)

    def test_set_name_method(self) -> None:
        """
        Tests the method which let us set the name to work with.
        """

        given = self.test_name
        expected = given

        self.helper.set_name(given)

        actual = self.helper.name

        self.assertEqual(expected, actual)

    def test_set_name_attribute(self) -> None:
        """
        Tests the method which let us overwrite the `name` attribute.
        """

        given = self.test_name
        expected = given

        self.helper.name = given

        actual = self.helper.name

        self.assertEqual(expected, actual)

    def test_set_name_through_init(self) -> None:
        """
        Tests the overwritting of the name to work with through the class
        constructor.
        """

        given = self.test_name
        expected = given

        helper = EnvironmentVariableHelper(given)
        actual = helper.name

        self.assertEqual(expected, actual)

    def test_set_env_file_path_return(self) -> None:
        """
        Tests the response from the method which let us set the path to the
        dot env file to work with.
        """

        actual = self.helper.set_env_file_path(str(self.temp_env_file))

        self.assertIsInstance(actual, EnvironmentVariableHelper)

    def test_set_env_file_path_method(self) -> None:
        """
        Tests the method which let us set the path to the dotenv file to work with.
        """

        given = str(self.temp_env_file)
        expected = given

        self.helper.set_env_file_path(given)

        actual = self.helper.env_file_path

        self.assertEqual(expected, actual)

    def test_set_env_file_path_attribute(self) -> None:
        """
        Tests the method which let us overwrite the `env_file_path` attribute.
        """

        given = str(self.temp_env_file)
        expected = given

        self.helper.env_file_path = given

        actual = self.helper.env_file_path

        self.assertEqual(expected, actual)

    def test_set_env_file_path_through_init(self) -> None:
        """
        Tests the overwritting of the dotenv file to work with through the class
        constructor.
        """

        given = str(self.temp_env_file)
        expected = given

        helper = EnvironmentVariableHelper(env_file_path=given)
        actual = helper.env_file_path

        self.assertEqual(expected, actual)

    def test_set_name_not_str(self) -> None:
        """
        Tests the method which let us set the name of the environment variable
        to work with for the case that the given name is not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.helper.set_name(given))

    def test_set_env_file_path_not_str(self) -> None:
        """
        Tests the method which let us set the path to the dotenv file to work
        with for the case that the given path is not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.helper.set_env_file_path(given))

    def test_exists(self) -> None:
        """
        Tests of the method which let us test if an environment variable exists.
        """

        expected = False
        actual = self.helper.set_name(self.test_name).exists()

        self.assertEqual(expected, actual)

        os.environ[self.test_name] = "This is a test."

        expected = True
        actual = self.helper.exists()

        self.assertEqual(expected, actual)

        del os.environ[self.test_name]

    def test_get_value(self) -> None:
        """
        Tests of the method which let us get the value of an environment
        variable.
        """

        expected = False
        actual = self.helper.set_name(self.test_name).exists()

        self.assertEqual(expected, actual)

        expected = "Hello"
        actual = self.helper.get_value(default="Hello")

        self.assertEqual(expected, actual)

        expected = "This is a test."

        os.environ[self.test_name] = "This is a test."

        actual = self.helper.get_value(default="Hello")

        self.assertEqual(expected, actual)

        del os.environ[self.test_name]

    def test_get_value_from_file(self) -> None:
        """
        Tests of the method which let us get the value of an environment
        variable from a given environment file.
        """

        self.temp_env_file.write_text(
            "IS_THIS_A_GHOST=yes", encoding="utf-8", newline="\n"
        )

        self.helper.set_env_file_path(str(self.temp_env_file))
        self.helper.set_name("IS_THIS_A_GHOST")

        expected = "yes"
        actual = self.helper.get_value_from_env_file()

        self.assertEqual(expected, actual)

    def test_get_value_from_file_not_found(self) -> None:
        """
        Tests of the method which let us get the value of an environment
        variable from a given environment file.

        In this case, we test the case that the given value is not known.
        """

        self.temp_env_file.write_text(
            "IS_THIS_A_GHOST_NOOOO=yes", encoding="utf-8", newline="\n"
        )

        self.helper.set_env_file_path(str(self.temp_env_file))
        self.helper.set_name("IS_THIS_A_GHOST")

        expected = "hello"
        actual = self.helper.get_value_from_env_file(default="hello")

        self.assertEqual(expected, actual)

    def test_set_value(self) -> None:
        """
        Tests of the method which let us set the value of an environment
        variable.
        """

        expected = False
        actual = self.helper.set_name(self.test_name).exists()

        self.assertEqual(expected, actual)

        self.helper.set_value("Hello, World!")

        expected = "Hello, World!"
        actual = self.helper.get_value()

        self.assertEqual(expected, actual)

        del os.environ[self.test_name]

    def test_set_value_in_env_file(self) -> None:
        """
        Tests of the method which let us set the value of an environment
        variable into a file.
        """

        self.helper.set_env_file_path(str(self.temp_env_file))
        self.helper.set_name("GHOST_FINDER")

        self.assertIsNone(self.helper.get_value())

        expected = 'GHOST_FINDER="no"\n'

        self.helper.set_value_in_env_file("no")

        self.assertTrue("no" in self.temp_env_file.read_text(encoding="utf-8"))

        expected = "no"

        self.assertEqual(expected, self.helper.get_value())

    def test_set_value_not_str(self) -> None:
        """
        Tests of the method which let us set the value of an environment
        variable for the case that the given value to set is not a string.
        """

        expected = False
        actual = self.helper.set_name(self.test_name).exists()

        self.assertEqual(expected, actual)

        self.assertRaises(TypeError, lambda: self.helper.set_value(["Hello", "World!"]))

    def test_delete(self) -> None:
        """
        Tests of the method which let us delete an environment variable.
        """

        expected = False
        actual = self.helper.set_name(self.test_name).exists()

        self.assertEqual(expected, actual)

        self.helper.set_value("Hello, World!")

        expected = True
        actual = self.helper.exists()

        self.assertEqual(expected, actual)

        self.helper.delete()

        expected = False
        actual = self.helper.exists()

        self.assertEqual(expected, actual)

    def test_delete_value_in_env_file(self) -> None:
        """
        Tests of the method which let us delete the value of an environment
        variable into a file.
        """

        self.temp_env_file.write_text(
            "GHOST_SPEAKER=yes", encoding="utf-8", newline="\n"
        )

        self.helper.set_env_file_path(str(self.temp_env_file))
        self.helper.set_name("GHOST_SPEAKER")

        self.helper.set_value("no")

        self.assertTrue(
            all(
                self.helper.name in x
                for x in self.temp_env_file.read_text(encoding="utf-8").splitlines()
            )
        )

        self.helper.delete_from_env_file()

        self.assertTrue(
            all(
                self.helper.name not in x
                for x in self.temp_env_file.read_text(encoding="utf-8").splitlines()
            )
        )

        self.assertIsNone(self.helper.get_value())


if __name__ == "__main__":
    unittest.main()
