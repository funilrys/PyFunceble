"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the RPZ Policy 2 subject converter.

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

from PyFunceble.converter.rpz_policy2subject import RPZPolicy2Subject

try:
    import pyf_test_dataset
    import pyf_test_helpers
except ModuleNotFoundError:  # pragma: no cover
    from .. import pyf_test_dataset, pyf_test_helpers


class TestRPZPolicy2Subject(unittest.TestCase):
    """
    Tests of our RPZ Policy 2 subject converter.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = RPZPolicy2Subject()

    def tearDown(self) -> None:
        """
        Destroys everything previously created for the tests.
        """

        del self.converter

    def test_remove_marker(self) -> None:
        """
        Tests the method which let us remove everything up to a given marker.
        """

        given = "example.org.rpz-nsdname"
        given_marker = ".rpz-nsdname"
        expected = "example.org"

        actual = self.converter.remove_marker(given, given_marker)

        self.assertEqual(expected, actual)

    def test_remove_not_marker(self) -> None:
        """
        Tests the method which let us remove everything up to a given marker
        for the case that the given marker does not exists in the givne subject.
        """

        given = "example.org"
        given_marker = ".rpz-nsdname"
        expected = "example.org"

        actual = self.converter.remove_marker(given, given_marker)

        self.assertEqual(expected, actual)

    def test_get_matching_cleanup_marker(self) -> None:
        """
        Tests the method which let us get the cleanup marker that matches the
        in the given subject.
        """

        given = "example.org.rpz-nsdname"
        expected = ".rpz-nsdname"

        actual = self.converter.get_matching_cleanup_marker(given)

        self.assertEqual(expected, actual)

    def test_get_not_matching_cleanup_marker(self) -> None:
        """
        Tests the method which let us get the cleanup marker that matches the
        in the given subject for the case that no marker can be found in the
        given string.
        """

        given = "example.org.rpz-funilrys"
        expected = None

        actual = self.converter.get_matching_cleanup_marker(given)

        self.assertEqual(expected, actual)

    def test_get_matching_ip_marker(self) -> None:
        """
        Tests the method which let us get the ip marker that matches the
        in the given subject.
        """

        given_map = {
            ".rpz-client-ip": "example.org.rpz-client-ip",
            ".rpz-ip": "example.org.rpz-ip",
            ".rpz-nsip": "example.org.rpz-nsip",
        }

        for expected, given in given_map.items():
            actual = self.converter.get_matching_ip_marker(given)

            self.assertEqual(expected, actual)

    def test_get_not_matching_ip_marker(self) -> None:
        """
        Tests the method which let us get the ip marker that matches the
        in the given subject for the case that no marker can be found in the
        given string.
        """

        given = "example.org.rpz-ip-funilrys"
        expected = None

        actual = self.converter.get_matching_ip_marker(given)

        self.assertEqual(expected, actual)

    def test_get_subject_from_ip_marker_with_ipv4(self) -> None:
        """
        Tests the method which let us get the real subject from the given
        ip marker.
        """

        for given_ip in pyf_test_dataset.VALID_IPV4:
            marker = ".rpz-client-ip"
            given = f"{pyf_test_helpers.convert_ipv4_to_rpz(given_ip)}{marker}"

            expected = given_ip

            actual = self.converter.get_subject_from_ip_marker(given, marker)

            self.assertEqual(expected, actual)

    def test_get_subject_from_ip_marker_with_ipv6(self) -> None:
        """
        Tests the method which let us get the real subject from the given
        ip marker.
        """

        for given_ip in pyf_test_dataset.VALID_IPV6:
            marker = ".rpz-client-ips"
            given = f"{pyf_test_helpers.convert_ipv6_to_rpz(given_ip)}{marker}"

            expected = given_ip

            actual = self.converter.get_subject_from_ip_marker(given, marker)

            self.assertEqual(expected, actual)

    def test_get_converted_simple_domain(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a simple domain is given.
        """

        given = "example.org"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_comment(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a simple domain is given.
        """

        given = "; Hello, World"
        expected = None

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_simple_commented_domain(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a simple but commented domain is given.
        """

        given = "example.org. ; Hello, World!"
        expected = "example.org."

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_wildcard(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a wildcard domain is given.
        """

        given = "*.example.org"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_nsdname(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a subjec with the :code:`.rpz-nsdname` policy is given.
        """

        given = "example.org.rpz-nsdname"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_wildcard_nsdname(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a wildcard subjec with the :code:`.rpz-nsdname` policy is given.
        """

        given = "*.example.org.rpz-nsdname"
        expected = "example.org"

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_rpz_ip_ipv4(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a wildcard subjec with the :code:`.rpz-ip` policy is given.
        """

        given = (
            f"{pyf_test_helpers.convert_ipv4_to_rpz(pyf_test_dataset.VALID_IPV4[0])}"
            ".rpz-ip"
        )
        expected = pyf_test_dataset.VALID_IPV4[0]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_rpz_ip_ipv6(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a wildcard subjec with the :code:`.rpz-ip` policy is given.
        """

        given = (
            f"{pyf_test_helpers.convert_ipv6_to_rpz(pyf_test_dataset.VALID_IPV6[0])}"
            ".rpz-ip"
        )
        expected = pyf_test_dataset.VALID_IPV6[0]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_set_soa_return(self) -> None:
        """
        Tests the response from the method which let us set the SOA to work with.
        """

        given = "example.com."

        actual = self.converter.set_soa(given)

        self.assertIsInstance(actual, RPZPolicy2Subject)

    def test_set_soa_method(self) -> None:
        """
        Tests the method which let us set the SOA to work with.
        """

        given = "example.com."
        expected = "example.com."

        self.converter.set_soa(given)

        actual = self.converter.soa

        self.assertEqual(expected, actual)
        self.assertTrue(given in self.converter.soas)

    def test_set_soa_attribute(self) -> None:
        """
        Tests overwritting of the :code:`soa` attribute.
        """

        given = "example.com."
        expected = "example.com."

        self.converter.soa = given
        actual = self.converter.soa

        self.assertEqual(expected, actual)
        self.assertTrue(given in self.converter.soas)

    def test_set_soa_no_str(self) -> None:
        """
        Tests overwritting of the :code:`soa` attribute.

        In this test we test the case that we give a non-string value.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.converter.set_soa(given))

    def test_set_soa_empty_str(self) -> None:
        """
        Tests overwritting of the :code:`soa` attribute.

        In this test we test the case that we give an empty string value.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.converter.set_soa(given))

    def test_set_soa_through_init(self) -> None:
        """
        Tests the overwritting of the SOA to work with through the class
        constructor.
        """

        given = "example.com."
        expected = "example.com."

        converter = RPZPolicy2Subject(soa=given)
        actual = converter.soa

        self.assertEqual(expected, actual)
        self.assertTrue(given in converter.soas)

    def test_set_soas_return(self) -> None:
        """
        Tests the response from the method which let us set the SOAs to work with.
        """

        given = ["example.com."]

        actual = self.converter.set_soas(given)

        self.assertIsInstance(actual, RPZPolicy2Subject)

    def test_set_soas_method(self) -> None:
        """
        Tests the method which let us set the SOA to work with.
        """

        given = ["example.com."]
        expected = ["example.com."]

        self.converter.set_soas(given)

        actual = self.converter.soas

        self.assertEqual(expected, actual)

    def test_set_soas_attribute(self) -> None:
        """
        Tests overwritting of the :code:`soas` attribute.
        """

        given = ["example.com."]
        expected = ["example.com."]

        self.converter.soas = given
        actual = self.converter.soas

        self.assertEqual(expected, actual)

    def test_set_soas_no_list(self) -> None:
        """
        Tests overwritting of the :code:`soas` attribute.

        In this test we test the case that we give a non-list value.
        """

        given = "Hello, World!"

        self.assertRaises(TypeError, lambda: self.converter.set_soas(given))

    def test_set_soas_non_list_of_str(self) -> None:
        """
        Tests overwritting of the :code:`soas` attribute.

        In this test we test the case that we give a non string value.
        """

        given = [".example.org.", None, ".example.net."]

        self.assertRaises(ValueError, lambda: self.converter.set_soas(given))

    def test_set_soas_through_init(self) -> None:
        """
        Tests the overwritting of the SOA to work with through the class
        constructor.
        """

        given = ["example.com."]
        expected = ["example.com."]

        converter = RPZPolicy2Subject(soas=given)
        actual = converter.soas

        self.assertEqual(expected, actual)

    def test_get_converted_soa(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        a subjec with the SOA given.
        """

        given = "example.org.example.net"
        given_soa = "example.net"
        expected = "example.org"

        self.converter.data_to_convert = given
        self.converter.soa = given_soa
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
