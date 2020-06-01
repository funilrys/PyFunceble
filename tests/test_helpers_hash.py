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

Tests of the PyFunceble.helpers.hash

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
# pylint: enable=line-too-long

from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.helpers import File, Hash


class TestHash(TestCase):
    """
    Tests of the PyFunceble.helpers.hash.
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        self.file = "this_file_should_be_deleted"
        self.data_to_write = ["Hello World!", "Thanks for using PyFunceble"]

        self.expected_hashed = {
            "md5": "ba2e0e1774c2e60e2327f263402facd4",
            "sha1": "b5c8520cd2c422019997dc6fdbc9cb9d7002356e",
            "sha224": "863c46d5ed52b439da8f62a791e77c0cbbfb7d92af7c5549279f580d",
            "sha384": "6492f4b5732e0af4b9edf2c29ee4622c62ee418e5d6e0f34b13cb80560a28256c6e21e949119872d26d2327fc112a63b",  # pylint: disable=line-too-long
            "sha512": "f193ad6ee2cfbecd580225d8e6bfb9df1910e5ca6135b21b03ae208a007f71e9b57b55e299d27157551a18ef4dfdde23c96aaea796064846edc6cd25ac7eaf7f",  # pylint: disable=line-too-long
            "sha512_224": "7c43867047942e9d441f5e3e29ad63ad579bc038bf9eba925ff6896b",
        }

    def test_hash_data_not_string_nor_bytes(self):
        """
        Tests the method which let us hash a given data for the case
        that we given a non string or bytes input.
        """

        given = [1, 2, 3, 4]

        self.assertRaises(ValueError, lambda: Hash().data(given))

    def test_hash_unknown_algo(self):
        """
        Tests the hash class for the case that we give an unknown algo.
        """

        given = "\n".join(self.data_to_write)

        self.assertRaises(ValueError, lambda: Hash(algo="Hello, World!").data(given))

    def test_hash_data(self):
        """
        Tests the method wich let us hash a given data.
        """

        given = "\n".join(self.data_to_write)

        for algo, expected in self.expected_hashed.items():
            self.assertEqual(expected, Hash(algo=algo).data(given))
            self.assertEqual(expected, Hash(algo=algo).data(given.encode()))

    def test_hash_file_not_exists(self):
        """
        Tests the method which let us the content of a given file.
        """

        file_instance = File(self.file)

        file_instance.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        expected = None
        for algo in self.expected_hashed:
            self.assertEqual(
                expected, Hash(algo=algo).file(self.file),
            )

    def test_hash_file(self):
        """
        Tests the method which let us the content of a given file.
        """

        file_instance = File(self.file)

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        file_instance.write("\n".join(self.data_to_write))

        expected = True
        actual = file_instance.exists()

        self.assertEqual(expected, actual)

        for algo, expected in self.expected_hashed.items():
            self.assertEqual(
                expected, Hash(algo=algo).file(self.file),
            )

        file_instance.delete()

        expected = False
        actual = file_instance.exists()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
