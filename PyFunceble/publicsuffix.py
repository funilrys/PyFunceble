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

This submodule will provide us a place and way to intertact with the helpful public sufix database.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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
from PyFunceble.helpers import Dict, Download, File, List


class PublicSuffix:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Let us interact with the public suffix database.
    """

    def __init__(self, live=True):
        # We initiate the destination of our database.
        self.destination = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["public_suffix"]
        )

        # We initiate a variablw which will save the database we are going to save.
        self.public_suffix_db = {}

        if "psl_db" not in PyFunceble.CONFIGURATION:
            # The psl database was not initiated.

            PyFunceble.CONFIGURATION["psl_db"] = {}

        if live:
            if not PyFunceble.CONFIGURATION["quiet"]:
                # The quiet mode is not activated.

                # We print a message for the user on screen.
                print(
                    "Update of %s"
                    % PyFunceble.OUTPUTS["default_files"]["public_suffix"],
                    end=" ",
                )

            # And we run the update logic.
            self.update()

    @classmethod
    def _data(cls):
        """
        Get the database from the public suffix repository.
        """

        # We initiate a variable which will save the link to the upstream public suffix file.
        public_suffix_url = "https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat"

        # And we return the content of the previously declared link.
        return Download(public_suffix_url, return_data=True).text()

    def _extensions(self, line):
        """
        Extract the extension from the given line.

        :param line: The line from the official public suffix repository.
        :type line: str
        """

        # We strip the parsed line.
        line = line.strip()

        if not line.startswith("//") and "." in line:
            # * The parsed line is not a commented line.
            # and
            # * There is a point in the parsed line.
            line = line.encode("idna").decode("utf-8")

            if line.startswith("*."):
                # The parsed line start with `*.`.

                # We remove the first two characters.
                line = line[2:]

            # We we split the points and we get the last element.
            # Explanation: The idea behind this action is to
            # always get the extension.
            extension = line.split(".")[-1]

            if extension in self.public_suffix_db:
                # The extension is alrady in our database.

                # We update the content of the 1st level TDL with
                # the content of the suffix.
                # In between, we format so that we ensure that there is no
                # duplicate in the database index content.
                self.public_suffix_db[extension] = List(
                    self.public_suffix_db[extension] + [line]
                ).format()
            else:
                # The extension is not already in our database.

                # We append the currently formatted extension and the line content.
                self.public_suffix_db.update({extension: [line]})

    def update(self):
        """
        Update of the content of the :code:`public-suffix.json`.
        """

        # We loop through the line of the upstream file.
        list(map(self._extensions, self._data().split("\n")))

        # We save the content of our database in the final testination.
        Dict(self.public_suffix_db).to_json(self.destination)

        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            # We inform the user that everything goes right.
            print(PyFunceble.CONFIGURATION["done"])

    def load(self):
        """
        Load the public suffix database into the system.
        """

        if not PyFunceble.CONFIGURATION["psl_db"]:
            # The public database was not already loaded.

            # * We read, convert to dict and return the file content.
            # and
            # * We fill the database.
            PyFunceble.CONFIGURATION["psl_db"].update(
                Dict().from_json(File(self.destination).read())
            )
