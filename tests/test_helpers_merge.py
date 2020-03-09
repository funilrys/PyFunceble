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

Tests of PyFunceble.helpers.merge

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.helpers.merge import Merge


class TestMerge(TestCase):
    """
    Tests of PyFunceble.helpers.merge
    """

    def test_str(self):
        """
        Tests the case that we want to merge 2 strs.
        """

        expected = "Hello"
        actual = Merge("Hello").into("World")

        self.assertEqual(expected, actual)

    def test_int(self):
        """
        Tests the case that we want to merge 2 ints.
        """

        expected = 2
        actual = Merge(2).into(1)

        self.assertEqual(expected, actual)

    def test_float(self):
        """
        Tests the case that we want to merge 2 floats.
        """

        expected = 2.1
        actual = Merge(2.1).into(3.1)

        self.assertEqual(expected, actual)

    def test_strict_simple_dict(self):
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
        actual = Merge(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

    def test_not_strict_simple_dict(self):
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

        actual = Merge(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

    def test_strict_dict(self):
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

        actual = Merge(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

    def test_not_strict_dict(self):
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

        actual = Merge(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

    def test_strict_simple_list(self):
        """
        Tests the case that we want to strictly merge 2 simple lists.
        """

        given = [1, 2, 3, 4]
        to_merge = [2, 4, 5, 6, 7]

        expected = [2, 4, 5, 6, 7]
        actual = Merge(to_merge).into(given, strict=True)

        self.assertEqual(actual, expected)

    def test_not_strict_simple_list(self):
        """
        Tests the case that we want to merge 2 simple lists.
        """

        given = [1, 2, 3, 4]
        to_merge = [2, 4, 5, 6, 7]

        expected = [1, 2, 3, 4, 5, 6, 7]
        actual = Merge(to_merge).into(given, strict=False)

        self.assertEqual(actual, expected)

    def test_strict_list(self):
        """
        Tests the case that we want to strictly merge 2 lists.
        """

        given = ["hello", "world", 5, {"hello": "world"}, [1, 2, 3]]
        to_merge = ["hello", "world", 5, {"world": "hello"}, [4, 5]]
        expected = ["hello", "world", 5, {"hello": "world", "world": "hello"}, [4, 5]]

        actual = Merge(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]

        actual = Merge(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]

        actual = Merge(to_merge).into(given, strict=True)

        self.assertEqual(expected, actual)

    def test_not_strict_list(self):
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

        actual = Merge(to_merge).into(given, strict=False)

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

        actual = Merge(to_merge).into(given, strict=False)

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

        actual = Merge(to_merge).into(given, strict=False)

        self.assertEqual(expected, actual)

    def test_mixed_str_int(self):
        """
        Tests the case that we want to merge a str into an int.
        """

        expected = "Hello"
        actual = Merge("Hello").into(1)

        self.assertEqual(expected, actual)

    def test_mixed_int_float(self):
        """
        Tests the case that we want to merge an int into a float.
        """

        expected = 1
        actual = Merge(1).into(2.1)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
