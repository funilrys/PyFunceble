#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the exipration date logic.

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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import requests
from PyFunceble.generate import Generate
from PyFunceble.helpers import File, Regex
from PyFunceble.http_code import HTTPCode
from PyFunceble.lookup import Lookup
from PyFunceble.referer import Referer
from PyFunceble.status import Status


class ExpirationDate(object):
    """
    Get, format and return the epiration date of a domain if exist.
    """

    def __init__(self):
        self.log_separator = "=" * 100 + " \n"

        self.expiration_date = ""
        self.whois_record = ""

    @classmethod
    def is_domain_valid(cls, domain=None):
        """
        Check if PyFunceble.CONFIGURATION['domain'] is a valid domain.

        Argument:
            - domain: str
                The domain to test

        """

        regex_valid_domains = r"^(?=.{0,253}$)(([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9]))$"  # pylint: disable=line-too-long

        if domain:
            to_test = domain
        else:
            to_test = PyFunceble.CONFIGURATION["domain"]

        return Regex(to_test, regex_valid_domains, return_data=False).match()

    @classmethod
    def is_ip_valid(cls, ip_to_check=None):
        """
        Check if PyFunceble.CONFIGURATION['domain'] is a valid IPv4.

        Argument:
            - ip_to_check: str
                The ip to test

        Note:
            We only test IPv4 because for now we only support domain and IPv4.
        """

        regex_ipv4 = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$"  # pylint: disable=line-too-long

        if ip_to_check:
            to_test = ip_to_check
        else:
            to_test = PyFunceble.CONFIGURATION["domain"]

        return Regex(to_test, regex_ipv4, return_data=False).match()

    def get(self):  # pragma: no cover
        """
        Execute the logic behind the meaning of ExpirationDate + return the matched status.
        """

        domain_validation = self.is_domain_valid()
        ip_validation = self.is_ip_valid()

        if domain_validation and not ip_validation or domain_validation:
            PyFunceble.CONFIGURATION.update(
                {"http_code": HTTPCode().get(), "referer": Referer().get()}
            )

            if PyFunceble.CONFIGURATION["referer"] in [
                PyFunceble.STATUS["official"]["up"],
                PyFunceble.STATUS["official"]["down"],
                PyFunceble.STATUS["official"]["invalid"],
            ]:
                return PyFunceble.CONFIGURATION["referer"]

            elif PyFunceble.CONFIGURATION["referer"]:
                return self._extract()

            self._whois_log()
            return Status(PyFunceble.STATUS["official"]["down"]).handle()

        elif ip_validation and not domain_validation or ip_validation:
            PyFunceble.CONFIGURATION["http_code"] = HTTPCode().get()

            self._whois_log()
            return Status(PyFunceble.STATUS["official"]["down"]).handle()

        self._whois_log()
        return Status(PyFunceble.STATUS["official"]["invalid"]).handle()

    def _whois_log(self):  # pragma: no cover
        """
        Log the whois record into a file
        """

        if PyFunceble.CONFIGURATION["debug"] and PyFunceble.CONFIGURATION["logs"]:
            log = self.log_separator + str(
                self.whois_record
            ) + "\n" + self.log_separator

            output = PyFunceble.CURRENT_DIRECTORY
            output += PyFunceble.OUTPUTS["parent_directory"]
            output += PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
            output += PyFunceble.OUTPUTS["logs"]["directories"]["whois"]

            if PyFunceble.CONFIGURATION["referer"]:
                output += PyFunceble.CONFIGURATION["referer"]
            else:
                output += PyFunceble.STATUS["official"]["invalid"]

            File(output).write(log)

    @classmethod
    def _convert_1_to_2_digits(cls, number):
        """
        Convert 1 digit number to two digits.
        """

        return str(number).zfill(2)

    @classmethod
    def _convert_or_shorten_month(cls, data):
        """
        Convert a given month into our unified format.

        Argument:
            - data: str
                The month to convert or shorten.

        Returns: str
            The unified month name.
        """

        short_month = {
            "jan": [str(1), "01", "Jan", "January"],
            "feb": [str(2), "02", "Feb", "February"],
            "mar": [str(3), "03", "Mar", "March"],
            "apr": [str(4), "04", "Apr", "April"],
            "may": [str(5), "05", "May"],
            "jun": [str(6), "06", "Jun", "June"],
            "jul": [str(7), "07", "Jul", "July"],
            "aug": [str(8), "08", "Aug", "August"],
            "sep": [str(9), "09", "Sep", "September"],
            "oct": [str(10), "Oct", "October"],
            "nov": [str(11), "Nov", "November"],
            "dec": [str(12), "Dec", "December"],
        }

        for month in short_month:
            if data in short_month[month]:
                return month

        return data

    def log(self):  # pragma: no cover
        """
        Log the extracted expiration date and domain into a file.
        """

        if PyFunceble.CONFIGURATION["logs"]:
            log = self.log_separator + "Expiration Date: %s \n" % self.expiration_date
            log += "Tested domain: %s \n" % PyFunceble.CONFIGURATION["domain"]

            File(
                PyFunceble.CURRENT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["date_format"]
                + PyFunceble.CONFIGURATION["referer"]
            ).write(
                log
            )

            if PyFunceble.CONFIGURATION["share_logs"]:
                date_to_share = {
                    "domain": PyFunceble.CONFIGURATION["domain"],
                    "expiration_date": self.expiration_date,
                    "whois_server": PyFunceble.CONFIGURATION["referer"],
                }

                requests.post(PyFunceble.LINKS["api_date_format"], data=date_to_share)

    def _cases_management(self, regex_number, matched_result):
        """
        A little helper of self.format. (Avoiding of nested loops)

        Note:
            Please note that the second value of the case represent the groups
            in order [day,month,year]. This means that a [2,1,0] will be for
            example for a date in format `2017-01-02` where `01` is the month.

        Retuns: list or None
            - None: the case is unknown.
            - list: the list representing the date [day, month, year]
        """

        cases = {
            "first": [[1, 2, 3, 10, 11, 22, 26, 27, 28, 29, 32, 34, 38], [0, 1, 2]],
            "second": [[14, 15, 31, 33, 36, 37], [1, 0, 2]],
            "third": [
                [4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 20, 21, 23, 24, 25, 30, 35],
                [2, 1, 0],
            ],
        }

        for case in cases:
            case_data = cases[case]

            if int(regex_number) in case_data[0]:

                return [
                    self._convert_1_to_2_digits(matched_result[case_data[1][0]]),
                    self._convert_or_shorten_month(matched_result[case_data[1][1]]),
                    str(matched_result[case_data[1][2]]),
                ]

        return matched_result  # pragma: no cover

    def _format(self, date_to_convert=None):
        """
        Format the expiration date into an unified format (01-jan-1970).

        Argument:
            - date_to_convert: str
                The date to convert.
        """

        if not date_to_convert:  # pragma: no cover
            date_to_convert = self.expiration_date

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

        for regx in regex_dates:
            matched_result = Regex(
                date_to_convert, regex_dates[regx], return_data=True, rematch=True
            ).match()

            if matched_result:
                date = self._cases_management(regx, matched_result)

                if date:
                    return "-".join(date)

        return ""

    def _extract(self):  # pragma: no cover
        """
        Extract the expiration date from the whois record.
        """

        self.whois_record = Lookup().whois(PyFunceble.CONFIGURATION["referer"])

        to_match = [
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
        ]

        if self.whois_record:
            for string in to_match:
                expiration_date = Regex(
                    self.whois_record, string, return_data=True, rematch=True, group=0
                ).match()

                if expiration_date:
                    self.expiration_date = expiration_date[0].strip()

                    regex_rumbers = r"[0-9]"
                    if Regex(
                        self.expiration_date, regex_rumbers, return_data=False
                    ).match():

                        self.expiration_date = self._format()

                        if self.expiration_date and not Regex(
                            self.expiration_date,
                            r"[0-9]{2}\-[a-z]{3}\-2[0-9]{3}",
                            return_data=False,
                        ).match():
                            self.log()
                            self._whois_log()

                        Generate(
                            PyFunceble.STATUS["official"]["up"],
                            "WHOIS",
                            self.expiration_date,
                        ).status_file()

                        self._whois_log()
                        return PyFunceble.STATUS["official"]["up"]

                    self._whois_log()
                    return Status(PyFunceble.STATUS["official"]["down"]).handle()

        self._whois_log()
        return Status(PyFunceble.STATUS["official"]["down"]).handle()
