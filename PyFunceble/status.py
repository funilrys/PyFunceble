#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will manage the status.

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
import PyFunceble
from PyFunceble.generate import Generate
from PyFunceble.lookup import Lookup


class Status:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Hanle the research of domain status in case we don't use
    WHOIS or in case that WHOIS record is not readable nor exploitable.

    :param matched_result: The previously catched status.
    :type matched_result: str
    """

    def __init__(self, matched_status, invalid_source="IANA"):
        # We get the the parsed status.
        self.matched_status = matched_status

        # We get the parsed source.
        self.invalid_source = invalid_source

    def handle(self):
        """
        Handle the lack of WHOIS. :smile_cat:

        :return:
            The strus of the domain after generating the files desired
            by the user.
        :rtype: str
        """

        if self.matched_status.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            # The matched status is not in the list of invalid status.

            # We initiate the source we are going to parse to the Generate class.
            source = "NSLOOKUP"

            if Lookup().nslookup():
                # We could execute the nslookup logic.

                # We generate the status files with the up status.
                Generate(PyFunceble.STATUS["official"]["up"], source).status_file()

                # We return the up status.
                return PyFunceble.STATUS["official"]["up"]

            # We could not execute the nslookup logic.

            # * We generate the status file with the down status.
            Generate(PyFunceble.STATUS["official"]["down"], source).status_file()

            # We return the down status.
            return PyFunceble.STATUS["official"]["down"]

        # The matched status is in the list of invalid status.

        # We generate the status file with the invalid status.
        Generate(
            PyFunceble.STATUS["official"]["invalid"], self.invalid_source
        ).status_file()

        # We return the invalid status.
        return PyFunceble.STATUS["official"]["invalid"]


class URLStatus:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status when testing for URL.

    :param catched_status: THe catched status.
    :type catched_status: str
    """

    def __init__(self, catched_status):
        # We get the parsed status.
        self.catched = catched_status

    def handle(self):
        """
        Handle the backend of the given status.
        """

        # We initiate the source we are going to parse to the Generate class.
        source = "URL"

        if self.catched.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            # The parsed status is not in the list of invalid.

            # We generate the status file with the catched status.
            Generate(self.catched, source).status_file()
        else:
            # The parsed status is in the list of invalid.

            # We generate the status file with the parsed status.
            Generate(self.catched, "SYNTAX").status_file()

        # We return the parsed status.
        return self.catched


class SyntaxStatus:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status when testing for Syntax.

    :param catched_status: THe catched status.
    :type catched_status: str
    """

    def __init__(self, catched_status):
        # We get the parsed status.
        self.catched = catched_status

    def handle(self):
        """
        Handle the backend of the given status.
        """

        # We generate the status file with the catched status.
        Generate(self.catched, "SYNTAX").status_file()

        # We return the parsed status.
        return self.catched
