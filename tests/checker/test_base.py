"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our checker base.

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

import unittest

from PyFunceble.checker.base import CheckerBase, CheckerStatusBase


class TestCheckerBase(unittest.TestCase):
    """
    Tests of the base of all our checker.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.checker = CheckerBase()

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        del self.checker

    def test_set_subject_return(self) -> None:
        """
        Tests the response of the method which let us set the subject to work
        with.
        """

        given = "example.org"

        actual = self.checker.set_subject(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "example.org"
        expected = "example.org"

        self.checker.set_subject(given)

        actual = self.checker.subject

        self.assertEqual(expected, actual)

    def test_set_subject_idna(self) -> None:
        """
        Tests the initilization of the :code:`idna_subject` attribute when
        we overwrite the subject.
        """

        given = "äxample.org"
        expected_subject = "äxample.org"
        expected_idna_subject = "xn--xample-9ta.org"

        self.checker.subject = given

        actual_subject = expected_subject
        actual_idna_subject = expected_idna_subject

        self.assertEqual(expected_subject, actual_subject)
        self.assertEqual(expected_idna_subject, actual_idna_subject)

    def test_set_subject_idna_url(self) -> None:
        """
        Tests the initilization of the :code:`idna_subject` attribute when
        we overwrite the subject.

        In this case we check the conversion when a URL is given.
        """

        given = "http://äxample.org/?is_admin=true"
        expected_subject = "http://äxample.org/?is_admin=true"
        expected_idna_subject = "http://xn--xample-9ta.org/?is_admin=true"

        self.checker.subject = given

        actual_subject = expected_subject
        actual_idna_subject = expected_idna_subject

        self.assertEqual(expected_subject, actual_subject)
        self.assertEqual(expected_idna_subject, actual_idna_subject)

    def test_set_subject_through_init(self) -> None:
        """
        Tests the overwritting of the subjct through the class constructor.
        """

        given = "example.org"
        expected = "example.org"

        checker = CheckerBase(given)

        actual = checker.subject

        self.assertEqual(expected, actual)

    def test_set_subject_not_str(self) -> None:
        """
        Tests the case that we want to set a non-string subject.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_subject(given))

    def test_set_subject_empty_str(self) -> None:
        """
        Tests the case that we want to set an empty string as subject.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.checker.set_subject(given))

    def test_set_idna_subject(self) -> None:
        """
        Tests the case that we want to overwrite the :code:`idna_subject`
        attribute.
        """

        given = "xn--xample-9ta.org"
        expected = "xn--xample-9ta.org"

        self.checker.idna_subject = given

        actual = self.checker.idna_subject

        self.assertEqual(expected, actual)

    def test_set_idna_subject_method(self) -> None:
        """
        Tests the method that let us overwrite the :code:`idna_subject`
        attribute.
        """

        given = "xn--xample-9ta.org"
        expected = "xn--xample-9ta.org"

        actual = self.checker.set_idna_subject(given)

        self.assertIsInstance(actual, CheckerBase)

        actual = self.checker.idna_subject

        self.assertEqual(expected, actual)

    def test_set_idna_subject_not_str(self) -> None:
        """
        Tests the case that we want to overwrite the :code:`idna_subject`
        attribute with a non-string value.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.checker.set_idna_subject(given))

    def test_set_idna_subject_empty_str(self) -> None:
        """
        Tests the case that we want to overwrite the :code:`idna_subject`
        attribute with an empty string value.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.checker.set_idna_subject(given))

    def test_set_do_syntax_check_first_return(self) -> None:
        """
        Tests the response of the method which let us define that we want the
        syntax to be tested first.
        """

        given = True

        actual = self.checker.set_do_syntax_check_first(given)

        self.assertIsInstance(actual, CheckerBase)

    def test_set_do_syntax_check_first_method(self) -> None:
        """
        Tests the method which let us define that we want the
        syntax to be tested first.
        """

        given = False
        expected = False

        self.checker.set_do_syntax_check_first(given)

        actual = self.checker.do_syntax_check_first

        self.assertEqual(expected, actual)

    def test_set_do_syntax_check_first_init(self) -> None:
        """
        Tests the definition of the :code:`do_syntax_check_first` attribute
        through the class constructor.
        """

        given = True
        expected = True

        checker = CheckerBase(do_syntax_check_first=given)

        actual = checker.do_syntax_check_first

        self.assertEqual(expected, actual)

    def test_set_do_syntax_check_first_not_bool(self) -> None:
        """
        Tests the case that we want to overwrite the
        :code:`do_syntax_check_first` attribute with a non-boolean value.
        """

        given = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: self.checker.set_do_syntax_check_first(given)
        )

    def test_get_status(self) -> None:
        """
        Tests the method which let us get the status.
        """

        given = "example.org"

        # This is an abstract method. So we need to define it.
        self.checker.query_status = lambda: None

        self.checker.subject = given

        actual = self.checker.get_status()

        self.assertIsInstance(actual, CheckerStatusBase)


if __name__ == "__main__":
    unittest.main()
