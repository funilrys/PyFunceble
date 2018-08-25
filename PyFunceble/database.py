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
from PyFunceble import path, time
from PyFunceble.helpers import Dict, File, List


class Database:
    """
    Logic behind the generation and the usage of a database system.
    The main idea behind this is to provide an inactive-db.json and test all
    inactive domain which are into to it regularly
    """

    def __init__(self):
        self.file_path = PyFunceble.CONFIGURATION["file_to_test"]

        self.one_day_in_seconds = 1 * 24 * 3600
        self.days_in_seconds = (
            PyFunceble.CONFIGURATION["days_between_db_retest"] * 24 * 3600
        )

        self.inactive_db_path = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["inactive_db"]
        )

        if "domain" in PyFunceble.CONFIGURATION and PyFunceble.CONFIGURATION["domain"]:
            self.element = PyFunceble.CONFIGURATION["domain"]
        elif "URL" in PyFunceble.CONFIGURATION and PyFunceble.CONFIGURATION["URL"]:
            self.element = PyFunceble.CONFIGURATION["URL"]

    def _reformat_historical_formating_error(self):  # pragma: no cover
        """
        This method will format the old format so it can be merge into the newer format.
        """

        historical_formating_error = PyFunceble.CURRENT_DIRECTORY + "inactive-db.json"

        if path.isfile(historical_formating_error):
            data = Dict().from_json(File(historical_formating_error).read())

            data_to_parse = {}
            top_keys = data.keys()

            for top_key in top_keys:
                low_keys = data[top_key].keys()
                data_to_parse[top_key] = {}

                for low_key in low_keys:
                    if low_key.isdigit():
                        data_to_parse[top_key][
                            int(low_key) - (self.one_day_in_seconds * 30)
                        ] = data[top_key][low_key]
                    else:
                        data_to_parse[top_key][
                            int(time()) - (self.one_day_in_seconds * 30)
                        ] = data[top_key][low_key]

            if PyFunceble.CONFIGURATION["inactive_db"]:
                PyFunceble.CONFIGURATION["inactive_db"].update(data_to_parse)
            else:
                PyFunceble.CONFIGURATION["inactive_db"] = data_to_parse

            File(historical_formating_error).delete()

    def _merge_new_into_old(self):
        """
        This method will merge the real database with the older one which
        has already been set into PyFunceble.CONFIGURATION["inactive_db"]
        """

        database_content = Dict().from_json(File(self.inactive_db_path).read())

        database_top_keys = database_content.keys()

        for database_top_key in database_top_keys:
            if database_top_key not in PyFunceble.CONFIGURATION["inactive_db"]:
                PyFunceble.CONFIGURATION["inactive_db"][
                    database_top_key
                ] = database_content[database_top_key]
            else:
                database_low_keys = database_content[database_top_key].keys()

                for database_low_key in database_low_keys:
                    if (
                        database_low_key
                        not in PyFunceble.CONFIGURATION["inactive_db"][database_top_key]
                    ):  # pragma: no cover
                        PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                            database_low_key
                        ] = database_content[database_top_key][database_low_key]
                    else:
                        PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                            database_low_key
                        ].extend(database_content[database_top_key][database_low_key])
                        PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                            database_low_key
                        ] = List(
                            PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                                database_low_key
                            ]
                        ).format()

    def _retrieve(self):
        """
        Return the current content of the inactive-db.json file.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            self._reformat_historical_formating_error()

            if path.isfile(self.inactive_db_path):
                self._merge_new_into_old()
            else:
                PyFunceble.CONFIGURATION["inactive_db"] = {}

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

        if PyFunceble.CONFIGURATION["inactive_database"]:
            if not isinstance(to_add, list):
                to_add = [to_add]

            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                if "to_test" in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ].extend(to_add)
                else:
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ] = to_add
            else:
                PyFunceble.CONFIGURATION["inactive_db"].update(
                    {self.file_path: {"to_test": to_add}}
                )

            PyFunceble.CONFIGURATION["inactive_db"][self.file_path]["to_test"] = List(
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path]["to_test"]
            ).format()

            self._backup()

    def to_test(self):
        """
        Get the list to test for the next session.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            result = []
            to_delete = []

            self._retrieve()

            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    if data != "to_test":
                        if int(time()) > int(data) + self.days_in_seconds:
                            result.extend(
                                PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                                    data
                                ]
                            )
                            to_delete.append(data)

                Dict(
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path]
                ).remove_key(to_delete)

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

        if PyFunceble.CONFIGURATION["inactive_database"]:
            if (
                self.file_path in PyFunceble.CONFIGURATION["inactive_db"]
                and PyFunceble.CONFIGURATION["inactive_db"][self.file_path]
            ):
                database_keys = list(
                    filter(
                        lambda x: x.isdigit(),
                        PyFunceble.CONFIGURATION["inactive_db"][self.file_path].keys(),
                    )
                )

                if database_keys:
                    recent_date = max(database_keys)
                else:  # pragma: no cover
                    return int(time())

                if int(time()) > int(recent_date) + self.one_day_in_seconds:
                    return int(time())

                if int(time()) < int(recent_date) + self.days_in_seconds:
                    return int(recent_date)

        return int(time())

    def add(self):
        """
        Save the current PyFunceble.CONFIGURATION['domain'] into the current timestamp.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            timestamp = str(self._timestamp())

            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                if timestamp in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    if (
                        self.element
                        not in PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                            timestamp
                        ]
                    ):
                        PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                            timestamp
                        ].append(self.element)
                else:
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path].update(
                        {timestamp: [self.element]}
                    )

                if (
                    "to_test" in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]
                    and self.element
                    in PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ]
                ):
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ].remove(self.element)
            else:
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path] = {
                    timestamp: [self.element]
                }

            self._backup()

    def remove(self):
        """
        Remove all occurence of PyFunceble.CONFIGURATION['domain'] into the database.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    if (
                        self.element
                        in PyFunceble.CONFIGURATION["inactive_db"][self.file_path][data]
                    ):
                        PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                            data
                        ].remove(self.element)

            self._backup()

    def content(self):
        """
        This method will return the content of the database.
        """

        result = []

        if (
            PyFunceble.CONFIGURATION["inactive_database"]
            and PyFunceble.CONFIGURATION["inactive_db"]
        ):
            for key in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                if key == "to_test":
                    continue

                result.extend(
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][key]
                )

        return result
