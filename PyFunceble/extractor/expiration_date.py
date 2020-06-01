"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the expiration date extractor.

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

import PyFunceble.converter as converter
import PyFunceble.helpers as helpers

from .base import ExtractorBase


class ExpirationDate(ExtractorBase):
    """
    Provides a way to extract the expiration date from a
    given WHOIS record.

    :param str data: The WHOIS record.s
    """

    # We initiate all possible regex which correspond to an
    # expiration date.
    # We list the list of regex which will help us get an unformatted expiration date.
    expiration_patterns = [
        r"expire:(.*)",
        r"expire on:(.*)",
        r"Expiry Date:(.*)",
        r"free-date(.*)",
        r"expires:(.*)",
        r"Expiration date:(.*)",
        r"Expiry date:(.*)",
        r"Expire Date:(.*)",
        r"renewal date:(.*)",
        r"Expires:(.*)",
        r"validity:(.*)",
        r"Expiration Date             :(.*)",
        r"Expiry :(.*)",
        r"expires at:(.*)",
        r"domain_datebilleduntil:(.*)",
        r"Data de expiração \/ Expiration Date \(dd\/mm\/yyyy\):(.*)",
        r"Fecha de expiración \(Expiration date\):(.*)",
        r"\[Expires on\](.*)",
        r"Record expires on(.*)(\(YYYY-MM-DD\))",
        r"status:      OK-UNTIL(.*)",
        r"renewal:(.*)",
        r"expires............:(.*)",
        r"expire-date:(.*)",
        r"Exp date:(.*)",
        r"Valid-date(.*)",
        r"Expires On:(.*)",
        r"Fecha de vencimiento:(.*)",
        r"Expiration:.........(.*)",
        r"Fecha de Vencimiento:(.*)",
        r"Registry Expiry Date:(.*)",
        r"Expires on..............:(.*)",
        r"Expiration Time:(.*)",
        r"Expiration Date:(.*)",
        r"Expired:(.*)",
        r"Date d'expiration:(.*)",
        r"expiration date:(.*)",
    ]

    # The regex which match a digit.
    regex_numbers = r"[0-9]"

    # We map the different possible regex.
    # The regex index represent a unique number which have to be reported
    # to the __format_management method.
    regex_dates = {
        # Date in format: 02-jan-2017
        "1": r"([0-9]{2})-([a-z]{3})-([0-9]{4})",
        # Date in format: 02.01.2017 // Month: jan
        "2": r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})$",
        # Date in format: 02/01/2017 // Month: jan
        "3": r"([0-3][0-9])\/(0[1-9]|1[012])\/([0-9]{4})",
        # Date in format: 2017-01-02 // Month: jan
        "4": r"([0-9]{4})-([0-9]{2})-([0-9]{2})$",
        # Date in format: 2017.01.02 // Month: jan
        "5": r"([0-9]{4})\.([0-9]{2})\.([0-9]{2})$",
        # Date in format: 2017/01/02 // Month: jan
        "6": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})$",
        # Date in format: 2017.01.02 15:00:00
        "7": r"([0-9]{4})\.([0-9]{2})\.([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
        # Date in format: 20170102 15:00:00 // Month: jan
        "8": r"([0-9]{4})([0-9]{2})([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
        # Date in format: 2017-01-02 15:00:00 // Month: jan
        "9": r"([0-9]{4})-([0-9]{2})-([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
        # Date in format: 02.01.2017 15:00:00 // Month: jan
        "10": r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
        # Date in format: 02-Jan-2017 15:00:00 UTC
        "11": r"([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{1}.*",  # pylint: disable=line-too-long
        # Date in format: 2017/01/02 01:00:00 (+0900) // Month: jan
        "12": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s\(.*\)",
        # Date in format: 2017/01/02 01:00:00 // Month: jan
        "13": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}$",
        # Date in format: Mon Jan 02 15:00:00 GMT 2017
        "14": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{3}\s([0-9]{4})",  # pylint: disable=line-too-long
        # Date in format: Mon Jan 02 2017
        "15": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s([0-9]{4})",
        # Date in format: 2017-01-02T15:00:00 // Month: jan
        "16": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}$",
        # Date in format: 2017-01-02T15:00:00Z // Month: jan${'7}
        "17": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Z].*",
        # Date in format: 2017-01-02T15:00:00+0200 // Month: jan
        "18": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{4}",
        # Date in format: 2017-01-02T15:00:00+0200.622265+03:00 //
        # Month: jan
        "19": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[+-][0-9]{2}:[0-9]{2}",  # pylint: disable=line-too-long
        # Date in format: 2017-01-02T15:00:00+0200.622265 // Month: jan
        "20": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}$",
        # Date in format: 2017-01-02T23:59:59.0Z // Month: jan
        "21": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[A-Z]",
        # Date in format: 02-01-2017 // Month: jan
        "22": r"([0-9]{2})-([0-9]{2})-([0-9]{4})",
        # Date in format: 2017. 01. 02. // Month: jan
        "23": r"([0-9]{4})\.\s([0-9]{2})\.\s([0-9]{2})\.",
        # Date in format: 2017-01-02T00:00:00+13:00 // Month: jan
        "24": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}",  # pylint: disable=line-too-long
        # Date in format: 20170102 // Month: jan
        "25": r"(?=[0-9]{8})(?=([0-9]{4})([0-9]{2})([0-9]{2}))",
        # Date in format: 02-Jan-2017
        "26": r"([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})$",
        # Date in format: 02.1.2017 // Month: jan
        "27": r"([0-9]{2})\.([0-9]{1})\.([0-9]{4})",
        # Date in format: 02 Jan 2017
        "28": r"([0-9]{1,2})\s([A-Z]{1}[a-z]{2})\s([0-9]{4})",
        # Date in format: 02-January-2017
        "29": r"([0-9]{2})-([A-Z]{1}[a-z]*)-([0-9]{4})",
        # Date in format: 2017-Jan-02.
        "30": r"([0-9]{4})-([A-Z]{1}[a-z]{2})-([0-9]{2})\.",
        # Date in format: Mon Jan 02 15:00:00 2017
        "31": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{1,2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s([0-9]{4})",  # pylint: disable=line-too-long
        # Date in format: Mon Jan 2017 15:00:00
        "32": r"()[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
        # Date in format: January 02 2017-Jan-02
        "33": r"([A-Z]{1}[a-z]*)\s([0-9]{1,2})\s([0-9]{4})",
        # Date in format: 2.1.2017 // Month: jan
        "34": r"([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})",
        # Date in format: 20170102000000 // Month: jan
        "35": r"([0-9]{4})([0-9]{2})([0-9]{2})[0-9]+",
        # Date in format: 01/02/2017 // Month: jan
        "36": r"(0[1-9]|1[012])\/([0-3][0-9])\/([0-9]{4})",
        # Date in format: January  2 2017
        "37": r"([A-Z]{1}[a-z].*)\s\s([0-9]{1,2})\s([0-9]{4})",
        # Date in format: 2nd January 2017
        "38": r"([0-9]{1,})[a-z]{1,}\s([A-Z].*)\s(2[0-9]{3})",
    }

    # We map our regex numbers with with the right group order.
    # Note: please report to the method note for more information about the mapping.
    format_cases = {
        "first": [[1, 2, 3, 10, 11, 22, 26, 27, 28, 29, 32, 34, 38], [0, 1, 2]],
        "second": [[14, 15, 31, 33, 36, 37], [1, 0, 2]],
        "third": [
            [4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 20, 21, 23, 24, 25, 30, 35],
            [2, 1, 0],
        ],
    }

    def __init__(self, data):
        super().__init__(data)

        self.extracted_data = self.__extract_it()

    def __format_management(self, index, matched):
        """
        A format management helper.

        .. note::
            Please note that the second value of the case represent the groups
            in order :code:`[day,month,year]`.

            This means that a :code:`[2,1,0]` will be for example for a date
            in format :code:`2017-01-02` where
            :code:`01` is the month.

        :param int index: The identifiant of the regex.

        :param list matched: The matched result to format.

        :return:
            A list representing the expiration date.
            The list can be "decoded" like :code:`[day, month, year]`
        :rtype: list|None
        """

        for _, case_data in self.format_cases.items():
            if int(index) in case_data[0]:
                # The regex number is into the currently read case data.

                # We return a list with the formatted elements.
                # 1. We convert the day to 2 digits.
                # 2. We convert the month to the unified format.
                # 3. We return the year.
                return [
                    converter.Digit2Digits(matched[case_data[1][0]]).get_converted(),
                    converter.Month(matched[case_data[1][1]]).get_converted(),
                    str(matched[case_data[1][2]]),
                ]

        return matched  # pragma: no cover

    def __format_it(self, data):
        """
        Formats the given data.
        """

        for index, regex in self.regex_dates.items():
            matched = helpers.Regex(regex).match(data, return_match=True, rematch=True)

            if not matched:
                continue

            date = self.__format_management(index, matched)

            if not date:  # pragma: no cover
                continue

            return "-".join(date)
        return None  # pragma: no cover

    def __extract_it(self):
        """
        Try to extract the expiration date from the given
        data.
        """

        for regex in self.expiration_patterns:
            expiration_date = helpers.Regex(regex).match(
                self.data, return_match=True, rematch=True, group=0
            )

            if not expiration_date:
                continue

            expiration_date = expiration_date[0].strip()

            if helpers.Regex(self.regex_numbers).match(
                expiration_date, return_match=True
            ):
                return self.__format_it(expiration_date)

        return None
