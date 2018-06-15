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

This submodule will manage the status interface.

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


class Status(object):  # pragma: no cover  # pylint: disable=too-few-public-methods
    """
    Return the domain status in case we don't use WHOIS or in case that WHOIS
    record is not readable.

    Argument:
        - matched_result: str
            The previously catched status.
    """

    def __init__(self, matched_status):
        self.matched_status = matched_status

    def handle(self):
        """
        Handle the lack of WHOIS. :)

        Returns: str
            The status of the domains after generating the files.
        """

        source = "NSLOOKUP"

        if self.matched_status.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            if Lookup().nslookup():
                Generate(PyFunceble.STATUS["official"]["up"], source).status_file()
                return PyFunceble.STATUS["official"]["up"]

            Generate(PyFunceble.STATUS["official"]["down"], source).status_file()
            return PyFunceble.STATUS["official"]["down"]

        Generate(PyFunceble.STATUS["official"]["invalid"], "IANA").status_file()
        return PyFunceble.STATUS["official"]["invalid"]


class URLStatus(object):  # pragma: no cover  # pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status.

    Argument:
        - catched_status: str
            The catched status.
    """

    def __init__(self, catched_status):
        self.catched = catched_status

    def handle(self):
        """
        Handle the backend of the given status.
        """

        source = "URL"

        if self.catched.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            Generate(self.catched, source).status_file()
        else:
            Generate(self.catched, "IANA").status_file()

        return self.catched
