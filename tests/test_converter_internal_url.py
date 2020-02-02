# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.converters.internal_url

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

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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
from unittest.mock import patch

from PyFunceble.converter.internal_url import InternalUrl


class TestInternalURL(TestCase):
    """
    Tests of PyFunceble.converters.internal_url
    """

    @patch("PyFunceble.abstracts.Package.VERSION", "1.0.0.dev (Hello, World)")
    def test_nothing_to_do(self):
        """
        Tests case that there is no changes.
        """

        expected = (
            "https://raw.githubusercontent.com/funilrys/PyFuneceble/dev/test.json"
        )

        actual = InternalUrl(expected).get_converted()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "1.0.0. (Hello, World)")
    def test_from_dev_to_master(self):
        """
        Tests case that there is no changes.
        """

        given = "https://raw.githubusercontent.com/funilrys/PyFuneceble/dev/test.json"
        expected = (
            "https://raw.githubusercontent.com/funilrys/PyFuneceble/master/test.json"
        )
        actual = InternalUrl(given).get_converted()

        self.assertEqual(expected, actual)

    @patch("PyFunceble.abstracts.Package.VERSION", "1.0.0.dev (Hello, World)")
    def test_from_master_to_dev(self):
        """
        Tests case that there is no changes.
        """

        given = "https://raw.githubusercontent.com/funilrys/PyFuneceble/dev/test.json"
        expected = (
            "https://raw.githubusercontent.com/funilrys/PyFuneceble/dev/test.json"
        )
        actual = InternalUrl(given).get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
