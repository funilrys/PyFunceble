#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the database logic and interface.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import path, strftime
from PyFunceble.helpers import Dict, File


class Database(object):
    """
    Logic behind the generation and the usage of a database system.
    The main idea behind this is to provide an inactive-db.json and test all
    inactive domain which are into to it regularly
    """

    def __init__(self):
        self.file_path = PyFunceble.CONFIGURATION["file_to_test"]
        self.current_time = int(strftime("%s"))
        self.day_in_seconds = PyFunceble.CONFIGURATION[
            "days_between_db_retest"
        ] * 24 * 3600
        self.inactive_db_path = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS[
            "default_files"
        ][
            "inactive_db"
        ]

    def _retrieve(self):
        """
        Return the current content of the inactive-db.json file.
        """

        if path.isfile(self.inactive_db_path):
            PyFunceble.CONFIGURATION["inactive_db"] = Dict().from_json(
                File(self.inactive_db_path).read()
            )
        else:
            PyFunceble.CONFIGURATION["inactive_db"] = {}

        return

    def _backup(self):
        """
        Save the current database into the inactive-db.json file.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            Dict(PyFunceble.CONFIGURATION["inactive_db"]).to_json(self.inactive_db_path)

    def _add_to_test(self, to_add):
        """
        Add an element or a list of element into
        PyFunceble.CONFIGURATION['inactive_db'][self.file_path]['to_test'].

        Argument:
            - to_add: str
                The domain or ip to add.
        """

        if not isinstance(to_add, list):
            to_add = [to_add]

        if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
            if "to_test" in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                    "to_test"
                ].extend(
                    to_add
                )
            else:
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                    "to_test"
                ] = to_add
        else:
            PyFunceble.CONFIGURATION["inactive_db"].update(
                {self.file_path: {"to_test": to_add}}
            )

        self._backup()

    def to_test(self):
        """
        Get the list to test for the next session.
        """

        result = []
        to_delete = []

        self._retrieve()

        if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
            for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                if data != "to_test":
                    if self.current_time > int(data) + self.day_in_seconds:
                        result.extend(
                            PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                                data
                            ]
                        )
                        to_delete.append(data)

            Dict(PyFunceble.CONFIGURATION["inactive_db"][self.file_path]).remove_key(
                to_delete
            )

            self._add_to_test(result)
        else:
            PyFunceble.CONFIGURATION["inactive_db"].update({self.file_path: {}})

        self._backup()

    def _timestamp(self):
        """
        Return the timestamp where we are going to save our current list.

        Returns: int or str
            The timestamp to append with the currently tested domains.
        """

        result = 0
        to_delete = []

        if self.file_path in PyFunceble.CONFIGURATION[
            "inactive_db"
        ] and PyFunceble.CONFIGURATION[
            "inactive_db"
        ][
            self.file_path
        ]:
            for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                if data != "to_test":
                    if self.current_time < int(data) + self.day_in_seconds:
                        result = int(data)
                    else:
                        result = self.current_time
                        to_delete.append(data)

            for element in to_delete:
                self._add_to_test(
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][element]
                )
            Dict(PyFunceble.CONFIGURATION["inactive_db"][self.file_path]).remove_key(
                to_delete
            )

            return result

        return self.current_time

    def add(self):
        """
        Save the current PyFunceble.CONFIGURATION['domain'] into the current timestamp.
        """

        timestamp = str(self._timestamp())

        if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
            if timestamp in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                if PyFunceble.CONFIGURATION["domain"] not in PyFunceble.CONFIGURATION[
                    "inactive_db"
                ][
                    self.file_path
                ][
                    timestamp
                ]:
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        timestamp
                    ].append(
                        PyFunceble.CONFIGURATION["domain"]
                    )
            else:
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path].update(
                    {timestamp: [PyFunceble.CONFIGURATION["domain"]]}
                )

            if "to_test" in PyFunceble.CONFIGURATION["inactive_db"][
                self.file_path
            ] and PyFunceble.CONFIGURATION[
                "domain"
            ] in PyFunceble.CONFIGURATION[
                "inactive_db"
            ][
                self.file_path
            ][
                "to_test"
            ]:
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                    "to_test"
                ].remove(
                    PyFunceble.CONFIGURATION["domain"]
                )
        else:
            PyFunceble.CONFIGURATION["inactive_db"][self.file_path] = {
                timestamp: [PyFunceble.CONFIGURATION["domain"]]
            }

        self._backup()

    def remove(self):
        """
        Remove all occurence of PyFunceble.CONFIGURATION['domain'] into the database.
        """

        if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
            for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                if PyFunceble.CONFIGURATION["domain"] in PyFunceble.CONFIGURATION[
                    "inactive_db"
                ][
                    self.file_path
                ][
                    data
                ]:
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        data
                    ].remove(
                        PyFunceble.CONFIGURATION["domain"]
                    )

        self._backup()
