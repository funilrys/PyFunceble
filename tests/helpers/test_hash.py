"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the hash helper.

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

import tempfile
import unittest

from PyFunceble.helpers.hash import HashHelper


class TestHashHelper(unittest.TestCase):
    """
    Tests our hash helpers.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.hashing_subject = ["Hello World!", "Thanks for using PyFunceble"]

        self.hashing_table = {
            "md5": "ba2e0e1774c2e60e2327f263402facd4",
            "sha1": "b5c8520cd2c422019997dc6fdbc9cb9d7002356e",
            "sha224": "863c46d5ed52b439da8f62a791e77c0cbbfb7d92af7c5549279f580d",
            "sha384": "6492f4b5732e0af4b9edf2c29ee4622c62ee418e5d6e0f34b13cb80560a28256c6e21e949119872d26d2327fc112a63b",  # pylint: disable=line-too-long
            "sha512": "f193ad6ee2cfbecd580225d8e6bfb9df1910e5ca6135b21b03ae208a007f71e9b57b55e299d27157551a18ef4dfdde23c96aaea796064846edc6cd25ac7eaf7f",  # pylint: disable=line-too-long
            "sha512_224": "7c43867047942e9d441f5e3e29ad63ad579bc038bf9eba925ff6896b",
        }

    def tearDown(self) -> None:
        """
        Destroys everything which was setup for the tests.
        """

        del self.hashing_table
        del self.hashing_subject

    def test_set_algo_return(self) -> None:
        """
        Tests the response from the method which let us set the algoritm to
        work with.
        """

        given = "SHA512_224"

        hash_helper = HashHelper()
        actual = hash_helper.set_algo(given)

        self.assertIsInstance(actual, HashHelper)

    def test_set_algo(self) -> None:
        """
        Tests the method which let us set the algorithm to work with.
        """

        given = "SHA512_224"
        expected = "SHA512_224"

        hash_helper = HashHelper()
        hash_helper.set_algo(given)

        actual = hash_helper.algo

        self.assertEqual(expected, actual)

        hash_helper = HashHelper(given)

        actual = hash_helper.algo

        self.assertEqual(expected, actual)

    def test_set_algo_not_str(self) -> None:
        """
        Tests the method which let us set the the algorithm to work with.
        """

        given = ["Hello", "World"]

        hash_helper = HashHelper()

        self.assertRaises(TypeError, lambda: hash_helper.set_algo(given))

    def test_set_algo_not_valid(self) -> None:
        """
        Tests the method which let us set the the algorithm to work with.
        """

        given = "Hello"

        hash_helper = HashHelper()

        self.assertRaises(ValueError, lambda: hash_helper.set_algo(given))

    def test_hash_data(self) -> None:
        """
        Tests the method which let us get the hash of a given data.
        """

        given = "\n".join(self.hashing_subject)

        hash_helper = HashHelper()

        for algo, expected in self.hashing_table.items():
            actual = hash_helper.set_algo(algo).hash_data(given)

            self.assertEqual(expected, actual)

            actual = hash_helper.hash_data(given.encode())

            self.assertEqual(expected, actual)

    def test_hash_data_wrong_type(self) -> None:
        """
        Tests the method which let us get the hash of a given data for the case
        that the given data is not a bytes nor a string.
        """

        given = 0
        hash_helper = HashHelper()

        self.assertRaises(TypeError, lambda: hash_helper.hash_data(given))

    def test_hash_file(self) -> None:
        """
        Tests the method which let us hash the content of a given file.
        """

        our_file = tempfile.NamedTemporaryFile(delete=False)

        our_file.write("\n".join(self.hashing_subject).encode())
        our_file.seek(0)

        hash_helper = HashHelper()

        for algo, expected in self.hashing_table.items():
            actual = hash_helper.set_algo(algo).hash_file(our_file.name)

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
