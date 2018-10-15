# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

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
    https://pyfunceble.readthedocs.io

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
    This class will test PyFunceble.check.Check().
    """

    def test_is_url_valid(self):
        """
        This method will test URL.is_url_valid().
        """

        # Test of the case that the URL is valid
        expected = True
        PyFunceble.CONFIGURATION["to_test"] = "http://hello.world/helloworld"
        actual = Check().is_url_valid()

        self.assertEqual(expected, actual)
        actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_url_valid()
        self.assertEqual(expected, actual)

        # Test of the case that the domains is not valid
        not_valid = [
            "world-hello",
            "-world.hello",
            "world-.hello",
            "world@hello.com",
            "world_hello.com",
            "httpWd",
        ]

        for domain in not_valid:
            expected = False
            actual = Check().is_url_valid("https://%s/hello_world" % domain)

            self.assertEqual(expected, actual)

            actual = Check("https://%s/hello_world" % domain).is_url_valid()

            self.assertEqual(expected, actual)

        # Test of the case that the protocol is not supported
        for domain in not_valid:
            expected = False
            actual = Check().is_url_valid("%s/hello_world" % domain)

            self.assertEqual(expected, actual)

            actual = Check("%s/hello_world" % domain).is_url_valid()

            self.assertEqual(expected, actual)

    def test_is_domains_valid(self):
        """
        This method test ExpirationDate().is_domain_valid().
        """

        # Test of the case that the domains are valid
        valid = [
            "hello-world.com",
            "hello.world.com",
            "hello_world.world.com",
            "hello_world.world.hello.com",
            "hello.world_hello.world.com",
            "hello---world.com",
            "hello.world.hello.com",
            "hello_.world.eu.com",
            "_world.hello.eu.com",
            "_world_.hello.eu.com",
            "_hello-beautiful-world_.wold.eu.com",
            "_hello_world_.hello.eu.com",
            "xn--bittr-fsa6124c.com",
            "xn--bllogram-g80d.com",
            "xn--coinbse-30c.com",
            "xn--cryptopi-ux0d.com",
            "xn--cyptopia-4e0d.com",
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
            actual = Check().is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is invalid." % domain)
            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_domain_valid()
            self.assertEqual(expected, actual, msg="%s is invalid." % domain)

        self.assertEqual(expected, actual)

        # Test of the case that the domains are not valid
        not_valid = [
            "hello-world",
            "-hello.world",
            "hello-.world",
            "hello@world.com",
            "hello_world.com",
            "hello_world_.com",
            "hello.com:443",
            "world.hello:80",
            "_world._hello.eu.com",
            "_world.hello_.eu.com",
            "bittréẋ.com",
            "bịllogram.com",
            "coinbȧse.com",
            "cryptopiạ.com",
            "cṙyptopia.com",
            "-hello-world_all-mine_.hello.eu.com",
            "test.-hello-world_all-mine_.abuse.co.za",
            "-hello-world_.abuse.co.za",
            "hello.-hello-world_.abuse.co.za",
            "-hello.abuse.co.za",
            "-hello-.abuse.co.za",
        ]
        expected = False

        for domain in not_valid:
            PyFunceble.CONFIGURATION["to_test"] = domain
            actual = Check().is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % domain)
            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_domain_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % domain)

    def test_is_ip_valid(self):
        """
        This method test ExpirationDate().is_ip_valid().
        """

        # test of the case that the ip is valid
        expected = True
        valid = ["15.47.85.65", "45.66.255.240"]

        for ip_to_test in valid:
            actual = Check().is_ip_valid(ip_to_test)

            self.assertEqual(expected, actual, msg="%s is invalid." % ip_to_test)

            actual = Check(ip_to_test).is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is invalid." % ip_to_test)

        # test of the case that the ip is invalid
        expected = False
        invalid = ["google.com", "287.468.45.26", "245.85.69.17:8081"]

        for ip_to_test in invalid:
            PyFunceble.CONFIGURATION["to_test"] = ip_to_test
            actual = Check().is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % ip_to_test)

            actual = Check(PyFunceble.CONFIGURATION["to_test"]).is_ip_valid()

            self.assertEqual(expected, actual, msg="%s is valid." % ip_to_test)


if __name__ == "__main__":
    launch_tests()
