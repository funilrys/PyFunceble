# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.check.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
# pylint: disable=import-error

from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.check import Check


class TestCheck(TestCase):
    """
    Test PyFunceble.check.Check().
    """

    def setUp(self):
        """
        Setup what we need for the tests.
        """

        PyFunceble.load_config(True)

        self.valid_domain = [
            "_hello_.abuse.co.za",
            "_hello_world_.abuse.co.za",
            "_hello_world_.hello.eu.com",
            "_hello-beautiful-world_.wold.eu.com",
            "_hello-world.abuse.co.za",
            "_hello._world.abuse.co.za",
            "_hello.abuse.co.za",
            "_world_.hello.eu.com",
            "_world.hello.eu.com",
            "hello_.world.eu.com",
            "hello_world.abuse.co.za",
            "hello_world.world.com",
            "hello_world.world.hello.com",
            "hello---world.com",
            "hello-.abuse.co.za",
            "hello-world.com",
            "hello.world_hello.world.com",
            "hello.world.com",
            "hello.world.hello.com",
            "xn--bittr-fsa6124c.com",
            "xn--bllogram-g80d.com",
            "xn--coinbse-30c.com",
            "xn--cryptopi-ux0d.com",
            "xn--cyptopia-4e0d.com",
        ]

        self.not_valid_domain = [
            "_world._hello.eu.com",
            "_world.hello_.eu.com",
            "-hello-.abuse.co.za",
            "-hello-world_.abuse.co.za",
            "-hello-world_all-mine_.hello.eu.com",
            "-hello.abuse.co.za",
            "-hello.world",
            "-world.hello",
            "bịllogram.com",
            "bittréẋ.com",
            "coinbȧse.com",
            "cryptopiạ.com",
            "cṙyptopia.com",
            "hello_world_.com",
            "hello_world.com",
            "hello-.world",
            "hello-world",
            "hello.-hello-world_.abuse.co.za",
            "hello.com:443",
            "hello@world.com",
            "httpWd",
            "test.-hello-world_all-mine_.abuse.co.za",
            "world_hello.com",
            "world-.hello",
            "world-hello",
            "world.hello:80",
            "world@hello.com",
        ]

    def test_is_url_valid(self):
        """
        Test URL.is_url_valid() for the case that the URL is valid.
        """

        expected = True

        for domain in self.valid_domain:
            PyFunceble.CONFIGURATION["to_test"] = "http://%s/helloworld" % domain

            actual = Check().is_url_valid()

            self.assertEqual(expected, actual)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_url_valid()

            self.assertEqual(expected, actual)

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_url_valid_not_valid(self):
        """
        Test URL.is_url_valid() for the case that the URL is not valid.
        """

        expected = False

        for domain in self.not_valid_domain:
            actual = Check().is_url_valid("https://%s/hello_world" % domain)

            self.assertEqual(expected, actual)

            actual = Check("https://%s/hello_world" % domain).is_url_valid()

            self.assertEqual(expected, actual)

    def test_is_url_valid_protocol_not_supported(self):
        """
        Test URL.is_url_valid() for the case that the
        URL protocol is not supported nor given.
        """

        expected = False

        for domain in self.not_valid_domain:
            actual = Check().is_url_valid("%s/hello_world" % domain)

            self.assertEqual(expected, actual)

            actual = Check("%s/hello_world" % domain).is_url_valid()

            self.assertEqual(expected, actual)

    def test_is_url_valid_convert_idna(self):
        """
        Test Check().is_url_valid() for the case that
        we have to convert to IDNA.
        """

        PyFunceble.CONFIGURATION["idna_conversion"] = True

        domains_to_test = [
            "bittréẋ.com",
            "hello-world.com",
            "coinbȧse.com",
            "cryptopiạ.com",
            "cṙyptopia.com",
        ]
        expected_domains = [
            "xn--bittr-fsa6124c.com",
            "hello-world.com",
            "xn--coinbse-30c.com",
            "xn--cryptopi-ux0d.com",
            "xn--cyptopia-4e0d.com",
        ]

        for num, domain in enumerate(domains_to_test):
            expected = "http://%s/hello_world" % expected_domains[num]
            to_test = "http://%s/hello_world" % domain

            actual = Check().is_url_valid(to_test, return_formatted=True)

            self.assertEqual(expected, actual)

            actual = Check(to_test).is_url_valid(return_formatted=True)
            self.assertEqual(expected, actual)

    def test_is_url_valid_not_convert_idna(self):
        """
        Test Check().is_url_valid() for the case that
        we do not have to convert to IDNA.
        """

        PyFunceble.CONFIGURATION["idna_conversion"] = False

        domains_to_test = [
            "bittréẋ.com",
            "hello-world.com",
            "coinbȧse.com",
            "cryptopiạ.com",
            "cṙyptopia.com",
        ]

        for domain in domains_to_test:
            to_test = "http://%s/hello_world" % domain
            expected = to_test

            actual = Check().is_url_valid(to_test, return_formatted=True)

            self.assertEqual(expected, actual)

            actual = Check(to_test).is_url_valid(return_formatted=True)
            self.assertEqual(expected, actual)

    def test_is_domain_valid(self):
        """
        Test Check().is_domain_valid() for the case that domains
        are valid.
        """

        expected = True

        for domain in self.valid_domain:
            PyFunceble.CONFIGURATION["to_test"] = domain
            actual = Check().is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is invalid." % domain)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is invalid." % domain)

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_domain_valid_not_valid(self):
        """
        Test Check().is_domain_valid() for the case that
        we meet invalid domains.
        """

        expected = False

        for domain in self.not_valid_domain:
            PyFunceble.CONFIGURATION["to_test"] = domain
            actual = Check().is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % domain)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % domain)

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_subdomain_valid(self):
        """
        Test Check().is_subdomain() for the case subdomains
        are valid.
        """

        valid = [
            "hello_world.world.com",
            "hello_world.world.hello.com",
            "hello.world_hello.world.com",
            "hello.world.hello.com",
            "hello_.world.eu.com",
            "_world.hello.eu.com",
            "_world_.hello.eu.com",
            "_hello-beautiful-world_.wold.eu.com",
            "_hello_world_.hello.eu.com",
            "_hello.abuse.co.za",
            "_hello_.abuse.co.za",
            "_hello._world.abuse.co.za",
            "_hello-world.abuse.co.za",
            "_hello_world_.abuse.co.za",
            "hello_world.abuse.co.za",
            "hello-.abuse.co.za",
        ]

        expected = True

        for domain in valid:
            PyFunceble.CONFIGURATION["to_test"] = domain
            actual = Check().is_subdomain()

            self.assertEqual(expected, actual, msg="%s is not a subdomain." % domain)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_subdomain()

            self.assertEqual(expected, actual, msg="%s is not a subdomain." % domain)

            actual = Check().is_subdomain(PyFunceble.CONFIGURATION["to_test"])

            self.assertEqual(expected, actual, msg="%s is not a subdomain." % domain)

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_subdomain_not_valid(self):
        """
        Test Check().is_subdomain() for the case subdomains
        are not valid.
        """

        not_valid = [
            "hello-world",
            "-hello.world",
            "hello-.world",
            "hello_world.com",
            "hello_world_.com",
            "bittréẋ.com",
            "bịllogram.com",
            "coinbȧse.com",
            "cryptopiạ.com",
            "cṙyptopia.com",
            "google.com",
        ]

        expected = False

        for domain in not_valid:
            PyFunceble.CONFIGURATION["to_test"] = domain
            actual = Check().is_subdomain()

            self.assertEqual(expected, actual, msg="%s is a subdomain." % domain)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_subdomain()

            self.assertEqual(expected, actual, msg="%s is a subdomain." % domain)

            actual = Check().is_subdomain(PyFunceble.CONFIGURATION["to_test"])

            self.assertEqual(expected, actual, msg="%s is a subdomain." % domain)

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_ip_valid(self):
        """
        Test Check().is_ip_valid() for the case that the IP is valid.
        """

        expected = True
        valid = ["15.47.85.65", "45.66.255.240"]

        for ip_to_test in valid:
            actual = Check().is_ip_valid(ip_to_test)

            self.assertEqual(expected, actual, msg="%s is invalid." % ip_to_test)

            actual = Check(ip_to_test).is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is invalid." % ip_to_test)

    def test_is_ip_valid_not_valid(self):
        """
        Test Check().is_ip_valid() for the case that the IP
        is not valid.
        """

        expected = False
        invalid = ["google.com", "287.468.45.26", "245.85.69.17:8081"]

        for ip_to_test in invalid:
            PyFunceble.CONFIGURATION["to_test"] = ip_to_test
            actual = Check().is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % ip_to_test)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % ip_to_test)

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_ip_range(self):
        """
        Test Check().is_ip_range() for the case that the IP is a range.
        """

        expected = True
        valid = ["255.45.65.0/24", "255.45.65.6/18"]

        for ip_to_test in valid:
            PyFunceble.CONFIGURATION["to_test"] = ip_to_test
            actual = Check().is_ip_range()

            self.assertEqual(
                expected, actual, msg="%s is not an IP range." % ip_to_test
            )

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_ip_range()

            self.assertEqual(
                expected, actual, msg="%s is not an IP range." % ip_to_test
            )

            del PyFunceble.CONFIGURATION["to_test"]

    def test_is_ip_range_not(self):
        """
        Test Check().is_ip_range() for the case that the IP is not a range.
        """

        expected = False
        valid = ["15.47.85.65", "45.66.255.240", "github.com"]

        for ip_to_test in valid:
            actual = Check().is_ip_range(ip_to_test)

            self.assertEqual(expected, actual, msg="%s is an IP range." % ip_to_test)

            actual = Check(ip_to_test).is_ip_range()

            self.assertEqual(expected, actual, msg="%s is an IP range." % ip_to_test)


if __name__ == "__main__":
    launch_tests()
