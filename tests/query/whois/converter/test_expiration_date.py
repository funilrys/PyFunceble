"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our expiration date extractor.

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


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

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
from typing import List

from PyFunceble.query.whois.converter.expiration_date import ExpirationDateExtractor


class TestExpirationDateExtractor(unittest.TestCase):
    """
    Tests our interface for the extraction of expiration date.
    """

    DATE_SAMPLES: List[str] = [
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

    EXPIRATION_DATE_MARKERS: List[str] = [
        "expire: ",
        "expire on: ",
        "Expiry Date: ",
        "free-date ",
        "expires: ",
        "Expiration date: ",
        "Expiry date: ",
        "Expire Date: ",
        "renewal date: ",
        "Expires: ",
        "validity: ",
        "Expiration Date             : ",
        "Expiry : ",
        "expires at: ",
        "domain_datebilleduntil: ",
        "Data de expiração / Expiration Date (dd/mm/yyyy): ",
        "Fecha de expiración (Expiration date): ",
        "[Expires on] ",
        "status:      OK-UNTIL ",
        "renewal: ",
        "expires............: ",
        "expire-date: ",
        "Exp date: ",
        "Valid-date ",
        "Expires On: ",
        "Fecha de vencimiento: ",
        "Expiration:......... ",
        "Fecha de Vencimiento: ",
        "Registry Expiry Date: ",
        "Expires on..............: ",
        "Expiration Time: ",
        "Expiration Date: ",
        "Expired: ",
        "Date d'expiration: ",
        "expiration date: ",
    ]

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = ExpirationDateExtractor()

    def tearDown(self) -> None:
        """
        Destroys everything needed for the tests.
        """

        del self.converter

    def test_set_data_to_convert_not_str(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that it's not a string.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_data_to_convert(given))

    def test_set_data_to_convert_empty_str(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that it's an empty string.
        """

        given = ""

        self.assertRaises(ValueError, lambda: self.converter.set_data_to_convert(given))

    def test_get_converted(self) -> None:
        """
        Tests the method which let us get the converted data.
        """

        expected = "02-jan-2017"

        for marker in self.EXPIRATION_DATE_MARKERS:
            for date_sample in self.DATE_SAMPLES:
                test_line = f"{marker} {date_sample}"

                self.converter.data_to_convert = test_line

                actual = self.converter.get_converted()

                self.assertEqual(expected, actual)

    def test_get_converted_no_pattern(self) -> None:
        """
        Tests the method which let us get the converted data.
        """

        given = "Hello, World!"
        expected = None

        self.converter.data_to_convert = given

        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_get_converted_pattern_no_date(self) -> None:
        """
        Tests the method which let us get the converted data.
        """

        given = f"{self.EXPIRATION_DATE_MARKERS[0]} 02 Hello :-)"
        expected = None

        self.converter.data_to_convert = given

        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
