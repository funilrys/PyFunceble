"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our expiration date extracter.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

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

from typing import List, Optional, Tuple

from PyFunceble.helpers.regex import RegexHelper
from PyFunceble.query.whois.converter.base import ConverterBase
from PyFunceble.query.whois.converter.digit2digits import Digit2Digits
from PyFunceble.query.whois.converter.month2unified import Month2Unified


class ExpirationDateExtractor(ConverterBase):
    """
    Provides an interface for the extraction of the expiration date.
    """

    PATTERNS: List[str] = [
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
    """
    Provides all our known patterns.
    """

    REGEX_DIGITS: str = r"[0-9]"
    """
    Provides the regex to match in order to extract the digits.
    """

    MARKER2DATE_REGEX: dict = {
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
        "11": r"([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{1}.*",  # pylint: disable=line-too-long  # noqa: E501
        # Date in format: 2017/01/02 01:00:00 (+0900) // Month: jan
        "12": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s\(.*\)",
        # Date in format: 2017/01/02 01:00:00 // Month: jan
        "13": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}$",
        # Date in format: Mon Jan 02 15:00:00 GMT 2017
        "14": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{3}\s([0-9]{4})",  # pylint: disable=line-too-long  # noqa: E501
        # Date in format: Mon Jan 02 2017
        "15": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s([0-9]{4})",
        # Date in format: 2017-01-02T15:00:00 // Month: jan
        "16": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}$",
        # Date in format: 2017-01-02T15:00:00Z // Month: jan${'7}
        "17": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Z].*",
        # Date in format: 2017-01-02T15:00:00+0200 // Month: jan
        "18": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{4}",  # pylint: disable=line-too-long  # noqa: E501
        # Date in format: 2017-01-02T15:00:00+0200.622265+03:00 //
        # Month: jan
        "19": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[+-][0-9]{2}:[0-9]{2}",  # pylint: disable=line-too-long  # noqa: E501
        # Date in format: 2017-01-02T15:00:00+0200.622265 // Month: jan
        "20": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}$",
        # Date in format: 2017-01-02T23:59:59.0Z // Month: jan
        "21": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[A-Z]",  # pylint: disable=line-too-long  # noqa: E501
        # Date in format: 02-01-2017 // Month: jan
        "22": r"([0-9]{2})-([0-9]{2})-([0-9]{4})",
        # Date in format: 2017. 01. 02. // Month: jan
        "23": r"([0-9]{4})\.\s([0-9]{2})\.\s([0-9]{2})\.",
        # Date in format: 2017-01-02T00:00:00+13:00 // Month: jan
        "24": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}",  # pylint: disable=line-too-long  # noqa: E501
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
        "31": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{1,2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s([0-9]{4})",  # pylint: disable=line-too-long   # noqa: E501
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
    """
    Provides all the known regex to extract the date.

    .. note::
        The index (or key) will be used to map or group some of them later.
    """

    REGEX_PARSE_MAP: List[dict] = [
        {
            "regex_keys": [1, 2, 3, 10, 11, 22, 26, 27, 28, 29, 32, 34, 38],
            "positions": {"day": 0, "month": 1, "year": 2},
        },
        {
            "regex_keys": [14, 15, 31, 33, 36, 37],
            "positions": {"day": 1, "month": 0, "year": 2},
        },
        {
            "regex_keys": [
                4,
                5,
                6,
                7,
                8,
                9,
                12,
                13,
                16,
                17,
                18,
                19,
                20,
                21,
                23,
                24,
                25,
                30,
                35,
            ],
            "positions": {"day": 2, "month": 1, "year": 0},
        },
    ]
    """
    Our parsing map. Indeed, we hava a list of regex, but no way to know
    how to parse them. Especially when the order (month, day, year) are
    different from a format to another.

    This variable solve that problem by interpreting all regex we previously
    created.
    """

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: str) -> None:
        """
        Sets the data to convert or work with.

        :param value:
            The record to work with.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} is given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        # pylint: disable=no-member
        super(ExpirationDateExtractor, self.__class__).data_to_convert.fset(self, value)

    def __get_line(self) -> Optional[str]:
        """
        Tries to get the expiration date line from the given record.
        """

        for regex in self.PATTERNS:
            expiration_date_line = RegexHelper(regex).match(
                self.data_to_convert, return_match=True, rematch=True, group=0
            )

            if not expiration_date_line:
                continue

            return expiration_date_line
        return None

    def __get_actual_expiration_date(
        self, extracted: str
    ) -> Optional[Tuple[str, str, str]]:
        """
        Tries to extract the actual expiration date.
        """

        for index, date_regex in self.MARKER2DATE_REGEX.items():
            matched = RegexHelper(date_regex).match(
                extracted, return_match=True, rematch=True
            )
            date_parts = tuple()

            if not matched:
                continue

            for parse_case in self.REGEX_PARSE_MAP:
                if int(index) not in parse_case["regex_keys"]:
                    continue

                date_parts = (
                    Digit2Digits(
                        matched[parse_case["positions"]["day"]],
                    ).get_converted(),
                    Month2Unified(
                        matched[parse_case["positions"]["month"]]
                    ).get_converted(),
                    str(matched[parse_case["positions"]["year"]]),
                )

            if date_parts:
                return "-".join(date_parts)
        return None

    @ConverterBase.ensure_data_to_convert_is_given
    def get_converted(self) -> Optional[str]:
        """
        Provides the expiration date of the record (if found).
        """

        expiration_date_line = self.__get_line()

        if expiration_date_line:
            expiration_date = expiration_date_line[0].strip()

            if RegexHelper(self.REGEX_DIGITS).match(
                expiration_date, return_match=False
            ):
                return self.__get_actual_expiration_date(expiration_date)

        return None
