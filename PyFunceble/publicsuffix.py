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

This submodule will helps us intert with the helpful public sufix.

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

import PyFunceble
from PyFunceble.helpers import Dict, Download, List


class PublicSuffix:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    This class will help us interract with the public suffix database.
    """

    def __init__(self):
        if not PyFunceble.CONFIGURATION["quiet"]:
            print(
                "Update of %s" % PyFunceble.OUTPUTS["default_files"]["public_suffix"],
                end=" ",
            )

        self.destination = PyFunceble.OUTPUTS["default_files"]["public_suffix"]

        self.public_suffix_db = {}
        self.update()

    @classmethod
    def _data(cls):
        """
        Get the database from the public suffix repository.
        """

        public_suffix_url = "https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat"

        return Download(public_suffix_url, return_data=True).text()

    def _extensions(self, line):
        """
        Extract the extension from the given line.

        Argument:
            - line: str
                The line from the official public suffix repository.
        """

        line = line.strip()

        if not line.startswith("//") and "." in line:
            line = line.encode("idna").decode("utf-8")

            if line.startswith("*."):
                line = line[2:]

            extension = line.split(".")[-1]

            if extension in self.public_suffix_db:
                self.public_suffix_db[extension] = List(
                    self.public_suffix_db[extension] + [line]
                ).format()
            else:
                self.public_suffix_db.update({extension: [line]})

    def update(self):
        """
        Update of the content of the `public-suffix.json`.
        """

        list(map(self._extensions, self._data().split("\n")))
        Dict(self.public_suffix_db).to_json(self.destination)

        if not PyFunceble.CONFIGURATION["quiet"]:
            print(PyFunceble.CONFIGURATION["done"])
