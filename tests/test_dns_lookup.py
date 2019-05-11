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

This submodule will test PyFunceble.dns_lookup.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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

from PyFunceble.dns_lookup import DNSLookup


class TestDNSLookup(TestCase):
    """
    Try to test PyFunceble.dns_nslookup
    Indeed, we use try because it's impossible to know if a domain is always up
    but we try to keep it simple.
    """

    def test_dns_lookup_domain_down(self):
        """
        Test of NSLookup() for the case a domain is down or non
        existant.
        """

        expected = {}
        actual = DNSLookup("thisdoes-not-workdnfhfep.de").request()

        self.assertEqual(expected, actual)

    def test_dns_lookup_domain_invalid(self):
        """
        Test of NSLookup() for the case a domain is invalid.
        """

        expected = {}
        actual = DNSLookup("helloworld-.com").request()

        self.assertEqual(expected, actual)

    def test_dns_lookup_domain_up(self):
        """
        Test of Lookup().request() for the case a domain is up.
        """

        actual = DNSLookup("google.com").request()

        self.assertIsInstance(actual, dict)

        if "A" not in actual:
            raise AssertionError(actual)

        actual = DNSLookup("172.217.22.14").request()

        self.assertIsInstance(actual, dict)

        if "PTR" not in actual:
            raise AssertionError(actual)

        if "A" not in actual:
            raise AssertionError(actual)


if __name__ == "__main__":
    launch_tests()
