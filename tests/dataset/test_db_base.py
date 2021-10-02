"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the base of all our database dataset.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/latest/

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
import unittest.mock
from typing import Generator, Optional

from PyFunceble.dataset.db_base import DBDatasetBase


class TestDBDatasetBase(unittest.TestCase):
    """
    Tests the base of all database dataset.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.dataset = DBDatasetBase()

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.dataset

    def test_set_authorized_return(self) -> None:
        """
        Tests the response from the method which let us set the authorization
        to operate.
        """

        given = True

        actual = self.dataset.set_authorized(given)

        self.assertIsInstance(actual, DBDatasetBase)

    def test_set_authorized_method(self) -> None:
        """
        Tests the method which let us set the authorization to operate.
        """

        given = True
        expected = True

        self.dataset.set_authorized(given)

        actual = self.dataset.authorized

        self.assertEqual(expected, actual)

    def test_set_authorized_attribute(self) -> None:
        """
        Tests overwritting of the :code:`authorized` attribute.
        """

        given = True
        expected = True

        self.dataset.authorized = given
        actual = self.dataset.authorized

        self.assertEqual(expected, actual)

    def test_set_authorized_through_init(self) -> None:
        """
        Tests the overwritting of the authorization to operate through the
        class constructor.
        """

        given = True
        expected = True

        dataset = DBDatasetBase(authorized=given)
        actual = dataset.authorized

        self.assertEqual(expected, actual)

    def test_set_authorized_no_string(self) -> None:
        """
        Tests the method which let us set the authorization to operate for the
        case that the given value is not a boolean.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.dataset.set_authorized(given))

    def test_set_remove_unneeded_fields_return(self) -> None:
        """
        Tests the response from the method which let us authorize the
        deletion of unneeded fields
        """

        given = True

        actual = self.dataset.set_remove_unneeded_fields(given)

        self.assertIsInstance(actual, DBDatasetBase)

    def test_set_remove_unneeded_fields_method(self) -> None:
        """
        Tests the method which let us authorize the deletion of unneeded fields.
        """

        given = True
        expected = True

        self.dataset.set_remove_unneeded_fields(given)

        actual = self.dataset.remove_unneeded_fields

        self.assertEqual(expected, actual)

    def test_set_remove_unneeded_fields_attribute(self) -> None:
        """
        Tests overwritting of the :code:`remove_unneeded_fields` attribute.
        """

        given = True
        expected = True

        self.dataset.remove_unneeded_fields = given
        actual = self.dataset.remove_unneeded_fields

        self.assertEqual(expected, actual)

    def test_set_remove_unneeded_fields_through_init(self) -> None:
        """
        Tests the overwritting of the :code:`remove_unneeded_fields` attribute
        through the class constructor.
        """

        given = True
        expected = True

        dataset = DBDatasetBase(remove_unneeded_fields=given)
        actual = dataset.remove_unneeded_fields

        self.assertEqual(expected, actual)

    def test_set_remove_unneeded_fields_no_string(self) -> None:
        """
        Tests the method which let us authorizes the deletion of unneeded fields
        for the case that the given value is not a boolean.
        """

        given = ["Hello", "World"]

        self.assertRaises(
            TypeError, lambda: self.dataset.set_remove_unneeded_fields(given)
        )

    def test_get_filtered_row(self) -> None:
        """
        Tests the method which let us filter a given row to the only minimum.
        """

        self.dataset.authorized = True
        self.dataset.FIELDS = ["hello", "world", "fun", "state"]
        self.dataset.COMPARISON_FIELDS = ["hello"]

        given = {
            "my_key": "key_my",
            "world": "hello",
            "fun": "ilrys",
            "state": "sleeping",
            "sleeping": None,
        }
        expected = {"hello": "", "world": "hello", "state": "sleeping", "fun": "ilrys"}

        actual = self.dataset.get_filtered_row(given)

        self.assertEqual(expected, actual)

    def test_get_filtered_row_not_authorized(self) -> None:
        """
        Tests the method which let us filter a given row to the only minimum.

        In this case we check what should happen when the dataset interface
        is not authorized to operate.
        """

        self.dataset.authorized = False
        self.dataset.FIELDS = ["hello", "world", "fun", "state"]
        self.dataset.COMPARISON_FIELDS = ["hello"]

        given = {
            "my_key": "key_my",
            "world": "hello",
            "fun": "ilrys",
            "state": "sleeping",
            "sleeping": None,
        }
        expected = {}

        actual = self.dataset.get_filtered_row(given)

        self.assertEqual(expected, actual)

    def test_get_filtered_content(self) -> None:
        """
        Tests the method which let us get a filter content.
        """

        def our_get_content() -> Generator[Optional[dict], None, None]:
            """
            Provides our very own content provider.
            """

            dataset = [
                {"user": "funilrys", "state": "sleeping"},
                {"user": "fun.ilrys", "state": "coding"},
                {"user": "ilrys.fun", "state": "eating"},
                {"user": "anonymous", "state": "coding"},
                {"user": "foo.bar", "state": "sleeping"},
                {"user": "bar.foo", "state": "coding"},
            ]

            for data in dataset:
                yield data

        self.dataset.authorized = True

        with unittest.mock.patch.object(
            DBDatasetBase, "get_content"
        ) as get_content_patch:
            get_content_patch.return_value = our_get_content()

            to_filter = {"state": "coding"}
            expected = [
                {"user": "fun.ilrys", "state": "coding"},
                {"user": "anonymous", "state": "coding"},
                {"user": "bar.foo", "state": "coding"},
            ]

            actual = list(self.dataset.get_filtered_content(to_filter))

            self.assertEqual(expected, actual)

        # Now we test the case that we give a key that is not into the dataset.
        with unittest.mock.patch.object(
            DBDatasetBase, "get_content"
        ) as get_content_patch:
            get_content_patch.return_value = our_get_content()

            to_filter = {"sleeping": True}
            expected = []

            actual = list(self.dataset.get_filtered_content(to_filter))

            self.assertEqual(expected, actual)

    def test_get_filtered_content_not_dict(self) -> None:
        """
        Tests the method which let us get a filter content for the case that
        the given filter is not a :py:class:`dict`.
        """

        self.dataset.authorized = True

        to_filter = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: list(self.dataset.get_filtered_content(to_filter))
        )


if __name__ == "__main__":
    unittest.main()
