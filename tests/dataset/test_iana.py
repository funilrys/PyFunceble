"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of iana dataset interaction.

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

from PyFunceble.dataset.base import DatasetBase
from PyFunceble.dataset.iana import IanaDataset


class TestIanaDataset(unittest.TestCase):
    """
    Tests the iana dataset interaction.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.tempfile = tempfile.NamedTemporaryFile()

        self.our_dataset = {
            "aaa": "whois.nic.aaa",
            "aarp": "whois.nic.aarp",
            "abarth": "whois.afilias-srs.net",
            "abb": "whois.nic.abb",
            "abbott": "whois.afilias-srs.net",
            "abbvie": "whois.afilias-srs.net",
            "abc": "whois.nic.abc",
            "able": "whois.nic.able",
            "abogado": "whois.nic.abogado",
            "abudhabi": "whois.nic.abudhabi",
            "ac": "whois.nic.ac",
        }

        self.tempfile.write(json.dumps(self.our_dataset).encode())
        self.tempfile.seek(0)

        self.iana_dataset = IanaDataset()
        self.iana_dataset.source_file = self.tempfile.name

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
        del self.iana_dataset

    def test_contains(self) -> None:
        """
        Tests of the method which let us check if a given extension is into the
        dataset.
        """

        given = "aaa"

        expected = True
        actual = given in self.iana_dataset

        self.assertEqual(expected, actual)

    def test_contains_extension_starts_with_point(self) -> None:
        """
        Tests of the method which let us check if a given extension is into the
        dataset for the case that the extension starts with a point.
        """

        given = ".aaa"

        expected = True
        actual = given in self.iana_dataset

        self.assertEqual(expected, actual)

    def test_does_not_contain(self) -> None:
        """
        Tests of the method which let us check if a given extension is into the
        dataset.
        """

        given = "com"

        expected = False
        actual = given in self.iana_dataset

        self.assertEqual(expected, actual)

    def test_getitem(self) -> None:
        """
        Tests the method which let us (indirectly) get the whois server.
        """

        expected = "whois.nic.aarp"
        actual = self.iana_dataset["aarp"]

        self.assertEqual(expected, actual)

    def test_getitem_extension_starts_with_point(self) -> None:
        """
        Tests the method which let us (indirectly) get the whois server.
        """

        expected = "whois.nic.aarp"
        actual = self.iana_dataset[".aarp"]

        self.assertEqual(expected, actual)

    def test_getitem_not_exist(self) -> None:
        """
        Tests the method which let us (indirectly) get the whois server for
        the case that the given extension does not exists.
        """

        expected = None
        actual = self.iana_dataset["hehehe"]

        self.assertEqual(expected, actual)

    def test_getattr(self) -> None:
        """
        Tests the method which let us (indirectly) get the whois server.
        """

        expected = "whois.nic.aarp"
        actual = self.iana_dataset.aarp

        self.assertEqual(expected, actual)

    def test_getattr_not_exist(self) -> None:
        """
        Tests the method which let us (indirectly) get the whois server for
        the case that the given extension does not exists.
        """

        expected = None
        actual = self.iana_dataset.hehehe

        self.assertEqual(expected, actual)

    def test_is_extension(self) -> None:
        """
        Tests the method which let us check if the given extension is known.
        """

        expected = True
        actual = self.iana_dataset.is_extension("aarp")

        self.assertEqual(expected, actual)

    def test_is_not_extension(self) -> None:
        """
        Tests the method which let us check if the given extension is known for
        the case tha the given extension does not exists.
        """

        expected = False
        actual = self.iana_dataset.is_extension("heheh")

        self.assertEqual(expected, actual)

    def test_is_extension_not_str(self) -> None:
        """
        Tests the method which let us check if the given extension is known for
        the case that the given extension
        """

        self.assertRaises(TypeError, lambda: self.iana_dataset.is_extension(["test"]))

    def test_get_whois_server(self) -> None:
        """
        Tests the method which let us get the whois server of a given extension.
        """

        expected = "whois.nic.aarp"
        actual = self.iana_dataset.get_whois_server("aarp")

        self.assertEqual(expected, actual)

    def test_get_whois_server_not_extension(self) -> None:
        """
        Tests the method which let us get the whois server of a given extension
        for the case that the given extension is not known.
        """

        expected = None
        actual = self.iana_dataset.get_whois_server("hehehehehe")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
