"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the merging helper.

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

import unittest

from PyFunceble.helpers.merge import Merge


class TestMerge(unittest.TestCase):
    """
    Tests our merging helper.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.helper = Merge()

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.helper

    def test_set_subject_return(self) -> None:
        """
        Tests the response from the method which let us set the subject to work
        with.
        """

        actual = self.helper.set_subject("This is an example.")

        self.assertIsInstance(actual, Merge)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "This is an example."
        expected = given

        self.helper.set_subject(given)

        actual = self.helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_attribute(self) -> None:
        """
        Tests overwritting of the :code:`subject` attribute.
        """

        given = "This is another example."
        expected = given

        self.helper.subject = given
        actual = self.helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_through_init(self) -> None:
        """
        Tests the overwritting of the subject to work through the class
        constructor.
        """

        given = "This is a strange example."
        expected = given

        helper = Merge(given)
        actual = helper.subject

        self.assertEqual(expected, actual)

    def test_merge_str(self) -> None:
        """
        Tests the method which let us merge 2 objects for the case that 2
        strings are given.
        """

        given = "Hello"
        expected = "Hello"
        actual = self.helper.set_subject(given).into("World")

        self.assertEqual(expected, actual)

    def test_merge_int(self) -> None:
        """
        Tests the method which let us merge 2 objects for the case that 2
        integers are given.
        """

        given = 2
        expected = 2
        actual = self.helper.set_subject(given).into(1)

        self.assertEqual(expected, actual)

    def test_merge_float(self) -> None:
        """
        Tests the method which let us merge 2 objects for the case that 2
        floats are given.
        """

        given = 2.1
        expected = 2.1
        actual = self.helper.set_subject(given).into(3.1)

        self.assertEqual(expected, actual)

    def test_strict_simple_dict(self) -> None:
        """
        Tests the case that we want to strictly merge 2 simple dict.
        """

        given = {
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
            "hello": ["This is PyFunceble!", "Uhh!"],
        }
        to_merge = {
            "hello_world": {"author": "nobody", "surname": "body"},
            "hello": ["hello", "Uhh"],
        }
        expected = {
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
            "world": "Fun Ilrys",
            "hello": ["hello", "Uhh"],
        }
        actual = self.helper.set_subject(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

    def test_not_strict_simple_dict(self) -> None:
        """
        Tests the case that we want to merge 2 simple dicts.
        """

        given = {
            "hello": ["This is PyFunceble!", "Uhh!"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
        }
        to_merge = {
            "hello": ["hello", "Uhh"],
            "hello_world": {"author": "nobody", "surname": "body"},
        }
        expected = {
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
            "hello": ["This is PyFunceble!", "Uhh!", "hello", "Uhh"],
        }

        actual = self.helper.set_subject(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

    def test_strict_dict(self) -> None:
        """
        Tests the case that we want to strictly merge 2 dicts.
        """

        given = {
            "hello": {"world": ["This is PyFunceble!", "Uhh!"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
        }
        to_merge = {
            "hello": {"world": ["hello", "Uhh!"]},
            "hello_world": {"author": "nobody", "surname": "body"},
        }
        expected = {
            "hello": {"world": ["hello", "Uhh!"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }

        actual = self.helper.set_subject(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

    def test_not_strict_dict(self) -> None:
        """
        Tests the case that we want to merge 2 dicts.
        """

        given = {
            "hello": {"world": ["This is PyFunceble!", "Uhh!"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
        }
        to_merge = {
            "hello": {"world": ["hello", "Uhh!"]},
            "hello_world": {"author": "nobody", "surname": "body"},
        }
        expected = {
            "hello": {"world": ["This is PyFunceble!", "Uhh!", "hello"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }

        actual = self.helper.set_subject(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

    def test_strict_simple_list(self) -> None:
        """
        Tests the case that we want to strictly merge 2 simple lists.
        """

        given = [1, 2, 3, 4]
        to_merge = [2, 4, 5, 6, 7]

        expected = [2, 4, 5, 6, 7]
        actual = self.helper.set_subject(to_merge).into(given, strict=True)

        self.assertEqual(actual, expected)

    def test_not_strict_simple_list(self) -> None:
        """
        Tests the case that we want to merge 2 simple lists.
        """

        given = [1, 2, 3, 4]
        to_merge = [2, 4, 5, 6, 7]

        expected = [1, 2, 3, 4, 5, 6, 7]
        actual = self.helper.set_subject(to_merge).into(given, strict=False)

        self.assertEqual(actual, expected)

    def test_strict_list(self) -> None:
        """
        Tests the case that we want to strictly merge 2 lists.
        """

        given = ["hello", "world", 5, {"hello": "world"}, [1, 2, 3]]
        to_merge = ["hello", "world", 5, {"world": "hello"}, [4, 5]]
        expected = ["hello", "world", 5, {"hello": "world", "world": "hello"}, [4, 5]]

        actual = self.helper.set_subject(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]

        actual = self.helper.set_subject(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]

        actual = self.helper.set_subject(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

    def test_not_strict_list(self) -> None:
        """
        Tests the case that we want to merge 2 lists.
        """

        given = ["hello", "world", 5, {"hello": "world"}, [1, 2, 3]]
        to_merge = ["hello", "world", 5, {"world": "hello"}, [4, 5]]
        expected = [
            "hello",
            "world",
            5,
            {"hello": "world"},
            [1, 2, 3],
            {"world": "hello"},
            [4, 5],
        ]

        actual = self.helper.set_subject(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = [
            "hello",
            "world",
            5,
            {"hello": "world"},
            [1, 2, 3],
            {"hello": "you!"},
            [1, 2, 4, 5],
        ]

        actual = self.helper.set_subject(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = [
            "hello",
            "world",
            5,
            {"hello": "world"},
            [1, 2, 3],
            {"hello": "you!"},
            [1, 2, 4, 5],
        ]

        actual = self.helper.set_subject(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

    def test_mixed_str_int(self) -> None:
        """
        Tests the case that we want to merge a str into an int.
        """

        expected = "Hello"
        actual = self.helper.set_subject("Hello").into(1)

        self.assertEqual(expected, actual)

    def test_mixed_int_float(self) -> None:
        """
        Tests the case that we want to merge an int into a float.
        """

        expected = 1
        actual = self.helper.set_subject(1).into(2.1)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
