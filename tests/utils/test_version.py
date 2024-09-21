"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our version utility.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

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

from PyFunceble.utils.version import VersionUtility


class TestVersionUtility(unittest.TestCase):
    """
    Tests our version utility.
    """

    def setUp(self) -> None:
        """
        Setups everything needed.
        """

        self.utility = VersionUtility()

    def tearDown(self) -> None:
        """
        Destroys everything that was needed.
        """

        del self.utility

    def test_set_local_version_return(self) -> None:
        """
        Tests the response from the method which let us set the data to work with.
        """

        given = "example.com"

        actual = self.utility.set_local_version(given)

        self.assertIsInstance(actual, VersionUtility)

    def test_set_local_version_method(self) -> None:
        """
        Tests the method which let us set the data to work with.
        """

        given = "1.0.0.dev (Hello, World)"
        expected = "1.0.0.dev (Hello, World)"

        self.utility.set_local_version(given)

        actual = self.utility.local_version

        self.assertEqual(expected, actual)

    def test_set_local_version_attribute(self) -> None:
        """
        Tests overwritting of the :code:`local_version` attribute.
        """

        given = "1.0.0.dev (Hello, World)"
        expected = "1.0.0.dev (Hello, World)"

        self.utility.local_version = given
        actual = self.utility.local_version

        self.assertEqual(expected, actual)

    def test_set_local_version_through_init(self) -> None:
        """
        Tests the overwritting of the data to work through the class constructor.
        """

        given = "1.0.0.dev (Hello, World)"
        expected = "1.0.0.dev (Hello, World)"

        utility = VersionUtility(given)
        actual = utility.local_version

        self.assertEqual(expected, actual)

    def test_set_local_version_not_str(self) -> None:
        """
        Tests the method which let us set the version to work with for the case
        that it's not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.utility.set_local_version(given))

    def test_get_splitted(self) -> None:
        """
        Tests the method which let us split the version from it's code name.
        """

        given = "1.0.0.dev (Hello, World)"
        expected = (["1", "0", "0"], "dev (Hello, World)")

        actual = self.utility.get_splitted(given)

        self.assertEqual(expected, actual)

    def test_get_splitted_alpha(self) -> None:
        """
        Tests the method which let us split the version from it's code name
        for the case that we follow PEP440.
        """

        given = "1.0.0a1.dev (Hello, World)"
        expected = (["1", "0", "0a1"], "dev (Hello, World)")

        actual = self.utility.get_splitted(given)

        self.assertEqual(expected, actual)

    def test_get_splitted_alpha_no_code_name(self) -> None:
        """
        Tests the method which let us split the version from it's code name
        for the case that we follow PEP440.

        In this case we don't give any code name.
        """

        given = "1.0.0a1"
        expected = (["1", "0", "0a1"], "")

        actual = self.utility.get_splitted(given)

        self.assertEqual(expected, actual)

    def test_literally_compare(self) -> None:
        """
        Tests the method which let us literally compare 2 versions.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.literally_compare(given_upstream)

        self.assertEqual(expected, actual)

    def test_literally_compare_not_equal(self) -> None:
        """
        Tests the method which let us literally compare 2 versions for the case
        that the 2 versions differs.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a2.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.literally_compare(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_than(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a2.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_than_release_candidate(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one - which is a release candidate.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0rc1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_than_huge_number(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we give huge numbers as local version.
        """

        given_local = "1.0.0a40.dev (Hello, World)"
        given_upstream = "1.0.0a2.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_almost_same(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare a10 agains a1.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a10.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent_beta(self) -> None:
        """
        Tests the method which let us check if the local version is recent
        than the given one.

        In this case we compare the beta against the alpha.
        """

        given_local = "1.0.0b10.dev (Hello, World)"
        given_upstream = "1.0.0a20.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_beta(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare the alpha against the beta.
        """

        given_local = "1.0.0a40.dev (Hello, World)"
        given_upstream = "1.0.0b2.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent_alpha(self) -> None:
        """
        Tests the method which let us check if the local version is recent
        than the given one.

        In this case we compare the beta against the alpha.
        """

        given_local = "1.0.0a40.dev (Hello, World)"
        given_upstream = "1.0.0b1.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent_almost_same(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare a10 agains a1.
        """

        given_local = "1.0.0a10.dev (Hello, World)"
        given_upstream = "1.0.0a1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_alpha(self) -> None:
        """
        Tests the method which let us check if the local version is recent
        than the given one.

        In this case we compare the alpha against the beta.
        """

        given_local = "1.0.0a40.dev (Hello, World)"
        given_upstream = "1.0.0b2.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_equal_beta(self) -> None:
        """
        Tests the method which let us check if the local version is equal
        to the given one.

        In this case we compare the beta against the beta.
        """

        given_local = "1.0.0b1.dev (Hello, World)"
        given_upstream = "1.0.0b1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_equal_to(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_equal_almost_same(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare a10 agains a1.
        """

        given_local = "1.0.0a10.dev (Hello, World)"
        given_upstream = "1.0.0a1.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_equal_to(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_alpha_non_beta(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare the alpha against a non alpha version.
        """

        given_local = "1.0.1a1.dev (Hello, World)"
        given_upstream = "1.0.1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_non_beta_alpha(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare the non alpha against the alpha.
        """

        given_local = "1.0.1.dev (Hello, World)"
        given_upstream = "1.0.1a1.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent_alpha_non_beta(self) -> None:
        """
        Tests the method which let us check if the local version is recent
        than the given one.

        In this case we compare the alpha against a non alpha version.
        """

        given_local = "1.0.1a1.dev (Hello, World)"
        given_upstream = "1.0.1.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent_alpha_non_beta_4_x_to_3_x(self) -> None:
        """
        Tests the method which let us check if the local version is recent
        than the given one.

        In this case we compare the alpha against a non alpha version.
        """

        given_local = "4.0.0a1.dev (Hello, World)"
        given_upstream = "3.2.3.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_older_alpha_non_beta_4_x_to_3_x(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one.

        In this case we compare the alpha against a non alpha version.
        """

        given_local = "4.0.0a1.dev (Hello, World)"
        given_upstream = "3.2.2.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent_non_beta_alpha(self) -> None:
        """
        Tests the method which let us check if the local version is recent
        than the given one.

        In this case we compare the non alpha against the alpha.
        """

        given_local = "1.0.1.dev (Hello, World)"
        given_upstream = "1.0.1a1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_not_older_than(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one for the case that the given version is actualy not
        older.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a0.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_not_older_than_equal(self) -> None:
        """
        Tests the method which let us check if the local version is older
        than the given one for the case that the given version is actualy not
        older but equal.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a1.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_older_than(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_equal_to(self) -> None:
        """
        Tests the method which let us check if the local version is equal to
        the given one.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_equal_to(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_not_equal_to(self) -> None:
        """
        Tests the method which let us check if the local version is equal to
        the given one for the case that the given version is not equal..
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a0.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_equal_to(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_not_equal_to_recent(self) -> None:
        """
        Tests the method which let us check if the local version is equal to
        the given one.
        """

        given_local = "1.0.0a1.dev (Hello, World)"
        given_upstream = "1.0.0a2.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_equal_to(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_recent(self) -> None:
        """
        Tests the method which let us check if the local version is more recent
        than the given one.
        """

        given_local = "1.0.0a2.dev (Hello, World)"
        given_upstream = "1.0.0a1.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_not_recent(self) -> None:
        """
        Tests the method which let us check if the local version is more recent
        than the given one.
        """

        given_local = "1.0.0a2.dev (Hello, World)"
        given_upstream = "1.0.0a3.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_not_recent_recent(self) -> None:
        """
        Tests the method which let us check if the local version is more recent
        than the given one.
        """

        given_local = "1.0.0a2.dev (Hello, World)"
        given_upstream = "1.0.0a2.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_recent(given_upstream)

        self.assertEqual(expected, actual)

    def test_is_dev(self) -> None:
        """
        Tests the method which let us check if the given version is the dev one.
        """

        given_local = "1.0.0a2.dev (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_dev()

        self.assertEqual(expected, actual)

    def test_is_not_dev(self) -> None:
        """
        Tests the method which let us check if the given version is the dev one
        for the case that the given version is not a dev one.
        """

        given_local = "1.0.0a2.internal (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_dev()

        self.assertEqual(expected, actual)

    def test_is_master(self) -> None:
        """
        Tests the method which let us check if the given version is the master
        one.
        """

        given_local = "1.0.0a2. (Hello, World)"

        expected = True

        self.utility.local_version = given_local
        actual = self.utility.is_master()

        self.assertEqual(expected, actual)

    def test_is_not_master(self) -> None:
        """
        Tests the method which let us check if the given version is the master
        one for the case that the given version is not a master one.
        """

        given_local = "1.0.0a2.dev (Hello, World)"

        expected = False

        self.utility.local_version = given_local
        actual = self.utility.is_master()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
