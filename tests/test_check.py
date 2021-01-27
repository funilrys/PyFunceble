# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.check.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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
# pylint: enable=line-too-long
# pylint: disable=import-error

from unittest import TestCase
from unittest import main as launch_tests

import pyf_test_dataset

import PyFunceble
from PyFunceble.check import Check


class TestCheck(TestCase):
    """
    Test PyFunceble.check.Check().
    """

    # pylint: disable=too-many-public-methods

    def setUp(self):
        """
        Setup what we need for the tests.
        """

        PyFunceble.load_config(generate_directory_structure=False)

    def test_is_url(self):
        """
        Test Check.is_url() for the case that the URL is valid.
        """

        expected = True

        for domain in pyf_test_dataset.VALID_DOMAINS:
            to_test = "http://{0}/helloworld".format(domain)

            actual = Check(to_test).is_url()

            self.assertEqual(expected, actual, to_test)

            to_test = "http://{0}:8080/helloworld".format(domain)

            actual = Check(to_test).is_url()

            self.assertEqual(expected, actual)

    def test_is_url_not_valid(self):
        """
        Test Check.is_url() for the case that the URL is not valid.
        """

        expected = False

        for domain in pyf_test_dataset.NOT_VALID_DOMAINS:
            to_check = "https://{0}/hello_world".format(domain)
            actual = Check(to_check).is_url()

            self.assertEqual(expected, actual)

    def test_is_url_protocol_not_supported(self):
        """
        Test Check.is_url() for the case that the
        URL protocol is not supported nor given.
        """

        expected = False

        for domain in pyf_test_dataset.NOT_VALID_DOMAINS:
            to_check = "{0}/hello_world".format(domain)
            actual = Check(to_check).is_url()

            self.assertEqual(expected, actual)

    def test_is_url_get_base(self):
        """
        Test Check.is_url() for the case that we want to
        extract the url base.
        """

        for domain in pyf_test_dataset.VALID_DOMAINS:
            to_check = "http://{0}/hello_world".format(domain)
            expected = domain

            actual = Check(to_check).is_url(return_base=True)

            self.assertEqual(expected, actual, to_check)

    def test_is_url_get_not_base(self):
        """
        Test Check.is_url() for the case that we want to
        extract the url base for invalid domains.
        """

        expected = False
        PyFunceble.CONFIGURATION.idna_conversion = False

        for domain in pyf_test_dataset.NOT_VALID_DOMAINS:
            to_check = "http://{0}/hello_world".format(domain)

            actual = Check(to_check).is_url(return_base=True)

            self.assertEqual(expected, actual)

    def test_is_url_convert_idna(self):
        """
        Test Check().is_url() for the case that
        we have to convert to IDNA.
        """

        PyFunceble.CONFIGURATION.idna_conversion = True

        domains_to_test = {
            "bittréẋ.com": "xn--bittr-fsa6124c.com",
            "hello-world.com": "hello-world.com",
            "coinbȧse.com": "xn--coinbse-30c.com",
            "cryptopiạ.com": "xn--cryptopi-ux0d.com",
            "cṙyptopia.com": "xn--cyptopia-4e0d.com",
        }

        for domain, expected_after_conversion in domains_to_test.items():
            expected = "http://{0}/hello_world".format(expected_after_conversion)
            to_check = "http://{0}/hello_world".format(domain)

            actual = Check(to_check).is_url(return_formatted=True)

            self.assertEqual(expected, actual)

    def test_is_url_not_convert_idna(self):
        """
        Test Check().is_url() for the case that
        we do not have to convert to IDNA.
        """

        PyFunceble.CONFIGURATION.idna_conversion = False

        domains_to_test = [
            "bittréẋ.com",
            "hello-world.com",
            "coinbȧse.com",
            "cryptopiạ.com",
            "cṙyptopia.com",
        ]

        for domain in domains_to_test:
            to_check = "http://{0}/hello_world".format(domain)
            expected = to_check

            actual = Check(to_check).is_url(return_formatted=True)

            self.assertEqual(expected, actual)

    def test_is_domain(self):
        """
        Test Check().is_domain() for the case that domains
        are valid.
        """

        expected = True

        for domain in pyf_test_dataset.VALID_DOMAINS:
            to_check = domain
            actual = Check(to_check).is_domain()

            self.assertEqual(expected, actual, msg="%s is invalid." % domain)

    def test_is_domain_not_valid(self):
        """
        Test Check().is_domain() for the case that
        we meet invalid domains.
        """

        expected = False

        for domain in pyf_test_dataset.NOT_VALID_DOMAINS:
            to_check = domain
            actual = Check(to_check).is_domain()

            self.assertEqual(expected, actual, msg="%s is valid." % domain)

    def test_is_subdomain(self):
        """
        Test Check().is_subdomain() for the case subdomains
        are valid.
        """

        expected = True

        for domain in pyf_test_dataset.VALID_SUBDOMAINS:
            to_check = domain
            actual = Check(to_check).is_subdomain()

            self.assertEqual(expected, actual, msg="%s is not a subdomain." % domain)

    def test_is_subdomain_not_valid(self):
        """
        Test Check().is_subdomain() for the case subdomains
        are not valid.
        """

        expected = False

        for domain in pyf_test_dataset.NOT_VALID_SUBDOMAINS:
            to_check = domain
            actual = Check(to_check).is_subdomain()

            self.assertEqual(expected, actual, msg="%s is a subdomain." % domain)

    def test_is_ipv4(self):
        """
        Test Check().is_ipv4() for the case that the IP is valid.
        """

        expected = True

        for given_ip in pyf_test_dataset.VALID_IPV4:
            actual = Check(given_ip).is_ipv4()

            self.assertEqual(expected, actual, msg="%s is invalid." % given_ip)

    def test_is_ipv6(self):
        """
        Test Check().is_ipv6() for the case that the IP is valid.
        """

        expected = True

        for given_ip in pyf_test_dataset.VALID_IPV6:
            actual = Check(given_ip).is_ipv6()

            self.assertEqual(expected, actual, msg="%s is invalid." % given_ip)

    def test_is_ipv4_not_valid(self):
        """
        Test Check().is_ipv4() for the case that the IP
        is not valid.
        """

        expected = False

        for given_ip in pyf_test_dataset.NOT_VALID_IPV4:
            to_check = given_ip
            actual = Check(to_check).is_ipv4()

            self.assertEqual(expected, actual, msg="%s is valid." % given_ip)

    def test_is_ipv6_not_valid(self):
        """
        Test Check().is_ipv6() for the case that the IP is not valid.
        """

        expected = False

        for given_ip in pyf_test_dataset.NOT_VALID_IPV6:
            to_check = given_ip
            actual = Check(to_check).is_ipv6()

            self.assertEqual(expected, actual, msg="%s is valid." % given_ip)

    def test_is_ip_range_domain(self):
        """
        Test Check().is_ip_range() for the case that only domains are given.
        """

        expected = False
        for domain in pyf_test_dataset.VALID_DOMAINS:
            to_check = domain
            actual = Check(to_check).is_ip_range()

            self.assertEqual(expected, actual, "%s an IP range." % domain)

    def test_is_ip_range_mixed(self):
        """
        Test Check().is_ip_range()for the case that we give mixed pyf_test_dataset.
        """

        expected = True
        subjects = (
            pyf_test_dataset.VALID_IPV4_RANGES + pyf_test_dataset.VALID_IPV6_RANGES
        )

        for to_check in subjects:
            actual = Check(to_check).is_ip_range()

            self.assertEqual(expected, actual, msg="%s is not an IP range." % to_check)

    def test_is_ipv4_range(self):
        """
        Test Check().is_ipv4_range() for the case that the IP is a range.
        """

        expected = True

        for given_ip in pyf_test_dataset.VALID_IPV4_RANGES:
            to_check = given_ip
            actual = Check(to_check).is_ipv4_range()

            self.assertEqual(expected, actual, msg="%s is not an IP range." % given_ip)

    def test_is_ipv6_range(self):
        """
        Test Check().is_ipv6_range() for the case that the IP is a range.
        """

        expected = True

        for given_ip in pyf_test_dataset.VALID_IPV6_RANGES:
            to_check = given_ip
            actual = Check(to_check).is_ipv6_range()

            self.assertEqual(expected, actual, msg="%s is not an IP range." % given_ip)

    def test_is_ipv4_range_not_valid(self):
        """
        Test Check().is_ipv4_range() for the case that the IP is not a range.
        """

        expected = False

        for given_ip in pyf_test_dataset.NOT_VALID_IPV4_RANGES:
            to_check = given_ip
            actual = Check(to_check).is_ipv4_range()

            self.assertEqual(expected, actual, msg="%s is an IP range." % given_ip)

    def test_is_ipv6_range_not_valid(self):
        """
        Test Check().is_ipv6_range() for the case that the IP is not a range.
        """

        expected = False

        for given_ip in pyf_test_dataset.NOT_VALID_IPV6_RANGES:
            to_check = given_ip
            actual = Check(to_check).is_ipv6_range()

            self.assertEqual(expected, actual, msg="%s is not an IP range." % given_ip)

    def test_is_reserved_ip_domain(self):
        """
        Test Check().is_reserved_ip() for the case that domains are given.
        """

        expected = False

        for to_check in pyf_test_dataset.VALID_DOMAINS:
            actual = Check(to_check).is_reserved_ip()

            self.assertEqual(expected, actual, msg="%s is a reserved IP." % to_check)

    def test_is_reserver_ip_mixed(self):
        """
        Test Check().is_reserved_ip() for the case that mixed dataset are given.
        """

        expected = True

        subjects = pyf_test_dataset.RESERVED_IPV4 + pyf_test_dataset.RESERVED_IPV6

        for to_check in subjects:
            actual = Check(to_check).is_reserved_ip()

            self.assertEqual(expected, actual)

    def test_is_reserved_ipv4_wrong_input(self):
        """
        Test Check().is_reserved_ipv4() for the case that non IP dataset is given..
        """

        expected = False

        for to_check in pyf_test_dataset.VALID_DOMAINS:
            actual = Check(to_check).is_reserved_ipv4()

            self.assertEqual(expected, actual)

    def test_is_reserved_ipv4(self):
        """
        Test Check().is_reserved_ipv4() for the case that a reserved IP is given.
        """

        for subject in pyf_test_dataset.RESERVED_IPV4:
            expected = True
            actual = Check(subject).is_reserved_ipv4()

            self.assertEqual(
                expected, actual, "{0} is not IPv4 reserved.".format(repr(subject))
            )

    def test_is_reserved_ipv6(self):
        """
        Test Check().is_reserved_ipv6() for the case that a reserved IP is given.
        """

        for subject in pyf_test_dataset.RESERVED_IPV6:
            expected = True
            actual = Check(subject).is_reserved_ipv6()

            self.assertEqual(
                expected, actual, "{0} is not IPv6 reserved.".format(repr(subject))
            )

    def test_is_not_reserved_ipv4(self):
        """
        Test Check().is_reserved_ipv4() for the case that it is not a reserved IP.
        """

        expected = False

        for subject in pyf_test_dataset.NOT_RESERVED_IPV4:
            actual = Check(subject).is_reserved_ipv4()

            self.assertEqual(
                expected, actual, "{0} is IPv4 reserved.".format(repr(subject))
            )

    def test_is_not_reserved_ipv6(self):
        """
        Test Check().is_reserved_ipv6() for the case that is not a reserved IP.
        """

        expected = False

        for subject in pyf_test_dataset.NOT_RESERVED_IPV6:
            to_check = subject
            actual = Check(to_check).is_reserved_ipv6()

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
