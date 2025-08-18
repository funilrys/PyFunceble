"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the user agent dataset interaction.

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

import copy
import json
import tempfile
import unittest
import unittest.mock

from PyFunceble.config.loader import ConfigLoader
from PyFunceble.dataset.base import DatasetBase
from PyFunceble.dataset.user_agent import UserAgentDataset


class TestUserAgentDataset(unittest.TestCase):
    """
    Tests the user agent dataset interaction.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.config_loader = ConfigLoader()

        self.tempfile = tempfile.NamedTemporaryFile()
        self.modern_tempfile = tempfile.NamedTemporaryFile()

        self.our_dataset = {
            "@modern": {
                "chrome": {
                    "linux": [
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/77.0.3865.116 "
                        "Safari/537.36 Edg/77.11.4.5118"
                    ],
                    "macosx": [
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4364.0 "
                        "Safari/537.36"
                    ],
                    "win10": [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4361.0 "
                        "Safari/537.36"
                    ],
                },
                "edge": {
                    "linux": [],
                    "macosx": [],
                    "win10": [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 "
                        "Safari/537.36 Edge/18.17763/5.9.7 (Linux;Android 10) "
                        "ExoPlayerLib/2.9.6"
                    ],
                },
                "firefox": {
                    "linux": [
                        "Mozilla/5.0 (Linux x86_64; en-US) Gecko/20130401 "
                        "Firefox/82.4"
                    ],
                    "macosx": [
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0; "
                        "en-US) Gecko/20100101 Firefox/74.7"
                    ],
                    "win10": [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) "
                        "Gecko/20100101 Firefox/84.0/8mqDiPuL-36"
                    ],
                },
                "ie": {
                    "linux": [],
                    "macosx": [],
                    "win10": [
                        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; "
                        "Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR "
                        "2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet "
                        "PC 2.0; wbx 1.0.0; wbxapp 1.0.0)"
                    ],
                },
                "opera": {
                    "linux": [
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 "
                        "OPR/73.0.3856.284"
                    ],
                    "macosx": [
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 "
                        "Safari/537.36 OPR/72.0.3815.400"
                    ],
                    "win10": [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 "
                        "Safari/537.36 OPR/73.0.3856.284 (Edition avira-2)"
                    ],
                },
                "safari": {
                    "linux": [
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 "
                        "Safari/537.36 SputnikBrowser/1.2.5.158"
                    ],
                    "macosx": [
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) "
                        "AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.0.3 "
                        "Safari/601.4.4"
                    ],
                    "win10": [],
                },
            },
            "chrome": {
                "linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/77.0.3865.116 "
                "Safari/537.36 Edg/77.11.4.5118",
                "macosx": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4364.0 "
                "Safari/537.36",
                "win10": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4361.0 "
                "Safari/537.36",
            },
            "edge": {
                "linux": None,
                "macosx": None,
                "win10": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 "
                "Safari/537.36 Edge/18.17763/5.9.7 (Linux;Android 10) "
                "ExoPlayerLib/2.9.6",
            },
            "firefox": {
                "linux": "Mozilla/5.0 (Linux x86_64; en-US) Gecko/20130401 "
                "Firefox/82.4",
                "macosx": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0; "
                "en-US) Gecko/20100101 Firefox/74.7",
                "win10": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) "
                "Gecko/20100101 Firefox/84.0/8mqDiPuL-36",
            },
            "ie": {
                "linux": None,
                "macosx": None,
                "win10": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; "
                "Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR "
                "2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet "
                "PC 2.0; wbx 1.0.0; wbxapp 1.0.0)",
            },
            "opera": {
                "linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 "
                "OPR/73.0.3856.284",
                "macosx": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 "
                "Safari/537.36 OPR/72.0.3815.400",
                "win10": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 "
                "Safari/537.36 OPR/73.0.3856.284 (Edition avira-2)",
            },
            "safari": {
                "linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 "
                "Safari/537.36 SputnikBrowser/1.2.5.158",
                "macosx": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) "
                "AppleWebKit/600.8.9 (KHTML, like Gecko) Version/9.0.3 "
                "Safari/601.4.4",
                "win10": None,
            },
        }

        self.tempfile.write(json.dumps(self.our_dataset).encode())
        self.tempfile.seek(0)

        self.user_agent_dataset = UserAgentDataset()
        self.user_agent_dataset.source_file = self.tempfile.name

        self.get_content_patch = unittest.mock.patch.object(DatasetBase, "get_content")
        self.mock_get_content = self.get_content_patch.start()
        self.mock_get_content.return_value = copy.deepcopy(self.our_dataset)

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        self.get_content_patch.stop()
        del self.mock_get_content
        del self.tempfile
        del self.our_dataset
        del self.config_loader
        del self.user_agent_dataset

    def test_contains(self) -> None:
        """
        Tests of the method which let us check if a given browser is into the
        dataset.
        """

        given = "chrome"
        expected = True

        actual = given in self.user_agent_dataset

        self.assertEqual(expected, actual)

    def test_not_contains(self) -> None:
        """
        Tests the method which let us check if a given platform is into the
        dataset.
        """

        given = "vivaldi"
        expected = False

        actual = given in self.user_agent_dataset

        self.assertEqual(expected, actual)

    def test_get_all_from_browser(self) -> None:
        """
        Tests the way to get every information of a given browser.
        """

        given = "chrome"
        expected = copy.deepcopy(self.our_dataset["@modern"][given])

        actual = self.user_agent_dataset[given]

        self.assertEqual(expected, actual)

    def test_get_all_from_unknown_browser(self) -> None:
        """
        Tests the way to get every information of a given browser.

        In this test, we try to get from something that does not exists.
        """

        given = "vivaldi"
        expected = dict()  # pylint: disable=use-dict-literal

        actual = self.user_agent_dataset[given]

        self.assertEqual(expected, actual)

    def test_is_supported_browser(self) -> None:
        """
        Tests the method which let us check if a browser is supported.
        """

        given = "chrome"
        expected = True

        actual = self.user_agent_dataset.is_supported_browser(given)

        self.assertEqual(expected, actual)

    def test_is_not_supported_browser(self) -> None:
        """
        Tests teh method which let us check if a browser is supported for the
        case that the given browser is not supported.
        """

        given = "vivaldi"
        expected = False

        actual = self.user_agent_dataset.is_supported_browser(given)

        self.assertEqual(expected, actual)

    def test_is_supported_browser_not_str(self) -> None:
        """
        Tests the method which let us check if a browser is supported for the
        case the given browser not is not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(
            TypeError, lambda: self.user_agent_dataset.is_supported_browser(given)
        )

    def test_is_supported(self) -> None:
        """
        Tests the method which let us check if a browser and platform is
        supported.
        """

        given_browser = "chrome"
        given_platform = "linux"
        expected = True

        actual = self.user_agent_dataset.is_supported(given_browser, given_platform)

        self.assertEqual(expected, actual)

    def test_is_supported_not_str_browser(self) -> None:
        """
        Tests the method which let us check if a browser and platform is
        supported.

        In this test, we check the case that the given browser is not a string.
        """

        given_browser = ["Hello", "World"]
        given_platform = "linux"

        self.assertRaises(
            TypeError,
            lambda: self.user_agent_dataset.is_supported(given_browser, given_platform),
        )

    def test_is_supported_not_str_platform(self) -> None:
        """
        Tests the method which let us check if a browser and platform is
        supported.

        In this test, we check the case that the given platform is not a string.
        """

        given_browser = "chrome"
        given_platform = ["Hello", "Worl"]

        self.assertRaises(
            TypeError,
            lambda: self.user_agent_dataset.is_supported(given_browser, given_platform),
        )

    def test_is_supported_unknown_browser(self) -> None:
        """
        Tests the method which let us check if a browser and platform is
        supported.

        In this test, we check the case that the given browser is not known.
        """

        given_browser = "vivaldi"
        given_platform = "linux"
        expected = False

        actual = self.user_agent_dataset.is_supported(given_browser, given_platform)

        self.assertEqual(expected, actual)

    def test_is_supported_unknown_platform(self) -> None:
        """
        Tests the method which let us check if a browser and platform is
        supported.

        In this test, we check the case that the given platform is not known.
        """

        given_browser = "chrome"
        given_platform = "bsd"
        expected = False

        actual = self.user_agent_dataset.is_supported(given_browser, given_platform)

        self.assertEqual(expected, actual)

    def test_is_supported_unknown_platform_and_browser(self) -> None:
        """
        Tests the method which let us check if a browser and platform is
        supported.

        In this test, we check the case that the given platform and browser
        are not known.
        """

        given_browser = "vivaldi"
        given_platform = "bsd"
        expected = False

        actual = self.user_agent_dataset.is_supported(given_browser, given_platform)

        self.assertEqual(expected, actual)

    def test_set_preferred(self) -> None:
        """
        Tests the method which let us set our preferred browser and platform.
        """

        given_browser = "chrome"
        given_platform = "win10"

        actual = self.user_agent_dataset.set_preferred(given_browser, given_platform)

        self.assertIsInstance(actual, UserAgentDataset)

        expected_platform = "win10"
        expected_browser = "chrome"
        actual_platform = self.user_agent_dataset.preferred_platform
        actual_browser = self.user_agent_dataset.preferred_browser

        self.assertEqual(expected_platform, actual_platform)
        self.assertEqual(expected_browser, actual_browser)

    def test_set_preferred_not_supported(self) -> None:
        """
        Tests the method which let us set our preferred browser and platform.

        In this test, we check that an exception is correctly raised when
        the platform or browser is not supported.
        """

        given_browser = "vivaldi"
        given_platform = "win10"

        self.assertRaises(
            ValueError,
            lambda: self.user_agent_dataset.set_preferred(
                given_browser, given_platform
            ),
        )

        given_browser = "vivaldi"
        given_platform = "bsd"

        self.assertRaises(
            ValueError,
            lambda: self.user_agent_dataset.set_preferred(
                given_browser, given_platform
            ),
        )

    def test_get_latest(self) -> None:
        """
        Tests the method which let us get the latest user agent known.
        """

        given_browser = "chrome"
        given_platform = "win10"

        expected = self.our_dataset[given_browser][given_platform]

        self.user_agent_dataset.set_preferred(given_browser, given_platform)

        actual = self.user_agent_dataset.get_latest()

        self.assertEqual(expected, actual)

    def test_get_latest_from_config(self) -> None:
        """
        Tests the method which let us get the latest user agent known based
        on the settings from the configuration file.
        """

        given_browser = "firefox"
        given_platform = "win10"

        self.config_loader.custom_config = {
            "user_agent": {"platform": given_platform, "browser": given_browser}
        }
        self.config_loader.start()

        expected = self.our_dataset[given_browser][given_platform]

        actual = self.user_agent_dataset.get_latest()

        self.assertEqual(expected, actual)

    def test_get_latest_from_config_with_reference(self) -> None:
        """
        Tests the method which let us get the latest user agent known based
        on the settings from the configuration file.

        We also ensure that the reference is correctly appended.
        """

        given_browser = "firefox"
        given_platform = "win10"
        given_reference = "https://example.org"

        self.config_loader.custom_config = {
            "user_agent": {
                "platform": given_platform,
                "browser": given_browser,
                "reference": given_reference,
            }
        }
        self.config_loader.start()

        expected = (
            self.our_dataset[given_browser][given_platform] + "; +" + given_reference
        )

        actual = self.user_agent_dataset.get_latest()

        self.assertEqual(expected, actual)

    def test_get_latest_from_config_custom(self) -> None:
        """
        Tests the method which let us get the latest user agent known based
        on the settings from the configuration file.
        """

        self.config_loader.custom_config = {"user_agent": {"custom": "Hello, World!"}}
        self.config_loader.start()

        expected = "Hello, World!"

        actual = self.user_agent_dataset.get_latest()

        self.assertEqual(expected, actual)

    def test_get_latest_from_custom_config_with_reference(self) -> None:
        """
        Tests the method which let us get the latest user agent known based
        on the settings from the configuration file.

        In this test, we check the case that the given reference is set.
        """

        self.config_loader.custom_config = {
            "user_agent": {
                "custom": "Hello, World!",
                "reference": "https://example.org",
            }
        }
        self.config_loader.start()

        expected = "Hello, World!; +https://example.org"

        actual = self.user_agent_dataset.get_latest()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
