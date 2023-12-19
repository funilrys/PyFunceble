"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our our netinfo base class.

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

import unittest
import unittest.mock

from PyFunceble.query.netinfo.base import NetInfoBase


class TestNetInfobase(unittest.TestCase):
    """
    Tests the of the base of all out netinfo classes.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.interface = NetInfoBase()

    def tearDown(self) -> None:
        """
        Destroys everything previously initiated.
        """

        del self.interface

    def test_set_subject_return(self) -> None:
        """
        Tests the response from the method which let us set the subject to
        work with.
        """

        given = "example.com"

        actual = self.interface.set_subject(given)

        self.assertIsInstance(actual, NetInfoBase)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = "example.com"
        expected = "example.com"

        self.interface.set_subject(given)

        actual = self.interface.subject

        self.assertEqual(expected, actual)

    def test_set_subject_not_str(self) -> None:
        """
        Tests the method which let us set the subject to work with for the case
        that a non string value is given.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.interface.set_subject(given))

    def test_set_subject_empty_str(self) -> None:
        """
        Tests the method which let us set the subject to work with for the case
        that an empty string is given
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.interface.set_subject(given))

    def test_set_subject_attribute(self) -> None:
        """
        Tests overwritting of the :code:`subject` attribute.
        """

        given = "example.com"
        expected = "example.com"

        self.interface.subject = given
        actual = self.interface.subject

        self.assertEqual(expected, actual)

    def test_set_subject_through_init(self) -> None:
        """
        Tests the overwritting of the subject to work through the class
        constructor.
        """

        given = "example.com"
        expected = "example.com"

        interface = NetInfoBase(given)
        actual = interface.subject

        self.assertEqual(expected, actual)

    def test_get_info_no_subject_given(self) -> None:
        """
        Tests the method which let us get the information we are looking for;
        for the case that no subject is given.
        """

        # pylint: disable=unnecessary-lambda
        self.assertRaises(TypeError, lambda: self.interface.get_info())

    def test_get_info(self) -> None:
        """
        Tests the method which let us get the information we are looking for.
        """

        given = "example.com"

        self.interface.subject = given

        # pylint: disable=unnecessary-lambda
        self.assertRaises(NotImplementedError, lambda: self.interface.get_info())


if __name__ == "__main__":
    unittest.main()
