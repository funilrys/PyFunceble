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
