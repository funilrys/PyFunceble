"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our configuration comparison tool.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023 Nissar Chababy

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
import unittest

from PyFunceble.config.compare import ConfigComparison

try:
    import pyf_test_dataset
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset


class TestConfigCompare(unittest.TestCase):
    """
    Tests our configuration comparison tool.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.our_config = copy.deepcopy(pyf_test_dataset.DEFAULT_CONFIG)

    def tearDown(self) -> None:
        """
        Destroys everything initiated by the tests.
        """

        del self.our_config

    def test_set_local_config_return(self) -> None:
        """
        Tests the response of the method which let us set the local configuration
        to work with.
        """

        given = self.our_config

        config_comparison = ConfigComparison()
        actual = config_comparison.set_local_config(given)

        self.assertIsInstance(actual, ConfigComparison)

    def test_set_local_config_method(self) -> None:
        """
        Tests the method which let us set the local configuration to work with.
        """

        given = self.our_config
        expected = self.our_config

        config_comparison = ConfigComparison()
        config_comparison.set_local_config(given)

        actual = config_comparison.local_config

        self.assertEqual(expected, actual)

    def test_set_local_config_attribute(self) -> None:
        """
        Tests the method which let us set the local configuraiton to work with.

        In this case, we try to overwrite the attribute.
        """

        given = self.our_config
        expected = self.our_config

        config_comparison = ConfigComparison()
        config_comparison.local_config = given

        actual = config_comparison.local_config

        self.assertEqual(expected, actual)

    def test_set_local_config_through_init(self) -> None:
        """
        Tests the method which let us set the local configuraiton to work with.

        In this case, we try to overwrite the attribute through the constructor.
        """

        given = self.our_config
        expected = self.our_config

        config_comparison = ConfigComparison(local_config=given)

        actual = config_comparison.local_config

        self.assertEqual(expected, actual)

    def test_set_local_config_not_dict(self) -> None:
        """
        Tests the method which let us set the local configuration to work with
        for the case that the given local configuration is not a dict.
        """

        given = ["Hello", "World"]

        config_comparison = ConfigComparison()

        self.assertRaises(TypeError, lambda: config_comparison.set_local_config(given))

    def test_set_upstream_config_return(self) -> None:
        """
        Tests the response of the method which let us set the upstream configuration
        to work with.
        """

        given = copy.deepcopy(self.our_config)

        config_comparison = ConfigComparison()
        actual = config_comparison.set_upstream_config(given)

        self.assertIsInstance(actual, ConfigComparison)

    def test_set_upstream_config_method(self) -> None:
        """
        Tests the method which let us set the upstream configuration to work with.
        """

        given = self.our_config
        expected = self.our_config

        config_comparison = ConfigComparison()
        config_comparison.set_upstream_config(given)

        actual = config_comparison.upstream_config

        self.assertEqual(expected, actual)

    def test_set_upstream_config_attribute(self) -> None:
        """
        Tests the method which let us set the upstream configuraiton to work with.

        In this case, we try to overwrite the attribute.
        """

        given = self.our_config
        expected = self.our_config

        config_comparison = ConfigComparison()
        config_comparison.upstream_config = given

        actual = config_comparison.upstream_config

        self.assertEqual(expected, actual)

    def test_set_upstream_config_through_init(self) -> None:
        """
        Tests the method which let us set the upstream configuraiton to work with.

        In this case, we try to overwrite the attribute through the constructor.
        """

        given = self.our_config
        expected = self.our_config

        config_comparison = ConfigComparison(upstream_config=given)

        actual = config_comparison.upstream_config

        self.assertEqual(expected, actual)

    def test_set_upstream_config_not_dict(self) -> None:
        """
        Tests the method which let us set the upstream configuration to work with
        for the case that the given upstream configuration is not a dict.
        """

        given = ["Hello", "World"]

        config_comparison = ConfigComparison()

        self.assertRaises(
            TypeError, lambda: config_comparison.set_upstream_config(given)
        )

    def test_is_local_identical(self) -> None:
        """
        Tests the method which let us check if the given local configuration
        is identical to the upstream one.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = True
        actual = config_comparison.is_local_identical()

        self.assertEqual(expected, actual)

    def test_is_local_identical_missing_key(self) -> None:
        """
        Tests the method which let us check if the given local configuration
        is identical to the upstream one for the case that a key is missing.
        """

        given_upstream = copy.deepcopy(self.our_config)

        to_delete = ["links", "http_codes", "user_agent"]

        for index in to_delete:
            given_local = copy.deepcopy(self.our_config)
            del given_local[index]

            config_comparison = ConfigComparison(
                local_config=given_local, upstream_config=given_upstream
            )

            expected = False
            actual = config_comparison.is_local_identical()

            self.assertEqual(expected, actual)

    def test_is_local_identical_uneeded_links_key(self) -> None:
        """
        Tests the method which let us check if the given local configuration
        is identical to the upstream one for the case that a unneeded key
        inside the list of links is given.
        """

        given_upstream = copy.deepcopy(self.our_config)

        given_local = copy.deepcopy(self.our_config)
        given_local["links"].update(
            {
                "config": "https://example.org/PyFunceble_config.yaml",
                "iana": "https://example.org/iana-db.json",
            }
        )

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = False
        actual = config_comparison.is_local_identical()

        self.assertEqual(expected, actual)

    def test_get_merged_no_changed(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_key_renamed(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we renamed some keys.
        """

        old2new = {
            "hello_world": "cli_testing",
        }

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        for old, new in old2new.items():
            given_local[old] = copy.deepcopy(given_local[new])

            del given_local[new]

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        expected["hello_world"] = self.our_config["cli_testing"]
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_undeeded_links(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we have some uneeded links.
        """

        uneeded_links = {
            "config": "https://example.org/PyFunceble_config.yaml",
            "iana": "https://example.org/iana-db.json",
        }

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        given_local["links"].update(uneeded_links)

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_wrong_user_agent(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we still have the old user agent format.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        given_local["user_agent"] = "Hello, World!"

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_3_x_http_codes(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we still have some of the old http_codes indexes.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        given_local["http_codes"]["active"] = True
        given_local["http_codes"]["not_found_default"] = "XXXX"

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_3_x_dns_over_tcp(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we still have the old dns_over_tcp index.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        given_local["dns_lookup_over_tcp"] = True

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        expected["dns"]["protocol"] = "TCP"
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_3_x_cooldown_time(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we still have the old cooldown_time index.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        # Just to trigger the merge.
        given_local["http_codes"]["not_found_default"] = "XXXX"

        given_local["cli_testing"]["cooldown_time"] = None

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_3_x_json2csv(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we still have the old db type index.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        # Just to trigger the merge.
        given_local["http_codes"]["not_found_default"] = "XXXX"

        given_local["cli_testing"]["db_type"] = "json"

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_3_x_old_to_new(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we want to convert old keys to the new layout.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        # Just to trigger the merge.
        given_local["http_codes"]["not_found_default"] = "XXXX"

        given_local["adblock"] = True

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        expected["cli_decoding"]["adblock"] = True
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_3_x_old_to_new_nagated(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that we want to convert old keys to the new layout.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        # Just to trigger the merge.
        given_local["http_codes"]["not_found_default"] = "XXXX"

        given_local["no_special"] = True

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        expected["lookup"]["special"] = False
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_http_code_not_self_managed(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that the end-user is not managing the status code.
        """

        given_local = copy.deepcopy(self.our_config)
        given_upstream = copy.deepcopy(self.our_config)

        # Just to trigger the merge.
        given_local["http_codes"]["list"]["up"] = copy.deepcopy(
            self.our_config["http_codes"]["list"]["up"]
        )

        # Assume end-user added this before getting away from self management.
        given_local["http_codes"]["list"]["up"].append(403)

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_empty_local(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that the given local configuration is empty -- which should
        never happens.
        """

        given_local = dict()  # pylint: disable=use-dict-literal
        given_upstream = copy.deepcopy(self.our_config)

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )

        expected = self.our_config
        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_nested_old2new(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that one of the given migration path is nested.
        """

        given_local = {
            "cli_decoding": {"aggressive_test": False}
        }  # pylint: disable=use-dict-literal
        given_upstream = copy.deepcopy(self.our_config)
        given_upstream["cli_decoding"]["aggressive_world"] = True

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )
        config_comparison.OLD_TO_NEW = {
            "cli_decoding.aggressive_test": "cli_decoding.aggressive_world"
        }
        config_comparison.OLD_TO_NEW_NEGATE = {}

        expected = self.our_config
        expected["cli_decoding"]["aggressive_world"] = False

        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)

    def test_get_merged_nested_old2newnegate(self) -> None:
        """
        Tests the method which let us get the (clean) merged configuration
        for the case that one of the given migration path is nested and negated.
        """

        given_local = {
            "cli_decoding": {"aggressive_test": False}
        }  # pylint: disable=use-dict-literal
        given_upstream = copy.deepcopy(self.our_config)
        given_upstream["cli_decoding"]["aggressive_world"] = True

        config_comparison = ConfigComparison(
            local_config=given_local, upstream_config=given_upstream
        )
        config_comparison.OLD_TO_NEW = {}
        config_comparison.OLD_TO_NEW_NEGATE = {
            "cli_decoding.aggressive_test": "cli_decoding.aggressive_world"
        }

        expected = self.our_config
        expected["cli_decoding"]["aggressive_world"] = True

        actual = config_comparison.get_merged()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
