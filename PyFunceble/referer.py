#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the referer extraction interface.

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
from PyFunceble.helpers import Dict, File
from PyFunceble.status import Status


class Referer:  # pragma: no cover
    """
    Get the WHOIS server (referer) of the current domain extension according to
    the IANA database.
    """

    def __init__(self):
        # Note: A URL testing or an IP testing does not come around
        # here. So there is no need to be scared by the following.

        try:
            # We get the extension of the currently tested element.
            # We basically get everything after the last point.
            self.domain_extension = PyFunceble.CONFIGURATION["to_test"][
                PyFunceble.CONFIGURATION["to_test"].rindex(".") + 1 :
            ]
        except ValueError:
            # There was not point, so no extension to work with.
            self.domain_extension = None

        # We create a list of ignored extension.
        # Note: We need the following because those extension does
        # not have a centralized whois server (yet).
        self.ignored_extension = [
            "ad",
            "al",
            "an",
            "ao",
            "aq",
            "arpa",
            "az",
            "ba",
            "bb",
            "bd",
            "bf",
            "bh",
            "bl",
            "bq",
            "bs",
            "bt",
            "bv",
            "cg",
            "ck",
            "cu",
            "cv",
            "cw",
            "cy",
            "dj",
            "doosan",
            "eg",
            "eh",
            "er",
            "et",
            "fk",
            "flsmidth",
            "fm",
            "gb",
            "gm",
            "gn",
            "gp",
            "gr",
            "gt",
            "gu",
            "gw",
            "htc",
            "iinet",
            "jm",
            "jo",
            "kh",
            "km",
            "kp",
            "lb",
            "lr",
            "mc",
            "mh",
            "mil",
            "mm",
            "mt",
            "mv",
            "mw",
            "ne",
            "ni",
            "np",
            "nr",
            "pa",
            "pg",
            "ph",
            "pk",
            "pn",
            "py",
            "sd",
            "sr",
            "ss",
            "sv",
            "sz",
            "tj",
            "tp",
            "tt",
            "va",
            "vi",
            "vn",
            "ye",
            "zw",
        ]

    @classmethod
    def _iana_database(cls):
        """
        Convert :code:`iana-domains-db.json` into a dictionnary.

        :return: The content of the database in dictionnary format.
        :rtype: dict
        """

        # We construct/get the file to read.
        file_to_read = (
            PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS["default_files"]["iana"]
        )

        # And we read and return the database file.
        return Dict().from_json(File(file_to_read).read())

    def get(self):
        """
        Return the referer aka the WHOIS server of the current domain extension.
        """

        if not PyFunceble.CONFIGURATION["local"]:
            # We are not running a test in a local network.

            if self.domain_extension not in self.ignored_extension:
                # The extension of the domain we are testing is not into
                # the list of ignored extensions.

                # We set the referer to None as we do not have any.
                referer = None

                if "iana_db" not in PyFunceble.CONFIGURATION:
                    # The iana database is empty.

                    # We generate/construct the database from the local file.
                    PyFunceble.CONFIGURATION["iana_db"] = self._iana_database()

                if self.domain_extension in PyFunceble.CONFIGURATION["iana_db"]:
                    # The domain extension is in the iana database.

                    if not PyFunceble.CONFIGURATION["no_whois"]:
                        # We are authorized to use WHOIS for the test result.

                        # We get the referer from the database.
                        referer = PyFunceble.CONFIGURATION["iana_db"][
                            self.domain_extension
                        ]

                        if not referer:
                            # The referer is not filled.

                            # We log the case of the current extension.
                            self.log()

                            # And we handle and return the down status.
                            return Status(
                                PyFunceble.STATUS["official"]["down"]
                            ).handle()

                        # The referer is into the database.

                        # We return the extracted referer.
                        return referer

                    # We are not authorized to use WHOIS for the test result.

                    # We return None.
                    return None

                # The domain extension is not in the iana database.

                # We hanlde and return the invalid status.
                return Status(PyFunceble.STATUS["official"]["invalid"]).handle()

            # The extension of the domain we are testing is not into
            # the list of ignored extensions.

            # We handle and return the down status.
            return Status(PyFunceble.STATUS["official"]["down"]).handle()

        # We are running a test in a local network.

        # We return None.
        return None

    def log(self):
        """
        Log if no referer is found for a domain extension.
        """

        if PyFunceble.CONFIGURATION["logs"]:
            # The generation of logs is activated.

            # * We initiate a separator between the older and the current one.
            # and
            # * We initiate the message to print.
            logs = "=" * 100
            logs += "\nNo referer found for: %s domains\n" % self.domain_extension
            logs += "=" * 100
            logs += "\n"

            # We write the log into the file.
            File(
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["no_referer"]
                + self.domain_extension
            ).write(logs)

            if PyFunceble.CONFIGURATION["share_logs"]:
                # The logs sharing is activated.

                # We initiate the data to share.
                data_to_share = {"extension": self.domain_extension}

                # We post the data to the API.
                PyFunceble.requests.post(
                    PyFunceble.LINKS["api_no_referer"], data=data_to_share
                )
