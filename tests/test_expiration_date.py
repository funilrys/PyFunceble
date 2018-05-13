"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.expiration_date


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
# pylint: disable=protected-access
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.expiration_date import ExpirationDate


class TestExpirationDate(TestCase):
    """
    This class will test PyFunceble.expiration_date.
    """

    def test_is_domains_valid(self):
        """
        This method test ExpirationDate().is_domain_valid().
        """

        # Test of the case that the domains is valid
        expected = True
        PyFunceble.CONFIGURATION["domain"] = "hello.world"
        actual = ExpirationDate().is_domain_valid()

        self.assertEqual(expected, actual)

        # Test of the case that the domains is not valid
        not_valid = [
            "hello-world",
            "-hello.world",
            "hello-.world",
            "hello@world.com",
            "hello_world.com",
        ]
        expected = False

        for domain in not_valid:
            PyFunceble.CONFIGURATION["domain"] = domain
            actual = ExpirationDate().is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % domain)

    def test_is_ip_valid(self):
        """
        This method test ExpirationDate().is_ip_valid().
        """

        # test of the case that the ip is valid
        expected = True
        valid = ["15.47.85.65", "45.66.255.240"]

        for ip_to_test in valid:
            PyFunceble.CONFIGURATION["domain"] = ip_to_test
            actual = ExpirationDate().is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is invalid." % ip_to_test)

        # test of the case that the ip is invalid
        expected = False
        invalid = ["google.com", "287.468.45.26", "245.85.69.17:8081"]

        for ip_to_test in invalid:
            PyFunceble.CONFIGURATION["domain"] = ip_to_test
            actual = ExpirationDate().is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % ip_to_test)

    def test_convert_or_shorten_month(self):
        """
        This method test ExpirationDate()._convert_or_shorten_month().
        """

        expected = "jan"

        for element in ["1", "01", "Jan", "January"]:
            actual = ExpirationDate()._convert_or_shorten_month(element)

            self.assertEqual(expected, actual)

        expected = "Hello"
        actual = ExpirationDate()._convert_or_shorten_month("Hello")

        self.assertEqual(expected, actual)

    def test_convert_1_to_2_digits(self):
        """
        This method test ExpirationDate()._convert_1_to_2_digits().
        """

        expected = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]

        for index, number in enumerate(expected):
            actual = ExpirationDate()._convert_1_to_2_digits(index + 1)
            self.assertEqual(number, actual)

    def test_format_date(self):
        """
        This method test ExpirationDate()._format().
        """

        expected = "02-jan-2017"

        to_test = [
            "02-jan-2017",
            "02.01.2017",
            "02/01/2017",
            "2017-01-02",
            "2017.01.02",
            "2017/01/02",
            "2017.01.02 15:00:00",
            "20170102 15:00:00",
            "2017-01-02 15:00:00",
            "02.01.2017 15:00:00",
            "02-Jan-2017 15:00:00 UTC",
            "2017/01/02 01:00:00 (+0900)",
            "2017/01/02 01:00:00",
            "Mon Jan 02 15:00:00 GMT 2017",
            "Mon Jan 02 2017",
            "2017-01-02T15:00:00",
            "2017-01-02T15:00:00Z",
            "2017-01-02T15:00:00+0200",
            "2017-01-02T15:00:00+0200.622265+03:00",
            "2017-01-02T15:00:00+0200.622265",
            "2017-01-02T23:59:59.0Z",
            "02-01-2017",
            "2017. 01. 02.",
            "2017-01-02T00:00:00+13:00",
            "20170102",
            "02-Jan-2017",
            "02.1.2017",
            "02 Jan 2017",
            "02-January-2017",
            "2017-Jan-02.",
            "Mon Jan 02 15:00:00 2017",
            "January 02 2017-Jan-02",
            "2.1.2017",
            "20170102000000",
            "January  2 2017",
            "2nd January 2017",
        ]

        for date in to_test:
            actual = ExpirationDate()._format(date)
            self.assertEqual(expected, actual, msg="Error for %s" % repr(date))

        special_case = {
            "1": ["02/13/2017", "13-feb-2017"],
            "2": ["Mon Jan 2017 15:00:00", "00-jan-2017"],
            "3": ["15 janvier 2017", ""],
            "4": ["This is not a date", ""],
        }

        for data in special_case:
            actual = ExpirationDate()._format(special_case[data][0])
            expected = special_case[data][-1]
            self.assertEqual(
                expected, actual, msg="Error for %s" % special_case[data[0]]
            )


if __name__ == "__main__":
    launch_tests()
