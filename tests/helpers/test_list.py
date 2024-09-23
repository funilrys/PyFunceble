"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our list helper.

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
import unittest

from PyFunceble.helpers.list import ListHelper


class TestListHelper(unittest.TestCase):
    """
    Provides the test of our dictionnary helper.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.helper = ListHelper()

        self.mixed_test_subject = [
            ("Hello", "World"),
            "Hello",
            {"hello": "world"},
            "World",
            1,
            4.5,
            None,
            "",
        ]

        self.str_test_subject = [
            "hello",
            "world",
            "",
            "!",
            " ",
            "hello",
            "world!",
            "Hello",
        ]

    def tearDown(self) -> None:
        """
        Destroy everything needed by the tests.
        """

        del self.mixed_test_subject
        del self.str_test_subject

    def test_set_subject_return(self) -> None:
        """
        Tests the response from the method which let us set the subject to work
        with.
        """

        actual = self.helper.set_subject(self.mixed_test_subject)

        self.assertIsInstance(actual, ListHelper)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = self.mixed_test_subject
        expected = list(self.mixed_test_subject)

        self.helper.set_subject(given)

        actual = self.helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_attribute(self) -> None:
        """
        Tests overwritting of the :code:`subject` attribute.
        """

        given = self.mixed_test_subject
        expected = list(self.mixed_test_subject)

        self.helper.subject = given
        actual = self.helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_through_init(self) -> None:
        """
        Tests the overwritting of the subject to work through the class
        constructor.
        """

        given = self.mixed_test_subject
        expected = given

        helper = ListHelper(given)
        actual = helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_not_list(self) -> None:
        """
        Tests the response of the method which let us set the subject for the
        case that the given subject is not a list.
        """

        given = {"Hello": "World"}

        self.assertRaises(TypeError, lambda: self.helper.set_subject(given))

    def test_remove_empty(self) -> None:
        """
        Tests the method which let us remove the empty strings from a given
        list.
        """

        given = copy.deepcopy(self.str_test_subject)

        expected = ["hello", "world", "!", " ", "hello", "world!", "Hello"]
        actual = self.helper.set_subject(given).remove_empty().subject

        self.assertEqual(expected, actual)

        given = copy.deepcopy(self.mixed_test_subject)

        expected = [
            ("Hello", "World"),
            "Hello",
            {"hello": "world"},
            "World",
            1,
            4.5,
            None,
        ]
        actual = self.helper.set_subject(given).remove_empty().subject

        self.assertEqual(expected, actual)

    def test_remove_duplicates(self) -> None:
        """
        Tests the method which let us remove the duplicates from a given list.
        """

        given = copy.deepcopy(self.str_test_subject)

        expected = ["hello", "world", "", "!", " ", "world!", "Hello"]
        actual = self.helper.set_subject(given).remove_duplicates().subject

        self.assertEqual(expected, actual)

    def test_sort(self) -> None:
        """
        Tests the method which let us sort a given list.
        """

        given = copy.deepcopy(self.str_test_subject)

        expected = [
            "",
            " ",
            "!",
            "hello",
            "hello",
            "Hello",
            "world",
            "world!",
        ]
        actual = self.helper.set_subject(given).sort().subject

        self.assertEqual(expected, actual)

    def test_sort_reverse(self) -> None:
        """
        Tests the method which let us sort a given list.
        """

        given = copy.deepcopy(self.str_test_subject)

        expected = ["world!", "world", "hello", "hello", "Hello", "!", " ", ""]
        actual = self.helper.set_subject(given).sort(reverse=True).subject

        self.assertEqual(expected, actual)

    def test_custom_sort(self) -> None:
        """
        Tests the method which let us sort a given list with a custom method.
        """

        given = copy.deepcopy(self.str_test_subject)

        expected = ["", " ", "!", "world!", "world", "hello", "hello", "Hello"]
        actual = (
            self.helper.set_subject(given)
            .custom_sort(lambda x: x[-1] if x else x)
            .subject
        )

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
