"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our configuration loader.

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

import copy
import os
import tempfile
import unittest

import yaml
from box import Box

from PyFunceble.config.loader import ConfigLoader

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset

import PyFunceble.storage


class TestConfigLoader(unittest.TestCase):
    """
    Provides the test of our configuration loader.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.our_config = Box(copy.deepcopy(pyf_test_dataset.DEFAULT_CONFIG))

        self.default_config_file = tempfile.NamedTemporaryFile(delete=False)
        self.config_file = tempfile.NamedTemporaryFile(delete=False)

        self.merge_upstream = False

        self.config_loader = ConfigLoader()

        self.config_loader.merge_upstream = self.merge_upstream
        self.config_loader.path_to_default_config = self.default_config_file.name
        self.config_loader.path_to_config = self.config_file.name

    def tearDown(self) -> None:
        """
        Destroys everything initiated by the tests.
        """

        self.config_file.close()
        self.default_config_file.close()

        os.unlink(self.config_file.name)
        os.unlink(self.default_config_file.name)

        del self.our_config
        del self.default_config_file
        del self.config_file
        del self.merge_upstream
        del self.config_loader

    def test_is_already_loader(self) -> None:
        """
        Tests the method which let us know if the configuration was already
        loaded.
        """

        PyFunceble.storage.CONFIGURATION = self.our_config

        expected = True
        actual = self.config_loader.is_already_loaded()

        self.assertEqual(expected, actual)

    def test_is_not_already_loaded(self) -> None:
        """
        Tests the method which let us know if the configuration was already
        loaded for the case that it was not loaded yet.
        """

        expected = False
        actual = self.config_loader.is_already_loaded()

        self.assertEqual(expected, actual)

    def test_set_custom_config(self) -> None:
        """
        Tests the method which let us set the custom configuration to work with.
        """

        given = {"hello": "world"}
        expected = {"hello": "world"}

        self.config_loader.custom_config = given
        actual = self.config_loader.custom_config

        self.assertEqual(expected, actual)

    def test_set_custom_config_config_already_loaded(self) -> None:
        """
        Tests the method which let us set the custom configuration to work with.

        In this case, we want the loader to reload (itself). So we basically
        tests that the reload occurs.
        """

        PyFunceble.storage.CONFIGURATION = self.our_config

        given = {"hello": "world"}
        expected = {"hello": "world"}

        self.config_loader.custom_config = given
        actual = self.config_loader.custom_config

        self.assertEqual(expected, actual)

        expected = "world"
        actual = PyFunceble.storage.CONFIGURATION["hello"]

        self.assertEqual(expected, actual)

    def test_set_custom_config_not_dict(self) -> None:
        """
        Tests the method which let us set the custom configuration to work with
        for the case that the given custom configuration is not a
        :py:class:`dict`.
        """

        given = "Hello, World!"

        self.assertRaises(
            TypeError, lambda: self.config_loader.set_custom_config(given)
        )

    def test_set_merge_upstream(self) -> None:
        """
        Tests the method which let us authorize the merging of upstream inside
        the local one.
        """

        given = True
        expected = True

        self.config_loader.merge_upstream = given

        actual = self.config_loader.merge_upstream

        self.assertEqual(expected, actual)

    def test_set_merge_upstream_return(self) -> None:
        """
        Tests the method which let us authorize the merging of upstream inside
        the local one.

        In this case, we just want to be sure that the response is correct.
        """

        given = True

        actual = self.config_loader.set_merge_upstream(given)

        self.assertIsInstance(actual, ConfigLoader)

    def test_set_merge_upstream_not_bool(self) -> None:
        """
        Tests the method which let us authorize the merging of upstream inside
        the local one for the case that the given value is not a boolean.
        """

        given = "Hello, World!"

        self.assertRaises(
            TypeError,
            lambda: self.config_loader.set_merge_upstream(given),
        )

    def test_get_config_file_content(self) -> None:
        """
        Tests the method which let us get the content of the configuration file.
        """

        self.config_file.write(yaml.dump(self.our_config.to_dict()).encode())
        self.config_file.seek(0)

        expected = self.our_config.to_dict()

        actual = self.config_loader.get_config_file_content()

        self.assertEqual(expected, actual)

    def test_get_config_file_content_yaml_issue(self) -> None:
        """
        Tests the method which let us get the content of the configuration file.

        This case try to reproduce the issue we met because of my inattention.
        """

        self.default_config_file.write(yaml.dump(self.our_config.to_dict()).encode())
        self.default_config_file.seek(0)

        self.config_file.write(yaml.dump(self.our_config).encode())
        self.config_file.seek(0)

        expected = self.our_config.to_dict()

        actual = self.config_loader.get_config_file_content()

        self.assertEqual(expected, actual)

    def test_get_config_file_already_exists(self) -> None:
        """
        Tests the method which let us get the content of the configuration file
        for the case that the configuration was already loaded.
        """

        self.config_file.write(yaml.dump(self.our_config.to_dict()).encode())
        self.config_file.seek(0)

        PyFunceble.storage.CONFIGURATION = Box({"hello": "world"})

        expected = {"hello": "world"}
        actual = self.config_loader.get_config_file_content()

        self.assertEqual(expected, actual)

    def test_get_configured_value_not_loaded(self) -> None:
        """
        Tests the method which let us get the configured value.

        In this test, we check for the case that configuration is not
        loaded yet.
        """

        given = "cli_testing.display_mode.colour"

        self.assertRaises(
            RuntimeError, lambda: self.config_loader.get_configured_value(given)
        )

    def test_get_configured_value_not_found(self) -> None:
        """
        Tests the method which let us get the configured value.

        In this test, we check for the case that the wanted index does not
        exists.
        """

        PyFunceble.storage.CONFIGURATION = self.our_config

        given = "hello_world_hello"

        self.assertRaises(
            ValueError, lambda: self.config_loader.get_configured_value(given)
        )

    def test_get_configured_value(self) -> None:
        """
        Tests the method which let us get the configured value.

        In this test, we check for the case that configuration is not
        loaded yet.
        """

        PyFunceble.storage.CONFIGURATION = self.our_config

        given = "cli_testing.testing_mode.syntax"
        actual = self.config_loader.get_configured_value(given)

        self.assertIsInstance(actual, bool)

    def test_start_and_destroy(self) -> None:
        """
        Tests the methods which loads, put everything together and destroy
        the configuration.
        """

        self.config_file.write(yaml.dump(self.our_config.to_dict()).encode())
        self.config_file.seek(0)

        given_custom = {"this_is_a_custom": "test"}
        self.config_loader.set_custom_config(given_custom)

        response = self.config_loader.start()

        self.assertIsInstance(response, ConfigLoader)

        expected_with_custom = dict(
            copy.deepcopy(self.our_config.to_dict()), **given_custom
        )
        self.assertEqual(
            expected_with_custom,
            PyFunceble.storage.CONFIGURATION,
        )

        expected_indexes = ["http_codes", "links"]

        for index in expected_indexes:
            # Tests if correctly stored.
            expected = copy.deepcopy(self.our_config[index])
            actual = getattr(PyFunceble.storage, index.upper())

            self.assertEqual(expected, actual)

        response = self.config_loader.destroy()

        self.assertIsInstance(response, ConfigLoader)

        expected_custom = dict()
        actual = self.config_loader.custom_config

        self.assertEqual(expected_custom, actual)

        expected_indexes = ["http_codes", "links"]
        expected = dict()

        for index in expected_indexes:
            actual = getattr(PyFunceble.storage, index.upper())

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
