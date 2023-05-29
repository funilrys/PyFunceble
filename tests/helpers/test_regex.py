"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the regex helper.

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

from PyFunceble.helpers.regex import RegexHelper


class TestRegexHelper(unittest.TestCase):
    """
    Tests our regex helper.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the test.
        """

        self.helper = RegexHelper()

        self.test_regex = "[a-z]"
        self.testing_list_subject = [
            "hello",
            "world",
            "funilrys",
            "funceble",
            "PyFunceble",
            "pyfunceble",
        ]
        self.testing_subject = "Hello, this is Fun Ilrys. I just wanted to know how things goes around the tests."  # pylint: disable=line-too-long

    def tearDown(self) -> None:
        """
        Destroys everything previously initialized for the tests.
        """

        del self.testing_list_subject
        del self.testing_subject

    def test_set_regex_return(self) -> None:
        """
        Tests the response from the method which let us set the regex to work
        with.
        """

        actual = self.helper.set_regex(self.test_regex)

        self.assertIsInstance(actual, RegexHelper)

    def test_set_regex_method(self) -> None:
        """
        Tests the method which let us set the regex to work with.
        """

        given = self.test_regex
        expected = given

        self.helper.set_regex(given)

        actual = self.helper.regex

        self.assertEqual(expected, actual)

    def test_set_regex_attribute(self) -> None:
        """
        Tests overwritting of the :code:`regex` attribute.
        """

        given = self.test_regex
        expected = given

        self.helper.regex = given
        actual = self.helper.regex

        self.assertEqual(expected, actual)

    def test_set_regex_through_init(self) -> None:
        """
        Tests the overwritting of the regex to work through the class
        constructor.
        """

        given = self.test_regex
        expected = given

        helper = RegexHelper(given)
        actual = helper.regex

        self.assertEqual(expected, actual)

    def test_set_regex_not_str(self) -> None:
        """
        Tests the method which let us set the regex to work with for the case
        that it's not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.helper.set_regex(given))

    def test_set_regex_escape(self) -> None:
        """
        Tests the method which let us set the regex to work with for the case
        that it's not a string.
        """

        regex_helper = RegexHelper()
        regex_helper.escape_regex = True
        regex_helper.set_regex("[a-z]")

        expected = r"\[a\-z\]"
        actual = regex_helper.regex

        self.assertEqual(expected, actual)

    def test_not_matching_list(self) -> None:
        """
        Tests the method which let us get a list of non
        matching strin from a given list of string.
        """

        regex = "fun"
        expected = ["hello", "world", "PyFunceble"]
        actual = self.helper.set_regex(regex).get_not_matching_list(
            self.testing_list_subject
        )

        self.assertEqual(expected, actual)

    def test_matching_list(self) -> None:
        """
        Tests the method which let us get a list of
        matchint string from a given list of string.
        """

        regex = "fun"
        expected = ["funilrys", "funceble", "pyfunceble"]
        actual = self.helper.set_regex(regex).get_matching_list(
            self.testing_list_subject
        )

        self.assertEqual(expected, actual)

    def test_match_check(self) -> None:
        """
        Tests the matching method for the case that we want to just check.
        """

        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = True
        actual = self.helper.set_regex(regex).match(
            self.testing_subject, return_match=False
        )

        self.assertEqual(expected, actual)

    def test_match_not_check(self) -> None:
        """
        Tests the matching method for the case that we want to just check.
        """

        regex = r"@funilrys"
        expected = False
        actual = self.helper.set_regex(regex).match(
            self.testing_subject, return_match=False
        )

        self.assertEqual(expected, actual)

    def test_match_rematch(self) -> None:
        """
        Tests the matching method for the case that we want to rematch
        the different groups.
        """

        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = "is"
        actual = self.helper.set_regex(regex).match(
            self.testing_subject, rematch=True, group=1
        )

        self.assertEqual(expected, actual)

    def test_match_get_group(self) -> None:
        """
        Tests the matching method for the case that we want
        a specific group.
        """

        regex = "e"
        expected = "e"
        actual = self.helper.set_regex(regex).match(self.testing_subject, group=0)

        self.assertEqual(expected, actual)

        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = "this"
        actual = self.helper.set_regex(regex).match(self.testing_subject, group=1)

        self.assertEqual(expected, actual)

    def test_replace_no_replacement(self) -> None:
        """
        Tests the replacement method for the case that no replacement
        is not given.
        """

        regex = "th"
        expected = self.testing_subject
        actual = self.helper.set_regex(regex).replace_match(self.testing_subject, None)

        self.assertEqual(expected, actual)

    def test_replace(self) -> None:
        """
        Tests the replacement method.
        """

        regex = "th"
        expected = (
            "Hello, htis is Fun Ilrys. I just wanted to know how "
            "htings goes around hte tests."
        )
        actual = self.helper.set_regex(regex).replace_match(self.testing_subject, "ht")

        self.assertEqual(expected, actual)

    def test_split(self) -> None:
        """
        Tests the method which le us split occurences of a given regex.
        """

        regex = "th"
        expected = [
            "Hello, ",
            "is is Fun Ilrys. I just wanted to know how ",
            "ings goes around ",
            "e tests.",
        ]
        actual = self.helper.set_regex(regex).split(self.testing_subject)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
