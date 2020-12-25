"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the base of all our status handlers.

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
from datetime import datetime

from PyFunceble.checker.status_base import CheckerStatusBase

try:
    import pyf_test_helpers
except ModuleNotFoundError:
    from .. import pyf_test_helpers


class TestCheckerStatusBase(unittest.TestCase):
    """
    Tests of the base of all our status handler.
    """

    def setUp(self) -> None:
        """
        Setups everything we need.
        """

        self.status = CheckerStatusBase(
            subject="example.org", idna_subject="example.org"
        )

    def tearDown(self) -> None:
        """
        Destroyes everything we don't need.
        """

        del self.status

    def test_to_dict(self) -> None:
        """
        Tests of the method which gives us the :py:class:`dict` representation
        of the current status object.
        """

        test_datetime = datetime.utcnow()

        self.status.status = "ACTIVE"
        self.status.status_source = "Funilrys"
        self.status.tested_at = test_datetime

        expected = {
            "subject": "example.org",
            "idna_subject": "example.org",
            "status": "ACTIVE",
            "status_source": "Funilrys",
            "tested_at": test_datetime,
            "params": None,
        }

        actual = self.status.to_dict()

        self.assertEqual(expected, actual)

    def test_to_json(self) -> None:
        """
        Tests the method which let us get the JSON representation of the
        current status object.
        """

        test_datetime = datetime.fromtimestamp(0, tz=pyf_test_helpers.get_timezone())

        self.status.status = "ACTIVE"
        self.status.status_source = "Funilrys"
        self.status.tested_at = test_datetime

        expected = """{
    "idna_subject": "example.org",
    "params": null,
    "status": "ACTIVE",
    "status_source": "Funilrys",
    "subject": "example.org",
    "tested_at": "1970-01-01T00:00:00+00:00"
}"""

        actual = self.status.to_json()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
