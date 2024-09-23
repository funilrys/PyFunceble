"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of public suffic dataset interaction.

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

from PyFunceble.dataset.base import DatasetBase
from PyFunceble.dataset.public_suffix import PublicSuffixDataset


class TestPublicSuffixDataset(unittest.TestCase):
    """
    Tests the public suffix dataset interaction.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.tempfile = tempfile.NamedTemporaryFile()

        self.our_dataset = {
            "ac": ["com.ac", "edu.ac", "gov.ac", "mil.ac", "net.ac", "org.ac"],
            "academy": ["official.academy"],
            "ad": ["nom.ad"],
        }

        self.tempfile.write(json.dumps(self.our_dataset).encode())
        self.tempfile.seek(0)

        self.ps_dataset = PublicSuffixDataset()
        self.ps_dataset.source_file = self.tempfile.name

        self.get_content_patch = unittest.mock.patch.object(DatasetBase, "get_content")
        self.mock_get_content = self.get_content_patch.start()
        self.mock_get_content.return_value = copy.deepcopy(self.our_dataset)

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.tempfile
        del self.our_dataset
        del self.ps_dataset

        self.get_content_patch.stop()

        del self.get_content_patch

    def test_contains(self) -> None:
        """
        Tests of the method which let us check if a given extension is into the
        dataset.
        """

        given = "ac"

        expected = True
        actual = given in self.ps_dataset

        self.assertEqual(expected, actual)

    def test_contains_extension_starts_with_point(self) -> None:
        """
        Tests of the method which let us check if a given extension is into the
        dataset for the case that the extension starts with a point.
        """

        given = ".ac"

        expected = True
        actual = given in self.ps_dataset

        self.assertEqual(expected, actual)

    def test_does_not_contain(self) -> None:
        """
        Tests of the method which let us check if a given extension is into the
        dataset.
        """

        given = "com"

        expected = False
        actual = given in self.ps_dataset

        self.assertEqual(expected, actual)

    def test_getitem(self) -> None:
        """
        Tests the method which let us (indirectly) get the available subdataset.
        """

        expected = copy.deepcopy(self.our_dataset["ad"])
        actual = self.ps_dataset["ad"]

        self.assertEqual(expected, actual)

    def test_getitem_extension_starts_with_point(self) -> None:
        """
        Tests the method which let us (indirectly) get the available subdataset.
        """

        expected = copy.deepcopy(self.our_dataset["ad"])
        actual = self.ps_dataset[".ad"]

        self.assertEqual(expected, actual)

    def test_getitem_not_exist(self) -> None:
        """
        Tests the method which let us (indirectly) get the available subdataset
        for the case that the given extension does not exists.
        """

        expected = list()  # pylint: disable=use-list-literal
        actual = self.ps_dataset["hehehe"]

        self.assertEqual(expected, actual)

    def test_getattr(self) -> None:
        """
        Tests the method which let us (indirectly) get the available subdataset.
        """

        expected = copy.deepcopy(self.our_dataset["ad"])
        actual = self.ps_dataset.ad

        self.assertEqual(expected, actual)

    def test_getattr_not_exist(self) -> None:
        """
        Tests the method which let us (indirectly) get the available subdataset
        for the case that the given extension does not exists.
        """

        expected = list()  # pylint: disable=use-list-literal
        actual = self.ps_dataset.hehehe

        self.assertEqual(expected, actual)

    def test_is_extension(self) -> None:
        """
        Tests the method which let us check if the given extension is known.
        """

        expected = True
        actual = self.ps_dataset.is_extension("ad")

        self.assertEqual(expected, actual)

    def test_is_not_extension(self) -> None:
        """
        Tests the method which let us check if the given extension is known for
        the case tha the given extension does not exists.
        """

        expected = False
        actual = self.ps_dataset.is_extension("heheh")

        self.assertEqual(expected, actual)

    def test_is_extension_not_str(self) -> None:
        """
        Tests the method which let us check if the given extension is known for
        the case that the given extension
        """

        self.assertRaises(TypeError, lambda: self.ps_dataset.is_extension(["test"]))

    def test_get_available_suffix(self) -> None:
        """
        Tests the method which let us get the available suffixes of a
        given extension.
        """

        expected = copy.deepcopy(self.our_dataset["ad"])
        actual = self.ps_dataset.get_available_suffix("ad")

        self.assertEqual(expected, actual)

    def test_get_available_suffix_not_extension(self) -> None:
        """
        Tests the method which let us get the whois server of a given extension
        for the case that the given extension is not known.
        """

        expected = list()  # pylint: disable=use-list-literal
        actual = self.ps_dataset.get_available_suffix("hehehehehe")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
