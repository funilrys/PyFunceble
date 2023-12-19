"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the base of all our dataset.

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

import tempfile
import unittest
import unittest.mock

from PyFunceble.dataset.base import DatasetBase


class TestDatasetBase(unittest.TestCase):
    """
    Tests the base of all dataset.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.tempfile = tempfile.NamedTemporaryFile()

        self.our_dataset = [
            "127.176.134.253",
            "127.34.113.192",
            "127.34.107.238",
            "127.166.193.125",
            "127.179.153.18",
            "127.89.243.30",
            "127.147.142.53",
            "127.35.150.233",
            "127.97.172.196",
            "127.24.78.18",
        ]

        self.tempfile.write("\n".join(self.our_dataset).encode())
        self.tempfile.seek(0)

        self.dataset = DatasetBase()
        self.dataset.source_file = self.tempfile.name

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.tempfile
        del self.our_dataset
        del self.dataset

    def test_get_content_not_str(self) -> None:
        """
        Tests our decorator which checks if the source file is given.

        In this test, we check the case that the given source file is not a
        string.
        """

        self.dataset.source_file = ["Hello", "World!"]

        # pylint: disable=unnecessary-lambda
        self.assertRaises(TypeError, lambda: self.dataset.get_content())

    def test_get_content_empty_str(self) -> None:
        """
        Tests our decorator which checks if the source file is given.

        In this test, we check the case that the given source file is an empty
        string.
        """

        self.dataset.source_file = ""

        # pylint: disable=unnecessary-lambda
        self.assertRaises(ValueError, lambda: self.dataset.get_content())


if __name__ == "__main__":
    unittest.main()
