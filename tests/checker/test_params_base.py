"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our checker parameters base.

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

import unittest

from PyFunceble.checker.params_base import CheckerParamsBase


class TestCheckerParamsBase(unittest.TestCase):
    """
    Tests of the base of all our checker parameters.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.params = CheckerParamsBase()

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        del self.params

    def test_to_dict(self) -> None:
        """
        Tests the method which let us get the :py:class:`dict` representation
        of the current parameters.
        """

        self.params.do_syntax_check_first = True
        self.params.use_collection = False

        expected = {"do_syntax_check_first": True, "use_collection": False}

        actual = self.params.to_dict()

        self.assertEqual(expected, actual)

    def test_to_json(self) -> None:
        """
        Tests the method which let us get the JSON representation of the
        current parameters.
        """

        self.params.do_syntax_check_first = True
        self.params.use_collection = False

        expected = """{
    "do_syntax_check_first": true,
    "use_collection": false
}"""

        actual = self.params.to_json()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
