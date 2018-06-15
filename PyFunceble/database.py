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

This submodule will provide the database logic and interface.

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
