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

Tests of PyFunceble.extractor.expiration_date

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

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

from random import choice
from unittest import TestCase
from unittest import main as launch_tests

from PyFunceble.extractor import ExpirationDate


class TestExpirationDate(TestCase):
    """
    Tests of PyFunceble.engine.expiration_date.
    """

    def setUp(self):
        """
        Setups everything needed for the tests.
        """

        self.dates_samples = [
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

        self.expiration_date_markers = [
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

        self.expiration_dates = []

        for marker in self.expiration_date_markers:
            self.expiration_dates.append(f"{marker} {choice(self.dates_samples)}")

    def test_extractor(self):
        """
        Tests extractor.
        """

        expected = "02-jan-2017"

        for date in self.expiration_dates:
            actual = ExpirationDate(date).get_extracted()

            self.assertEqual(expected, actual, date)

        actual = (
            ExpirationDate(
                f"Record expires on {choice(self.dates_samples)} (YYYY-MM-DD)"
            ).get_extracted(),
        )

        expected = None
        actual = ExpirationDate("").get_extracted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
